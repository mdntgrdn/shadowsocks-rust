import sys

import click
import constants
import json


@click.command()
@click.option(
    "--port",
    type=click.INT,
    help=f"User port to remove",
)
def remove_user(port: int):
    with open(f"{constants.CONFIG_FILE_NAME}", "r") as file:
        current_config = json.load(file)
        for i, conf in enumerate(current_config["servers"]):
            if conf["server_port"] == port:
                current_config["servers"].pop(i)
                break
        else:
            print(f"User port {port} does not exist")
            sys.exit()
    with open(f"{constants.CONFIG_FILE_NAME}", "w") as file:
        json.dump(current_config, file)
        print(f"Port {port} has been removed")


if __name__ == "__main__":
    remove_user()
