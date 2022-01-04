from erc20token import *


def main():
    print("Main")

    # Create the ERC-20 token model
    token = ERC20Token("token", "TKN", decimals=8, quanta="qt", totalSupply=1e9, addressLength=8)



    print("Done")



def CreateWalletAddresses(token:ERC20Token, number):
    for N in range(number):
        # Create a new address (inits with zero balance)
        Address(token, GenerateRandomAddressID(), "wallet")


if __name__ == "__main__":
    main()