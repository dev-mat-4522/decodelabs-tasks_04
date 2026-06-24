// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// Structural Schematic Dependencies [cite: 456]
import '@openzeppelin/contracts/token/ERC721/ERC721.sol';
import '@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol';
import '@openzeppelin/contracts/access/Ownable.sol';

contract IotaEVMSampleNFT is ERC721, ERC721URIStorage, Ownable {
    uint256 private _nextTokenId;

    // Constructor initializes the token name and symbol, and sets the deployer as owner [cite: 459]
    constructor() ERC721('IotaEVMSampleNFT', 'SNFT') Ownable(msg.sender) {}

    // Structural Schematic: safeMint [cite: 501-506]
    // The Ownable modifier ensures only the admin can trigger the minting engine
    function safeMint(address to, string memory uri) public onlyOwner {
        uint256 tokenId = _nextTokenId++;
        
        // _safeMint actively queries the receiving contract to ensure it can handle NFTs [cite: 511-512]
        _safeMint(to, tokenId);
        
        // _setTokenURI links the on-chain token to the off-chain JSON metadata [cite: 506]
        _setTokenURI(tokenId, uri);
    }

    // Boilerplate overrides required by Solidity when inheriting from multiple OpenZeppelin contracts
    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}