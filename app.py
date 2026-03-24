from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
import os
from models import db, User, AgreementRecord
from pdf_generator import generate_agreement
from hash_utils import compute_hash
from blockchain import store_agreement, get_agreement

app = Flask(__name__)

# -----------------------------------------------
# CONFIG
# -----------------------------------------------
app.config['SECRET_KEY'] = 'rentalchain_secret_key_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rentalchain.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please login to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()

# -----------------------------------------------
# PUBLIC ROUTES
# -----------------------------------------------

@app.route('/')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # Check if email exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please login.', 'error')
            return redirect(url_for('register'))

        # Hash password securely
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create new user
        new_user = User(
            full_name=full_name,
            email=email,
            password_hash=password_hash,
            role=role
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('about'))


# -----------------------------------------------
# PROTECTED ROUTES
# -----------------------------------------------

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'landlord':
        # Landlord sees agreements they created
        agreements = AgreementRecord.query.filter_by(
            landlord_id=current_user.id
        ).order_by(AgreementRecord.created_at.desc()).all()
    else:
        # Tenant sees agreements linked to their ID
        agreements = AgreementRecord.query.filter_by(
            tenant_id=current_user.id
        ).order_by(AgreementRecord.created_at.desc()).all()

    return render_template('dashboard.html', agreements=agreements)


@app.route('/profile')
@login_required
def profile():
    if current_user.role == 'landlord':
        total_agreements = AgreementRecord.query.filter_by(
            landlord_id=current_user.id).count()
    else:
        total_agreements = AgreementRecord.query.filter(
            AgreementRecord.tenant_name.ilike(f'%{current_user.full_name}%')
        ).count()
    return render_template('profile.html', total_agreements=total_agreements)


@app.route('/generate-page')
@login_required
def generate_page():
    if current_user.role != 'landlord':
        flash('Only landlords can generate agreements.', 'error')
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/verify')
@login_required
def verify_page():
    return render_template('verify.html')


# -----------------------------------------------
# API ROUTES
# -----------------------------------------------

@app.route('/generate', methods=['POST'])
@login_required
def generate():
    if current_user.role != 'landlord':
        return jsonify({'success': False, 'error': 'Only landlords can generate agreements.'})

    try:
        # Get tenant email from form
        tenant_email = request.form['tenant_email']

        # Check if tenant exists in database
        tenant_user = User.query.filter_by(
            email=tenant_email, 
            role='tenant'
        ).first()

        if not tenant_user:
            return jsonify({
                'success': False,
                'error': f'Tenant with email "{tenant_email}" not found. Ask them to register on RentalChain first.'
            })

        data = {
            'landlord_name': request.form['landlord_name'],
            'tenant_name': tenant_user.full_name,  # Use name from database
            'property_address': request.form['property_address'],
            'rent_amount': request.form['rent_amount'],
            'duration_months': request.form['duration_months'],
            'start_date': request.form['start_date'],
            'deposit_amount': request.form['deposit_amount']
        }

        # Generate PDF
        filepath, filename = generate_agreement(data)

        # Compute hash
        pdf_hash = compute_hash(filepath)

        # Store on blockchain
        blockchain_result = store_agreement(
            pdf_hash,
            data['landlord_name'],
            data['tenant_name'],
            data['property_address'],
            data['rent_amount']
        )

        if blockchain_result['success']:
            # Save to database — now with tenant_id linked!
            record = AgreementRecord(
                landlord_id=current_user.id,
                tenant_id=tenant_user.id,        # ← linked to tenant
                tenant_email=tenant_email,        # ← tenant email saved
                landlord_name=data['landlord_name'],
                tenant_name=data['tenant_name'],
                property_address=data['property_address'],
                rent_amount=data['rent_amount'],
                duration_months=data['duration_months'],
                start_date=data['start_date'],
                deposit_amount=data['deposit_amount'],
                pdf_filename=filename,
                sha256_hash=pdf_hash,
                blockchain_agreement_id=blockchain_result['agreement_id'],
                transaction_hash=blockchain_result['transaction_hash'],
                block_number=blockchain_result['block_number']
            )
            db.session.add(record)
            db.session.commit()

            return jsonify({
                'success': True,
                'filename': filename,
                'hash': pdf_hash,
                'agreement_id': blockchain_result['agreement_id'],
                'transaction_hash': blockchain_result['transaction_hash'],
                'block_number': blockchain_result['block_number'],
                'tenant_name': tenant_user.full_name  # ← confirm tenant found
            })
        else:
            return jsonify({'success': False, 'error': blockchain_result['error']})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download/<filename>')
@login_required
def download(filename):
    filepath = os.path.join('static', 'agreements', filename)
    return send_file(filepath, as_attachment=True)


@app.route('/verify-agreement', methods=['POST'])
@login_required
def verify_agreement():
    try:
        agreement_id = request.form['agreement_id']
        uploaded_file = request.files['agreement_file']

        if uploaded_file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})

        temp_path = os.path.join('static', 'agreements', 'temp_verify.pdf')
        uploaded_file.save(temp_path)

        uploaded_hash = compute_hash(temp_path)
        stored = get_agreement(agreement_id)

        if not stored['success']:
            return jsonify({'success': False, 'error': 'Agreement ID not found on blockchain'})

        is_authentic = stored['hash'] == uploaded_hash
        os.remove(temp_path)

        return jsonify({
            'success': True,
            'is_authentic': is_authentic,
            'agreement_id': agreement_id,
            'stored_hash': stored['hash'],
            'uploaded_hash': uploaded_hash,
            'tenant': stored['tenant'],
            'landlord': stored['landlord'],
            'property': stored['property'],
            'rent': stored['rent']
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True, port=5000)