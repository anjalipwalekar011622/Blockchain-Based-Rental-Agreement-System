// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

contract RentalAgreement {
    
    // This is the structure of each agreement stored on blockchain
    struct Agreement {
        uint256 agreementId;      // Unique ID
        string agreementHash;     // SHA-256 hash of the PDF
        string landlordName;      // Landlord name
        string tenantName;        // Tenant name
        string propertyAddress;   // Property address
        uint256 rentAmount;       // Monthly rent
        uint256 timestamp;        // When it was stored
        bool isActive;            // Is agreement still active
    }

    // Store all agreements — ID maps to Agreement struct
    mapping(uint256 => Agreement) public agreements;
    
    // Keep track of total agreements created
    uint256 public agreementCount = 0;

    // Events — like notifications that get logged on blockchain
    event AgreementStored(
        uint256 agreementId,
        string agreementHash,
        string tenantName,
        uint256 timestamp
    );

    event AgreementVerified(
        uint256 agreementId,
        bool isAuthentic
    );

    // -----------------------------------------------
    // FUNCTION 1: Store a new agreement hash
    // -----------------------------------------------
    function storeAgreement(
        string memory _agreementHash,
        string memory _landlordName,
        string memory _tenantName,
        string memory _propertyAddress,
        uint256 _rentAmount
    ) public returns (uint256) {
        
        // Increment counter to get new ID
        agreementCount++;
        
        // Store agreement details on blockchain
        agreements[agreementCount] = Agreement({
            agreementId: agreementCount,
            agreementHash: _agreementHash,
            landlordName: _landlordName,
            tenantName: _tenantName,
            propertyAddress: _propertyAddress,
            rentAmount: _rentAmount,
            timestamp: block.timestamp,
            isActive: true
        });

        // Emit event so it gets logged
        emit AgreementStored(
            agreementCount,
            _agreementHash,
            _tenantName,
            block.timestamp
        );

        return agreementCount;
    }

    // -----------------------------------------------
    // FUNCTION 2: Get agreement details by ID
    // -----------------------------------------------
    function getAgreement(uint256 _agreementId) 
        public view returns (
            uint256 id,
            string memory hash,
            string memory landlord,
            string memory tenant,
            string memory property,
            uint256 rent,
            uint256 timestamp,
            bool isActive
        ) 
    {
        Agreement memory a = agreements[_agreementId];
        return (
            a.agreementId,
            a.agreementHash,
            a.landlordName,
            a.tenantName,
            a.propertyAddress,
            a.rentAmount,
            a.timestamp,
            a.isActive
        );
    }

    // -----------------------------------------------
    // FUNCTION 3: Verify if agreement is authentic
    // -----------------------------------------------
    function verifyAgreement(
        uint256 _agreementId,
        string memory _hashToVerify
    ) public returns (bool) {
        
        Agreement memory a = agreements[_agreementId];
        
        // Compare stored hash with provided hash
        bool isAuthentic = keccak256(bytes(a.agreementHash)) == 
                           keccak256(bytes(_hashToVerify));

        // Log the verification attempt
        emit AgreementVerified(_agreementId, isAuthentic);

        return isAuthentic;
    }

    // -----------------------------------------------
    // FUNCTION 4: Get total number of agreements
    // -----------------------------------------------
    function getTotalAgreements() public view returns (uint256) {
        return agreementCount;
    }
}