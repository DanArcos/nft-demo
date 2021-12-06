from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
import pytest
import time


def test_can_create_advanced_collectible_integration():
    # Deploy the contract
    # Create an NFT
    # Get a random breed back

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for Integration Testing")

    advanced_collectible, creation_transaction = deploy_and_create()

    time.sleep(60)

    # Assert
    assert advanced_collectible.tokenCounter() == 1
