# Gettings Started

To start:
- ```apt install docker```
- ```poetry install```
***

# Environment Variables
- ```DOCKER_IMAGE``` - base shadowsocks-rust docker image. default=ghcr.io/shadowsocks/ssserver-rust:v1.18.4
- ```V2RAY_VERSION``` - version of v2ray-plugin. default=v1.3.2
- ```XRAY_VERSION``` - version of xray-plugin. default=v1.8.11
- ```SERVER_DOMAIN_NAME``` - Domain name. Required when use tls. default=None
- ```SSL_CERTIFICATE_PATH``` - Path to SSL fullchain.pem file. Required when use tls. default=None
- ```SSL_CERTIFICATE_KEY_PATH``` - Path to SSL privkey.pem file. Required when use tls. default=None
## Yandex Backups

If you want to create backups to yandex disk on creation or deletion users, so follow next instructions of creating an app
https://yandex.com/dev/id/doc/en/register-client, keep in mind that redirect url must be https://oauth.yandex.ru/verification_code
- ```YANDEX_CLIENT_ID``` - Yandex Application ID
- ```YANDEX_CLIENT_SECRET``` - Yandex Application Client Secret
- ```YANDEX_DISK_FILE_PATH``` - Path to the yandex disk (default="/config.json")

To load default environment variables, add the next bash command at the end of the .bashrc file
```bash
export $(cat <<path>>/shadowsocks-rust/.env | grep -vE "^#" | xargs)
```
- path - path to the shadowsocks-rust folder
***

# Scripts

## add_user.py
Allow to automatically create new user. You should call "start" command after creation:
```bash
python3 add_user.py --plugin=v2ray-plugin --mode=websocket --description="My config" --use-tls=False
```
  - arguments: 
    * ```--use-tls``` - Bool value. Should plugin use TLS or not (default=False)
    * ```--plugin``` - The name of the plugin to use (xray-plugin, v2ray-plugin) (default=v2ray-plugin)
    * ```--mode``` - The Protocol the plugin will use (websocket or grpc) (default=websocket)
    * ```--description``` - User description (default="")
## delete_user.py
Allows to remove user by port:
```bash
python3 delete_user.py --port=8391
```
  - arguments:
    * ```--port```: The port to delete
## start.py
Start pre-configured docker container with shadowsocks-rust server:
```bash
python3 start.py
```
## backup_config.py
If backup is enabled and you would like to manually upload config.json file to the storage,
so you need to use this command
```bash
python3 backup_config.py 
```
## download_config.py
If you already have a config in supported storage you can download it through the next command
```bash
python3 download_config.py 
```
***

# Clients
## Android
client - https://github.com/shadowsocks/shadowsocks-android
plugin - https://github.com/shadowsocks/v2ray-plugin-android, https://github.com/teddysun/xray-plugin-android/releases/tag/v1.8.11

### IOS
client - https://apps.apple.com/us/app/shadowrocket/id932747118 \
v2ray-plugin included in the application.
If plugin is not required, you can use https://apps.apple.com/ru/app/potatso/id1239860606

### MacOS
client - https://github.com/shadowsocks/ShadowsocksX-NG
plugins - https://github.com/shadowsocks/v2ray-plugin, https://github.com/teddysun/xray-plugin

### Windows
coming soon