from collections import defaultdict
import string
import random






class ERC20Token():
    def __init__(self, name, symbol, decimals=18, quanta='_wei', totalSupply=0, addressLength=8):
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
        # Address will be hex string of length addressLength 
        self.addressLength = addressLength

        # List of all created addresses
        self.allAddresses = list()

        # Dict of address string -> address object
        self.allAddressDict = defaultdict(list)

        
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
    def __init__(self, token:ERC20Token, address, type, balance=0, contract=None):
        # Token using this address
        self.token = token
        
        # Address type string
        self.type = type
        # Address ID (hex string with token.addressLength #characters)
        self.id = address
        # Address as string (format type_id)
        self.addressStr = self.type + "_" + self.id
        
        # Add this address object to the allAddressDict
        self.token.allAddressDict[self.id] = self

        if(type == "Wallet"):
            # Token balance at this address
            self.balance = balance
            self.contract = None
        if(type == "Contract"):
            # Contract (method or class) at this address
            self.contract = contract
            self.balance = None

    def __repr__(self) -> str:
        return self.addressStr





# ======================================================== #
# ==================== HELPER METHODS ==================== #
# ======================================================== #


# Used to generate random address IDs 
def GenerateRandomAddressID(token:ERC20Token):
    id = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(token.address))
    # Ensure id has not already been created
    if(id in token.allAddresses):
        # Generate a new random address
        GenerateRandomAddressID(token)
    else:
        return id

