from collections import defaultdict
import string
import random





# Class that defines an ERC-20 token. Holds all addresses for this token
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

        # --------- MINTER --------- #
        # Create minter address (addressId = 000000000...0)
        self.minter = Address(self, f"{'0'*self.addressLength}", "wallet")
        # Init minter with starting total supply
        self.minter.balance = self.totalSupply

        
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
        # Get the address objects for sender and receiver
        try:
            sender = GetAddressObject(self, senderAddress)
            receiver = GetAddressObject(self, senderAddress)
            # Ensure both addresses are wallets
            if(sender.type.lower().strip() != "wallet" or receiver.type.lower().strip() != "wallet"):
                print("Sender or Receiver was not a wallet, aborting! \n Sender type: " + sender.type + "\n Receiver type: " + receiver.type)
                return
        except:
            print("Could not get address objects! \n Sender: " + senderAddress + "\nReceiver: " + receiverAddress)
        
        # Perform the transfer
        sender.balance -= quantisedAmount
        receiver.balance += quantisedAmount
        

    
# Class defining a single address object
class Address():
    def __init__(self, token:ERC20Token, addressId, type, contract=None, initBalance=0):
        # Token using this address
        self.token = token
        
        # Address type string
        self.type = type
        # Address ID (hex string with token.addressLength #characters)
        self.id = addressId
        # Address as string (format type_id)
        self.addressStr = self.type + "_" + self.id
        
        # Add this address object to the allAddressDict
        self.token.allAddressDict[self.id] = self
        
        # Init address with zero balance
        # Unless explicitly stated - all balance amounts are in quantised units
        if(initBalance == 0):
            self.balance = 0
        else:
            token.Transfer(token.minter, self, initBalance)

        # If this address contains a contract (otherwise contract=None)
        self.contract = contract

    def __repr__(self) -> str:
        return self.addressStr


# ======================================================== #
# ==================== HELPER METHODS ==================== #
# ======================================================== #


# Get the address object corresponding to the given address ID 
def GetAddressObject(token:ERC20Token, address:str or Address):
    if(isinstance(address, Address)):
        return address
    if(isinstance(address, str)):
        try:
            return token.allAddressDict[address]
        except:
            print("Address could not be found! " + address)
            return None


# Used to generate random address IDs 
def GenerateRandomAddressID(token:ERC20Token):
    id = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(token.address))
    # Ensure id has not already been created
    if(id in token.allAddresses):
        # Generate a new random address
        GenerateRandomAddressID(token)
    else:
        return id

