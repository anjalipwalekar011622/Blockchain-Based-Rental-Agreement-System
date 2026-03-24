from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    agreements_as_landlord = db.relationship(
        'AgreementRecord',
        foreign_keys='AgreementRecord.landlord_id',
        backref='landlord',
        lazy=True
    )
    agreements_as_tenant = db.relationship(
        'AgreementRecord',
        foreign_keys='AgreementRecord.tenant_id',
        backref='tenant_user',
        lazy=True
    )

class AgreementRecord(db.Model):
    __tablename__ = 'agreements'
    
    id = db.Column(db.Integer, primary_key=True)
    landlord_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # ← NEW
    
    landlord_name = db.Column(db.String(100), nullable=False)
    tenant_name = db.Column(db.String(100), nullable=False)
    tenant_email = db.Column(db.String(120), nullable=True)  # ← NEW
    property_address = db.Column(db.String(255), nullable=False)
    rent_amount = db.Column(db.String(20), nullable=False)
    duration_months = db.Column(db.String(10), nullable=False)
    start_date = db.Column(db.String(20), nullable=False)
    deposit_amount = db.Column(db.String(20), nullable=False)
    
    pdf_filename = db.Column(db.String(255), nullable=False)
    sha256_hash = db.Column(db.String(64), nullable=False)
    blockchain_agreement_id = db.Column(db.Integer, nullable=True)
    transaction_hash = db.Column(db.String(255), nullable=True)
    block_number = db.Column(db.Integer, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Agreement {self.id} - {self.tenant_name}>'