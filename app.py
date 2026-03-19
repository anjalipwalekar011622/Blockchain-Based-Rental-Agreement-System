from flask import Flask, render_template, request, jsonify, send_file
import os
from pdf_generator import generate_agreement
from hash_utils import compute_hash
from blockchain import store_agreement, get_agreement, verify_on_blockchain

app = Flask(__name__)

# -----------------------------------------------
# PAGE ROUTES
# -----------------------------------------------

@app.route('/')
def index():
    """Home page — Generate agreement form"""
    return render_template('index.html')

@app.route('/verify')
def verify_page():
    """Verification page"""
    return render_template('verify.html')

# -----------------------------------------------
# API ROUTES
# -----------------------------------------------

@app.route('/generate', methods=['POST'])
def generate():
    """
    Takes form data → generates PDF → computes hash → stores on blockchain
    Returns agreement details and blockchain info
    """
    try:
        # Get form data
        data = {
            'landlord_name': request.form['landlord_name'],
            'tenant_name': request.form['tenant_name'],
            'property_address': request.form['property_address'],
            'rent_amount': request.form['rent_amount'],
            'duration_months': request.form['duration_months'],
            'start_date': request.form['start_date'],
            'deposit_amount': request.form['deposit_amount']
        }

        # Step 1: Generate PDF
        filepath, filename = generate_agreement(data)

        # Step 2: Compute hash
        pdf_hash = compute_hash(filepath)

        # Step 3: Store on blockchain
        blockchain_result = store_agreement(
            pdf_hash,
            data['landlord_name'],
            data['tenant_name'],
            data['property_address'],
            data['rent_amount']
        )

        if blockchain_result['success']:
            return jsonify({
                'success': True,
                'filename': filename,
                'hash': pdf_hash,
                'agreement_id': blockchain_result['agreement_id'],
                'transaction_hash': blockchain_result['transaction_hash'],
                'block_number': blockchain_result['block_number']
            })
        else:
            return jsonify({
                'success': False,
                'error': blockchain_result['error']
            })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/download/<filename>')
def download(filename):
    """Download generated PDF"""
    filepath = os.path.join('static', 'agreements', filename)
    return send_file(filepath, as_attachment=True)


@app.route('/verify-agreement', methods=['POST'])
def verify_agreement():
    """
    Takes uploaded PDF + agreement ID → 
    recomputes hash → compares with blockchain →
    returns authentic or tampered
    """
    try:
        # Get agreement ID from form
        agreement_id = request.form['agreement_id']

        # Get uploaded file
        uploaded_file = request.files['agreement_file']

        if uploaded_file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})

        # Save uploaded file temporarily
        temp_path = os.path.join('static', 'agreements', 'temp_verify.pdf')
        uploaded_file.save(temp_path)

        # Recompute hash of uploaded file
        uploaded_hash = compute_hash(temp_path)

        # Get stored data from blockchain
        stored = get_agreement(agreement_id)

        if not stored['success']:
            return jsonify({'success': False, 'error': 'Agreement ID not found on blockchain'})

        # Compare hashes
        is_authentic = stored['hash'] == uploaded_hash

        # Clean up temp file
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