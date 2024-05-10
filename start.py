import json
import os
import subprocess
import sys
from typing import List

import click

import constants


def prepare_xray_plugin() -> None:
    subprocess.Popen(
        [
            "wget",
            f"https://github.com/teddysun/xray-plugin/releases/download/{constants.XRAY_VERSION}/{constants.XRAY_ARCHIVE}",
        ]
    ).wait()
    subprocess.Popen(["tar", "-xvf", f"{constants.XRAY_ARCHIVE}"]).wait()
    subprocess.Popen(["rm", f"{constants.XRAY_ARCHIVE}"]).wait()
    subprocess.Popen(
        [
            "mv",
            "xray-plugin_linux_amd64",
            f"{constants.XRAY_NAME}",
        ]
    ).wait()


def prepare_v2ray_plugin() -> None:
    subprocess.Popen(
        [
            "wget",
            f"https://github.com/shadowsocks/v2ray-plugin/releases/download/{constants.V2RAY_VERSION}/{constants.V2RAY_ARCHIVE}",
        ]
    ).wait()
    subprocess.Popen(["tar", "-xvf", f"{constants.V2RAY_ARCHIVE}"]).wait()
    subprocess.Popen(["rm", f"{constants.V2RAY_ARCHIVE}"]).wait()
    subprocess.Popen(
        [
            "mv",
            "v2ray-plugin_linux_amd64",
            f"{constants.V2RAY_NAME}",
        ]
    ).wait()


def remove_old_docker_container() -> None:
    subprocess.Popen(["docker", "stop", f"{constants.DOCKER_CONTAINER_NAME}"]).wait()
    subprocess.Popen(["docker", "rm", f"{constants.DOCKER_CONTAINER_NAME}"]).wait()


def prepare_plugins() -> None:
    if not os.path.exists(f"{constants.V2RAY_NAME}"):
        prepare_v2ray_plugin()
    if not os.path.exists(f"{constants.XRAY_NAME}"):
        prepare_xray_plugin()


def check_ports_with_tls() -> List[int]:
    with open(f"{constants.CONFIG_FILE_NAME}") as file:
        ports_with_tls = []
        for server in json.load(file)["servers"]:
            if "tls" in server["plugin_opts"].split(";"):
                ports_with_tls.append(server["server_port"])
    return ports_with_tls


def generate_docker_port_mapping() -> List[str]:
    with open(constants.CONFIG_FILE_NAME) as file:
        ports = []
        for server in json.load(file)["servers"]:
            port = server["server_port"]
            ports.append(f"-p {port}:{port}/tcp -p {port}:{port}/udp")
    return " ".join(ports).split(" ")


def generate_tls_volumes_command():
    command = []
    if not os.path.exists(f"{constants.SSL_CERTIFICATE_PATH}") or not os.path.exists(
        f"{constants.SSL_CERTIFICATE_KEY_PATH}"
    ):
        ports_with_tls = check_ports_with_tls()
        if ports_with_tls:
            print(
                f"Ports {ports_with_tls} have tls option,"
                f" but SSL_CERTIFICATE_PATH or SSL_CERTIFICATE_KEY_PATH not specified. Remove tls option and try again"
            )
            sys.exit()
    else:
        subprocess.Popen(["chmod", "+r", constants.SSL_CERTIFICATE_PATH]).wait()
        subprocess.Popen(["chmod", "+r", constants.SSL_CERTIFICATE_KEY_PATH]).wait()

        command.extend(
            [
                "-v",
                f"{constants.SSL_CERTIFICATE_PATH}:{constants.SSL_CERTIFICATE_PATH}",
                "-v",
                f"{constants.SSL_CERTIFICATE_KEY_PATH}:{constants.SSL_CERTIFICATE_KEY_PATH}",
            ]
        )
    return command


def get_docker_run_command() -> List[str]:
    command = [
        "docker",
        "run",
        "--name",
        f"{constants.DOCKER_CONTAINER_NAME}",
        "--restart",
        "always",
        *generate_docker_port_mapping(),
        "-v",
        f"./{constants.V2RAY_NAME}:{constants.PLUGINS_PATH}/{constants.V2RAY_NAME}",
        "-v",
        f"./{constants.XRAY_NAME}:{constants.PLUGINS_PATH}/{constants.XRAY_NAME}",
        "-v",
        f"./{constants.CONFIG_FILE_NAME}:/etc/shadowsocks-rust/config.json",
        *generate_tls_volumes_command(),
        "-dit",
        constants.DOCKER_IMAGE,
    ]
    return command


@click.command()
def start() -> None:
    if not os.path.exists(constants.CONFIG_FILE_NAME):
        print(
            "Shadowsocks config not found. Run add_user command to add config and user"
        )
        sys.exit()
    remove_old_docker_container()
    prepare_plugins()
    subprocess.Popen(get_docker_run_command()).wait()
    print("Docker container started.")


if __name__ == "__main__":
    start()
