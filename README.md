# Gettings Started

To start:
- ```pip install click```
- ```apt install docker```
***

# Environment Variables
- ```DOCKER_IMAGE``` - base shadowsocks-rust docker image. default=ghcr.io/shadowsocks/ssserver-rust:latest
- ```V2RAY_VERSION``` - version of v2ray-plugin. default=v1.3.2
- ```XRAY_VERSION``` - version of xray-plugin. default=v1.8.11
- ```SERVER_DOMAIN_NAME``` - Domain name. Required when use tls. default=None
- ```SSL_CERTIFICATE_PATH``` - Path to SSL fullchain.pem file. Required when use tls. default=None
- ```SSL_CERTIFICATE_KEY_PATH``` - Path to SSL privkey.pem file. Required when use tls. default=None
***

# Scripts

## add_user.py
Allow to automatically create new user. You should call "start" command after creation
  - arguments: 
    * ```--use-tls``` - Bool value. Should plugin use TLS or not
    * ```--plugin``` - The name of the plugin to use (xray-plugin or v2-ray-plugin)
    * ```--mode``` - The Protocol the plugin will use (websocket or grpc)
## delete_user.py
Allows to remove user by port
  - arguments:
    * ```--port```: The port to delete
## start.py
Start pre-configured docker container with shadowsocks-rust server
***

# Clients
## Android
client - https://github.com/shadowsocks/shadowsocks-android
plugin - https://github.com/shadowsocks/v2ray-plugin-android

### IOS
client - https://apps.apple.com/us/app/shadowrocket/id932747118 \
v2ray-plugin included in the application. It also supports xray-plugin
If plugin is not required, you can use https://apps.apple.com/ru/app/potatso/id1239860606

### MacOS
client - https://github.com/shadowsocks/ShadowsocksX-NG
plugins - https://github.com/shadowsocks/v2ray-plugin, https://github.com/teddysun/xray-plugin

### Windows
coming soon