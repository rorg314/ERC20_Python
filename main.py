from erc20token import *


def main():
    print("Main")

    # Create the ERC-20 token model
    token = ERC20Token("token", "TKN", decimals=8, quanta="qt", totalSymbolSupply=1e9, addressLength=8)

    CreateNumWalletAddresses(token, 5)

    RequestTransaction(token, token.minter, token.allAddresses[1], 100)

    print("Done")



def CreateNumWalletAddresses(token:ERC20Token, number):
    for N in range(number):
        # Create a new address (inits with zero balance)
        Address(token, GenerateRandomAddressID(token), "wallet")


if __name__ == "__main__":
    main()