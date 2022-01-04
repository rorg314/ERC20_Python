from collections import defaultdict




# Format of address GUID 
#   - incremental = incremental integers
#   - random8 = random 8 digit integer
ADDRESS_ID_FORMATS = ["incremental", "random8"]

class ERC20Token():
    def __init__(self, name, symbol, decimals=18, quanta='_wei', totalSupply=0, addressIdFormat='incremental'):
        # Token name
        self.name = name
        # Token symbol
        self.symbol = symbol
        
        # Total token supply
        self.totalSupply = totalSupply


        # --------- QUANTA --------- #
        # Defines token quanta (smallest individual unit - e.g satoshis or wei)

        # Token quanta name
        self.quanta = quanta
        # Number of token decimals 
        self.decimals = decimals


        # -------- ADDRESSES ------- #
        # Address ID will be of the form type_id
        # Eg wallet_21439 is the address for the wallet with GUID 21439
        # Eg contract_21 is the contract with GUID 21 

        # Address identifier format
        self.addressIdFormat = addressIdFormat
        
        # Dict of all address types -> list of all addresses
        self.allAddresses = defaultdict(list)

        
    # ======================================================== #
    # ===================== TOKEN METHODS ==================== #
    # ======================================================== #

    # --- QUANTA CONVERSIONS --- #

    # Convert a symbol amount into quanta (eg 1BTC = 100,000,000 Satoshi) 
    def GetQuantisedAmount(self, symbolAmount):
        return symbolAmount * (10**self.decimals)
    
    # Convert quanta amount to symbol amount (eg 1 Satoshi = 0.00000001 BTC)
    def GetSymbolAmount(self, quantaAmount):
        return quantaAmount * 10 ** (-self.decimals)

    

# Class defining a single wallet address
class WalletAddress():
    def __init__(self, token:ERC20Token, Id, balance=0):
        # Token held at in this wallet
        self.token = token
        
        # Address type string
        self.type = "Wallet"
        # Address ID for this wallet
        self.Id = Id
        # Address as string (format type_id)
        self.address = self.type + "_" + self.Id
        
        # Token balance at this address
        self.balance = balance
