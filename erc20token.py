from collections import defaultdict
import string
import random
import time
import datetime





# Class that defines an ERC-20 token. Holds all addresses for this token
class ERC20Token():
    """
        Description:
        ------------
        Paragraph describing the method. 
        Elaborate inputs, functionality and outputs.
        
        \_\_init\_\_(): Args:
        ------ 
            
            name : str 
                -- Name of the token
            symbol : str
                -- Token name abbreviation e.g. 'BTC'
            
            
        Kwargs:
        -------
        ```python
        decimals : int : default = 18 
            -- Decimal point accuracy of the currency 
                (e.g BTC= 8 decimals, ETH = 18 decimals)
        
        quanta : str : default = 'qnta'
            -- The name of the smallest indivisible currency unit 
                (e.g BTC quanta = Satoshi, ETH quanta = Wei )
        
        totalSymbolSupply : int : default = 10e9
            -- The total supply in token symbol units e.g 21 million BTC
        
        addressLength : int : default = 16
            -- The length of unique address identifiers (number of hex digits)
                (Note: transactions Ids will have length addressLength + 4)
        ```
                
                    
            
        
        Class Members:
        --------------

        ### Addresses:
        ```python
        allAddresses : list[Address]
            -- List of all Address objects that have been created for this token
        allAddressDict : dict[addressId:str] = addressObject : Address
            -- Dict of addressId -> addressObject 
        minter : Address
            -- The address of the minter - has Id with zero 00000... up to the addressLength
                Upon construction of the token the minter address initialises its balance with the total supply

        ```
        
        
        Notes:    
        ------
        Unless explicitly stated, wallet addresses and transaction quantities are stored in quantised units. The class methods GetQuantisedAmount and GetSymbolAmount should be used where appropriate.

    """
    
    
    def __init__(self, name, symbol, decimals=18, quanta='qnta', totalSymbolSupply=10e9, addressLength=16):
        # Token name
        self.name = name
        # Token symbol
        self.symbol = symbol
        
        
        # --------- QUANTA --------- #
        # Defines token quanta (smallest individual unit - e.g satoshis or wei)

        # Token quanta name
        self.quanta = quanta
        # Number of token decimals 
        self.decimals = decimals

        # --------- TOTAL SUPPLY --------- #
        
        # Total token supply
        self.totalSymbolSupply = totalSymbolSupply

        # Total quantised supply
        self.totalQuantisedSupply = self.GetQuantisedAmount(totalSymbolSupply)

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
        self.minter.balance = self.GetQuantisedAmount(self.totalSymbolSupply)

        # ------ TRANSACTIONS ------ #
        # Ensure transaction Id length is separate from address length
        self.transactionIdLength = addressLength + 4

        # List of all transactions
        self.allTransactions = list()

        # Dict of transactionId -> transaction
        self.transactionIdDict = dict()

        
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
        
        # Add to list of all addresses
        self.token.allAddresses.append(self)
        # Add this address object to the allAddressDict
        self.token.allAddressDict[self.id] = self
        
        # Init address with zero balance
        # Unless explicitly stated - all balance amounts are in quantised units
        if(initBalance == 0):
            self.balance = 0
        else:
            RequestTransaction(token.minter, self, initBalance)

        # If this address contains a contract (otherwise contract=None)
        self.contract = contract

    def __repr__(self) -> str:
        return self.addressStr

# Class defining a single transaction (these are effectively the blocks) - everything must be hashable  
class Transaction():
    def __init__(self, token:ERC20Token, sender:Address, receiver:Address, qntAmount):
        # Generate a random transaction ID
        self.transactionId = GenerateRandomTransactionID(token)
        # Sender and receiver addresses
        self.senderAddressId = sender.id
        self.receiverAddressId = receiver.id
        
        # Sender and receiver initial balances
        self.senderInitBalance = sender.balance
        self.receiverInitBalanace = receiver.balance
        
        # Requested transacted amount (quantised units)
        self.transactedQntAmount = qntAmount
        # Transacted amount (symbol units)
        self.transactedSymAmount = token.GetSymbolAmount(qntAmount)
        # Strings for quantised and symbol amounts 
        self.symbol = token.symbol
        self.quanta = token.quanta
    
        
        # Transaction timestamp
        self.transactionTimeUnix = time.time()
        self.timestamp = datetime.datetime.utcfromtimestamp(self.transactionTimeUnix).strftime('%Y-%m-%d %H:%M:%S')

        # Has transaction been verified yet?
        self.verified = False

    def __repr__(self) -> str:
        return "Transaction: " + str(self.transactionId) + " ----- Amount: " + str(self.transactedSymAmount) + " " + self.symbol + " ----- Time: " + str(self.timestamp)



# ======================================================== #
# ==================== ERC-20 PROTOCOL =================== #
# ======================================================== #

def RequestTransaction(token:ERC20Token, senderAddress, receiverAddress, quantisedAmount:int):
    # Get the address objects for sender and receiver
    
    try:
        sender = GetWalletFromAddress(token, senderAddress)
        receiver = GetWalletFromAddress(token, receiverAddress)
        
    except:
        print("Could not get address objects! \n Sender: " + str(senderAddress) + "\nReceiver: " + str(receiverAddress))
        return 

    try: 
        # Create the unverified transaction
        transaction = Transaction(token, sender, receiver, quantisedAmount)
        # Send the transaction for verification
        VerifyTransaction(token, transaction)
    except:
        print("Could not create the transaction!\n Sender: " + str(senderAddress) + "\nReceiver: " + str(receiverAddress) )
    


# Verify the requested transaction - simple implementation here checks if sender has enough balance - more complex implementations possible eg checking sender signed messages to prove wallet ownership 
def VerifyTransaction(token:ERC20Token, transaction:Transaction):
    if(transaction.senderInitBalance > transaction.transactedQntAmount):
        transaction.verified = True
        print("Verified transaction: \n" + str(transaction))
        DoTransaction(token, transaction)
        
    else:
        print("Could not verify transaction!" + str(transaction))

    
# Perform the transaction
def DoTransaction(token:ERC20Token, transaction:Transaction): 
    # Get the address objects for sender and receiver
    try:
        #sender = GetWalletFromAddress(transaction.senderAddressId)
        #receiver = GetWalletFromAddress(transaction.receiverAddressId)
        token.allAddressDict[transaction.senderAddressId].balance = transaction.senderInitBalance - transaction.transactedQntAmount
        token.allAddressDict[transaction.receiverAddressId].balance = transaction.receiverInitBalanace + transaction.transactedQntAmount
        
    except:
        print("Could not get address objects! \n Sender: " + transaction.senderAddressId + "\nReceiver: " + transaction.senderAddressId)
    
    # Perform the transaction
    #sender.balance -= transaction.transactedQntAmount
    #receiver.balance += transaction.transactedQntAmount

    print("Completed transaction: \n" + str(transaction))


# ======================================================== #
# ==================== HELPER METHODS ==================== #
# ======================================================== #


# Get the address object corresponding to the given address ID 
def GetAddressObject(token:ERC20Token, addressId:str or Address):
    # Check if already an address
    if(isinstance(addressId, Address)):
        return addressId
    # Ensure addressId str contains no prefix of address type
    if('_' in addressId):
        addressId = addressId.split("_")[-1]
    
    if(isinstance(addressId, str)):
        try:
            return token.allAddressDict[addressId]
        except:
            print("Address could not be found! " + addressId)
            return None


def GetWalletFromAddress(token, address):
    # Get the address objects for sender and receiver
    try:
        addressObject = GetAddressObject(token, address)
        
        # Ensure address object is of type "wallet" 
        if(addressObject.type.lower().strip() != "wallet"):
            print("Address was not a wallet, aborting! \n Address type: " + addressObject.type)
            return None
        # Return the wallet (address object)
        return addressObject
    except:
        print("Could not get address object! \n Address: " + addressObject)
        return None


# Used to generate random address IDs 
def GenerateRandomAddressID(token:ERC20Token):
    id = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(token.addressLength))
    # Ensure id has not already been created
    if(id in list(token.allAddressDict.keys())):
        # Generate a new random address
        GenerateRandomAddressID(token)
    else:
        return id


# Used to generate random transaction IDs 
def GenerateRandomTransactionID(token:ERC20Token):
    id = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(token.transactionIdLength))
    # Ensure id has not already been created
    if(id in token.allTransactions):
        # Generate a new random ID
        GenerateRandomTransactionID(token)
    else:
        return id





