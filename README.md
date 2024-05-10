# Gettings Started

To start:
- pip install click
- apt install docker

# Scripts

## add_user 
Allow to automatically create new user. You should call "start" command after creation
  - arguments: 
    * --use-tls - Bool value. Should plugin use TLS or not
    * --plugin - The name of the plugin to use (xray-plugin or v2-ray-plugin)
    * --mode - The Protocol the plugin will use (websocket or grpc)
## delete_user
Allows to remove user by port
  - arguments:
    * --port: The port to delete
## start
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