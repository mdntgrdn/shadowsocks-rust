import os
import dotenv


dotenv.load_dotenv('.env')


# Docker
DOCKER_IMAGE = os.environ["DOCKER_IMAGE"]
DOCKER_CONTAINER_NAME = "shadowsocks-rust"

# Config
CONFIG_FILE_NAME = "config.json"
INITIAL_PORT = 8388

# SSL/TLS
SERVER_DOMAIN_NAME = os.environ.get("SERVER_DOMAIN_NAME", "")
SSL_CERTIFICATE_PATH = os.environ.get("SSL_CERTIFICATE_PATH", "")
SSL_CERTIFICATE_KEY_PATH = os.environ.get("SSL_CERTIFICATE_KEY_PATH", "")


# PLUGINS SECTION
PLUGINS_PATH = "/usr/local/bin"

V2RAY_NAME = "v2ray-plugin"
V2RAY_VERSION = os.environ["V2RAY_VERSION"]
V2RAY_ARCHIVE = f"v2ray-plugin-linux-amd64-{V2RAY_VERSION}.tar.gz"

XRAY_NAME = "xray-plugin"
XRAY_VERSION = os.environ["XRAY_VERSION"]
XRAY_ARCHIVE = f"xray-plugin-linux-amd64-{XRAY_VERSION}.tar.gz"

WEBSOCKET_MODE = "websocket"
GRPC_MODE = "grpc"


# Backups

# Yandex
YADISK_PLATFORM = "yadisk"
YANDEX_CLIENT_ID = os.environ.get("YANDEX_CLIENT_ID", None)
YANDEX_CLIENT_SECRET = os.environ.get("YANDEX_CLIENT_SECRET", None)
YANDEX_DISK_FILE_PATH = os.environ.get("YANDEX_DISK_FILE_PATH", None)