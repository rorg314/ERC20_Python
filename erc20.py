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
        
        # List of all addresses
        self.allAddresses = list()

        # Dict of all address types -> list of all addresses of that type
        self.allAddressTypeDict = defaultdict(list)

        
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


    # ======================================================== #
    # ==================== ERC-20 PROTOCOL =================== #
    # ======================================================== #

    def Transfer(self, senderAddress, receiverAddress, quantisedAmount:int): 
        senderWallet = self.addressObjectDict[senderAddress]
        receiverWallet = self.addressObjectDict[receiverAddress]
        if(senderWallet.type != "Wallet" or receiverWallet.type != "Wallet"):
            print("Sender or Receiver was not a wallet! Sender type: " + senderWallet.type)
        

    
# Class defining a single address object
class Address():
    def __init__(self, token:ERC20Token, id, type, balance=0, contract=None):
        # Token using this address
        self.token = token
        
        # Address type string
        self.type = type
        # Address ID for this wallet
        self.Id = id
        # Address as string (format type_id)
        self.address = self.type + "_" + self.Id
        
        # Add the wallet to the addressObjectDict
        self.token.addressObjectDict[self.address] = self

        if(type == "Wallet"):
            # Token balance at this address
            self.balance = balance
            self.contract = None
        if(type == "Contract"):
            # Contract (method or class) at this address
            self.contract = contract
            self.balance = None

    def __repr__(self) -> str:
        return self.address





