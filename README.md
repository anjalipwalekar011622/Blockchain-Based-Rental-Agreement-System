# 🔗 Blockchain-Based Rental Agreement System

A blockchain-powered web application that auto-generates rental agreements and provides cryptographic tamper detection using Ethereum smart contracts.

---

## Project Overview

Traditional rental agreements are paper-based, easily forged, and lack transparency. This system addresses these problems by:

- Auto-generating professional rental agreement PDFs
- Computing SHA-256 cryptographic hash of each agreement
- Storing the hash permanently on Ethereum blockchain
- Allowing anyone to verify if an agreement has been tampered with

---

## Research Gap Addressed

While existing works focus on full-fledged decentralized rental ecosystems, there is limited implementation of **lightweight, automated agreement integrity verification** mechanisms suitable for real-world adoption. This project addresses this gap by proposing a blockchain-based auto-generated rental agreement system with tamper-detection capability.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python Flask |
| Blockchain | Ethereum (Ganache local) |
| Smart Contract | Solidity 0.8.21 |
| Contract Deployment | Truffle |
| Blockchain Interaction | Web3.py |
| PDF Generation | ReportLab |
| Hashing | SHA-256 |

---

## Project Structure
```
rental-agreement-blockchain/
│
├── contracts/
│   └── RentalAgreement.sol       ← Solidity smart contract
│
├── migrations/
│   └── 2_deploy_rental.js        ← Truffle deployment script
│
├── static/
│   ├── style.css                 ← Stylesheet
│   └── agreements/               ← Generated PDFs stored here
│
├── templates/
│   ├── index.html                ← Generate agreement page
│   └── verify.html               ← Verify agreement page
│
├── app.py                        ← Flask backend
├── blockchain.py                 ← Web3 / contract interaction
├── hash_utils.py                 ← SHA-256 hashing logic
├── pdf_generator.py              ← PDF generation logic
├── truffle-config.js             ← Truffle configuration
└── requirements.txt              ← Python dependencies
```

---

## How to Run

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/rental-agreement-blockchain.git
cd rental-agreement-blockchain
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Truffle and Ganache
```bash
npm install -g truffle ganache
```

### 4. Start Ganache (Terminal 1)
```bash
ganache --port 7545
```

### 5. Deploy smart contract (Terminal 2)
```bash
truffle migrate --network development
```
Copy the contract address from output and update `CONTRACT_ADDRESS` in `blockchain.py`

### 6. Run the Flask app
```bash
python app.py
```

### 7. Open in browser
```
http://127.0.0.1:5000
```

---

## Key Features

### Agreement Generation
- Fill landlord/tenant details in web form
- Auto-generates professional PDF agreement
- Computes SHA-256 hash of the document
- Stores hash permanently on blockchain

### Tamper Detection
- Upload any agreement PDF
- Enter its Agreement ID
- System recomputes hash and compares with blockchain
- Instantly detects if document was modified

---

## How It Works
```
User fills form
      ↓
PDF Agreement generated
      ↓
SHA-256 Hash computed
      ↓
Hash stored on Ethereum blockchain
      ↓
Agreement ID returned to user
      ↓
Later: Upload PDF + Agreement ID
      ↓
Hash recomputed and compared
      ↓
✅ Authentic  OR  ❌ Tampered
```

---

## Literature Review Mapping

| Paper | Our Contribution |
|-------|-----------------|
| Tseng et al. — Trustworthy Rental Market | Extends with lightweight hash verification |
| Santos et al. — Blockchain Documentation | Adds auto-generation + web interface |
| Patil et al. — Decentralized Rental System | Simplifies for real-world student PoC |
| ISROSET — Smart Contract Lease | Adds tamper detection module |
| IJARSCT — Auto Generated Agreement | Implements with full working prototype |

---

## Developed By

- **Name:** Anjali Walekar, Anushree Verma, Allison Suvarna, Srushti Thakur
- **Project Type:** Academic PoC (Proof of Concept)
- **Domain:** Blockchain, Web Development
