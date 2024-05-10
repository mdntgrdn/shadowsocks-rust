import base64
import json
import os
import subprocess
import sys
from secrets import token_bytes

import click

import constants


def generate_key():
    return base64.b64encode(token_bytes(32)).decode()


def generate_base_config():
    if os.path.exists(constants.CONFIG_FILE_NAME):
        return
    with open(constants.CONFIG_FILE_NAME, "w") as file:
        json.dump(
            {
                "mode": "tcp_and_udp",
                "servers": [],
            },
            file,
            indent=4,
        )
    return


def build_plugins_config(mode: str, plugin: str, use_tls: bool):
    plugin_opts = f"server;mode={mode}"
    if use_tls:
        plugin_opts += (
            f";tls;key={constants.SSL_CERTIFICATE_KEY_PATH};"
            f"cert={constants.SSL_CERTIFICATE_PATH};host={constants.SERVER_DOMAIN_NAME}"
        )

    plugins_config = {
        "plugin": f"{plugin}",
        "plugin_opts": plugin_opts,
    }
    return plugins_config


def get_available_port() -> int:
    with open(constants.CONFIG_FILE_NAME) as file:
        available_servers = json.load(file)["servers"]
        if not bool(available_servers):
            return constants.INITIAL_PORT
        else:
            return available_servers[-1]["server_port"] + 1


def generate_base_server_config(description: str) -> dict:
    return {
        "server": "::",
        "server_port": get_available_port(),
        "password": generate_key(),
        "method": "aes-256-gcm",
        "_description": description,
    }


def validate_add_user_params(mode: str, plugin: str, use_tls: bool) -> bool:
    if plugin == constants.V2RAY_NAME and mode == constants.GRPC_MODE:
        print(f"V2Ray plugin does not support grpc mode")
        sys.exit()
    if use_tls:
        if not plugin:
            print(
                f"You should specify plugin ({constants.V2RAY_NAME} or {constants.XRAY_NAME}) to you tls"
            )
            sys.exit()
        if not constants.SSL_CERTIFICATE_PATH or not constants.SSL_CERTIFICATE_KEY_PATH:
            print(
                f"To enable tls option you should specify SSL_CERTIFICATE_PATH and SSL_CERTIFICATE_KEY_PATH"
            )
            sys.exit()
        if not os.path.exists(
            f"{constants.SSL_CERTIFICATE_PATH}"
        ) or not os.path.exists(f"{constants.SSL_CERTIFICATE_KEY_PATH}"):
            print(f"SSL_CERTIFICATE_PATH or SSL_CERTIFICATE_KEY_PATH paths not found")
        sys.exit()
    return True


@click.command()
@click.option(
    "--plugin",
    default=None,
    type=click.Choice([constants.XRAY_NAME, constants.V2RAY_NAME]),
    help=f"The name of the plugin ({constants.XRAY_NAME} or {constants.V2RAY_NAME})",
)
@click.option(
    "--mode",
    default=constants.WEBSOCKET_MODE,
    type=click.Choice([constants.WEBSOCKET_MODE, constants.GRPC_MODE]),
    help=f"Protocol of plugin ({constants.GRPC_MODE} or {constants.WEBSOCKET_MODE})",
)
@click.option(
    "--use-tls", default=False, type=click.BOOL, help=f"Should plugin use TLS or not"
)
@click.option(
    "--description",
    default="",
    help=f"User description",
)
def add_user(plugin: str, mode: str, use_tls: bool, description: str):
    validate_add_user_params(plugin=plugin, mode=mode, use_tls=use_tls)
    generate_base_config()
    server_config = generate_base_server_config(description)
    if plugin:
        server_config.update(build_plugins_config(mode, plugin, use_tls))
    with open(constants.CONFIG_FILE_NAME, "r") as file:
        current_config = json.load(file)
        current_config["servers"].append(server_config)
    with open(constants.CONFIG_FILE_NAME, "w") as file:
        json.dump(current_config, file, indent=4)
    print({"password": server_config["password"], "port": server_config["server_port"]})


if __name__ == "__main__":
    add_user()
