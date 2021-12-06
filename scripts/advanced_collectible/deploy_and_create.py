from scripts.helpful_scripts import get_account, OPENSEA_URL, get_contract
from brownie import AdvancedCollectible, network, config
from web3 import Web3


def main():
    deploy_and_create()


def deploy_and_create():
    account = get_account()
    # Open sea test net only works with Rinkeby at the mopment
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
    )

    # Fund the contract with link
    fund_with_link(advanced_collectible.address)

    creating_tx = advanced_collectible.createCollectible({"from": account})
    creating_tx.wait(1)
    print(f"New token has been created")
    return advanced_collectible, creating_tx


def fund_with_link(
    contract_address, account=None, link_token=None, amount=Web3.toWei(1, "ether")
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    funding_tx = link_token.transfer(contract_address, amount, {"from": account})
    funding_tx.wait(1)
    print(f"Funded {contract_address}")
    return funding_tx
