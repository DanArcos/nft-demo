from brownie import AdvancedCollectible
from scripts.helpful_scripts import get_account
from scripts.advanced_collectible.deploy_and_create import fund_with_link
from web3 import Web3


"""
Here we can create a collectible. We don't have to deploy a new contract since we can work off of that which has been most recently deployed. 
"""


def main():
    # Get account
    account = get_account()

    # Get most recent deployment of advanced collectible
    advanced_collectible = AdvancedCollectible[-1]

    # Fund with link
    fund_with_link(advanced_collectible.address, amount=Web3.toWei(0.1, "ether"))

    # Create the transaction
    creation_transaction = advanced_collectible.createCollectible({"from": account})
    creation_transaction.wait(1)
    print("Collectible Created")
