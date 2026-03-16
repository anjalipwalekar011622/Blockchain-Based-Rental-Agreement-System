from pdf_generator import generate_agreement
from hash_utils import compute_hash

# Sample rental data
data = {
    'landlord_name': 'Anjali Walekar',
    'tenant_name': 'Priya Sharma',
    'property_address': '204, Sunshine Apartments, Andheri West, Mumbai - 400058',
    'rent_amount': '25000',
    'duration_months': '11',
    'start_date': '2025-04-01',
    'deposit_amount': '75000'
}

# Generate PDF
print("Generating agreement...")
filepath, filename = generate_agreement(data)
print(f"Agreement created: {filepath}")

# Compute hash
print("\nComputing hash...")
hash_value = compute_hash(filepath)
print(f"SHA-256 Hash: {hash_value}")
print(f"\nThis 64-character string is the document's fingerprint.")
print(f"This is what gets stored on the blockchain.")