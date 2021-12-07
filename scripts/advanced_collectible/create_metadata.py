import os
from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json
import os

breed_to_image_uri = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles")

    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )

        collectible_metadata = metadata_template

        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} exsits! Delete it to overwrite.")
        else:
            print(f"Creating metadata file: {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} pup!"
            print(collectible_metadata)

            # Upload image
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"

            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_ipfs(image_path)

            # If image uri exists, keep assigned as is, else look to breed mapping
            image_uri = image_uri if image_uri else breed_to_image_uri[breed]

            # Add image uri to metadata
            collectible_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)

            # upload metadata
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)


def upload_to_ipfs(filepath):
    # rb means open in binary
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()  # store image as binary.
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]

        # "./img/0-PUG.png" -> "0-PUG.png"
        # Split file into array and grab the last part, which should be {breed}.png
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri