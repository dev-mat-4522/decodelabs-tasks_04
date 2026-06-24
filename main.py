class ERC721Simulation:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
        
        # The Digital Architect: Value is a unique identity. 
        # mapping(uint256 => address) [cite: 409-410]
        self._owners = {}
        
        # Balances still tracked for UI purposes
        self._balances = {}
        
        # Off-Chain Metadata Pointer: mapping(uint256 => string)
        self._token_uris = {}
        
        self._next_token_id = 1

    # ==========================================
    # The Ledger of Truth: ownerOf [cite: 462]
    # ==========================================
    def owner_of(self, token_id):
        """Proves absolute ownership without requiring a trusted third party[cite: 479]."""
        owner = self._owners.get(token_id)
        
        # Validation Check: Is address 0x0? Yes -> revert [cite: 470-477]
        if not owner:
            raise ValueError(f"ERC721NonexistentToken: Token ID #{token_id} does not exist.")
            
        return owner

    # ==========================================
    # The Actuator: The Minting Engine [cite: 481]
    # ==========================================
    def safe_mint(self, to_address, token_uri):
        """Creates a new, permanent digital asset on the ledger[cite: 500]."""
        if not to_address or to_address == "0x0":
            raise ValueError("Invalid recipient address.")

        token_id = self._next_token_id
        self._next_token_id += 1

        # State Update: Map tokenId to 'to' address [cite: 489, 493]
        self._owners[token_id] = to_address
        
        # Balance Adjustment: Increment _balances[to] by 1 [cite: 491, 494]
        self._balances[to_address] = self._balances.get(to_address, 0) + 1
        
        # Link Metadata
        self._token_uris[token_id] = token_uri

        # Broadcast State: During a mint, the sender is the null address [cite: 518]
        self._emit_transfer_event("0x0000000000000000000000000000000000000000", to_address, token_id)
        
        return token_id

    def token_uri(self, token_id):
        """Returns the pointer to the off-chain JSON document[cite: 534, 541]."""
        self.owner_of(token_id) # Ensure token exists
        return self._token_uris.get(token_id)

    def _emit_transfer_event(self, sender, to, token_id):
        """
        Listeners (Marketplaces/Explorers) listen exclusively for these event logs 
        to update their user interfaces in real-time [cite: 521-522].
        """
        print(f"📡 [EVENT] Transfer(from: {sender}, to: {to}, tokenId: {token_id})")
        print(f"   ↳ This mathematical impossibility (minting from 0x0) signals token creation! [cite: 518-519]")


# ==========================================
# SYSTEM RUNNER: THE NFT LIFECYCLE
# ==========================================
if __name__ == "__main__":
    print("Initializing ERC-721 Engine...\n")
    
    nft_contract = ERC721Simulation("DecodeLabs Masterpiece", "DLM")
    user_wallet = "0xUser88888888888888888888888888888888888"
    
    # 1. IPFS Immutable Storage (Content-addressable) [cite: 578]
    # "Fetch the exact file that produces this specific hash." [cite: 579]
    ipfs_metadata_link = "ipfs://QmTy8w.../kitty57.json" 
    
    # 2. Execution Flow
    try:
        print("⚡ Triggering safeMint()...")
        minted_id = nft_contract.safe_mint(user_wallet, ipfs_metadata_link)
        
        print(f"\n✅ Asset Created! Token ID: {minted_id}")
        
        # 3. Validation
        print(f"🔍 Checking Ledger of Truth (ownerOf): {nft_contract.owner_of(minted_id)}")
        print(f"🔗 Resolving Metadata (tokenURI): {nft_contract.token_uri(minted_id)}")
        
        # 4. Threat Diagnostic
        print("\n🚨 Testing Unminted Token...")
        nft_contract.owner_of(999) # Will trigger ERC721NonexistentToken
        
    except ValueError as e:
        print(f"❌ Reverted: {e}")