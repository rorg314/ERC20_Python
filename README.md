# ERC20_PythonTemplate
This repository contains a python implementation of a simple blockchain/address/transaction structure that is loosely based on the ERC-20 protocol. I use this as a scaffolding for quickly prototyping ideas for new tokens. 

This does not implement a blockchain, but simply stores addresses and transactions in memory (that do not persist). In future I plan to create a simulated persistant blockchain for more in depth prototyping, but this template is simply meant to function as a test platform for minting and transacting tokens between addresses.  

- The file [erc20token.py](./erc20token.py) contains the class that defines an ERC-20 token and simulated addresses. 
- The file [main.py](./main.py) is used to initialise the token and create the desired amount of addresses.

# Installation

No packages are required, this is a very simple python program. 

# Set-Up 

## Deploying the token

In the file [main.py](./main.py), define the parameters of the ERC-20 token (passed as constructor arguments). These parameters are as follows:
- `name` : `str` : The name of the token e.g. Ethereum
- `symbol` : `str` : Token symbol (all caps) e.g ETH
- `decimals` : `int` : The maximum number of decimals used by the token (e.g BTC has 8 decimals)
- `quantaName` : `str` : The name used to refer to the smallest indivisible unit of the token (e.g 'Satoshi' for BTC)
- `totalSymbolSupply` : `int` : The total supply (in symbol values - e.g 21 million BTC)
- `addressLength` : `int` : Specified the length (number of hex characters) for address identifiers 

Upon construction, the token will create a single minter address (with address 000000... up to the specified addressLength) and allocate the total supply to the minter balance. 

## Creating Addresses

The function `CreateNWalletAddresses` can now be used to create the specified `number` of wallet addresses. Each wallet is assigned a random `addressId` (with the number of hex digits specified by the token). 

` NOTE: Address balances should always be stored as quantised amounts - i.e values in Satoshi not BTC ` 

Key points: 
- Each address is initialised with zero balance
- A list of all addresses (objects) is stored in the `ERC20Token` class
- Each address has a designated type ('wallet' or 'contract' - contracts are not yet implemented).

## Creating Transactions

Transactions are split into these stages 
1. Request transaction (unverified transaction created)
1. Transaction verified (simple implementation checks balance is sufficient - more complex verification possible at this stage (such as checking signed ownership of addresses))
1. Transaction performed if verified (balance transferred from sender to receiver)





