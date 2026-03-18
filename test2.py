from blockchain import w3, store_agreement, get_agreement
from hash_utils import compute_hash
from pdf_generator import generate_agreement

# Step 1: Generate agreement
data = {
    'landlord_name': 'Anjali Walekar',
    'tenant_name': 'Priya Sharma',
    'property_address': '204, Sunshine Apartments, Andheri West, Mumbai',
    'rent_amount': '25000',
    'duration_months': '11',
    'start_date': '2025-04-01',
    'deposit_amount': '75000'
}

print("📄 Generating agreement...")
filepath, filename = generate_agreement(data)
print(f"✅ PDF created: {filename}")

# Step 2: Compute hash
print("\n🔐 Computing hash...")
pdf_hash = compute_hash(filepath)
print(f"✅ Hash: {pdf_hash}")

# Step 3: Store on blockchain
print("\n⛓️ Storing hash on blockchain...")
result = store_agreement(
    pdf_hash,
    data['landlord_name'],
    data['tenant_name'],
    data['property_address'],
    data['rent_amount']
)

if result['success']:
    print(f"✅ Stored on blockchain!")
    print(f"   Agreement ID : {result['agreement_id']}")
    print(f"   Transaction  : {result['transaction_hash']}")
    print(f"   Block Number : {result['block_number']}")
else:
    print(f"❌ Error: {result['error']}")

# Step 4: Retrieve from blockchain
print("\n📖 Retrieving from blockchain...")
stored = get_agreement(result['agreement_id'])
if stored['success']:
    print(f"✅ Retrieved!")
    print(f"   Tenant  : {stored['tenant']}")
    print(f"   Landlord: {stored['landlord']}")
    print(f"   Hash    : {stored['hash']}")