import os
import json

import yadisk
import webbrowser
import constants

TOKEN_FILE = 'tokens.json'


class YandexClient:

    def __init__(self):
        self.access_token, self.refresh_token = self.load_tokens()
        self.yandex_client = yadisk.YaDisk(
            id=constants.YANDEX_CLIENT_ID,
            secret=constants.YANDEX_CLIENT_SECRET,
            token=self.access_token
        )

    def save_tokens(self, access_token, refresh_token):
        tokens = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        self.yandex_client.token = access_token
        self.access_token = access_token
        self.refresh_token = refresh_token
        with open(TOKEN_FILE, 'w') as f:
            json.dump(tokens, f)

    def load_tokens(self):
        try:
            with open(TOKEN_FILE, 'r') as f:
                tokens = json.load(f)
            return tokens['access_token'], tokens['refresh_token']
        except FileNotFoundError:
            return None, None

    def refresh_tokens(self):
        result = self.yandex_client.refresh_token(self.refresh_token)
        self.save_tokens(result.access_token, result.refresh_token)

    def request_tokens(self):
        result = self.yandex_client.get_token(self.initial_authorize())
        self.save_tokens(result.access_token, result.refresh_token)

    def check_and_refresh_token(self):
        try:
            if not self.yandex_client.check_token():
                if not self.refresh_token:
                    self.request_tokens()
                else:
                    self.refresh_tokens()
        except (yadisk.exceptions.UnauthorizedError, yadisk.exceptions.InvalidGrantError):
            self.request_tokens()

    def initial_authorize(self):
        REDIRECT_URI = 'https://oauth.yandex.ru/verification_code'

        # Создаем URL для авторизации
        auth_url = (f'https://oauth.yandex.ru/authorize?response_type=code&client_id='
                    f'{constants.YANDEX_CLIENT_ID}&redirect_uri={REDIRECT_URI}')

        # Открываем URL в браузере
        print("Open the next link in browser and authorize.")
        print(auth_url)
        webbrowser.open(auth_url)
        return input("Input code from browser here: ")

    def upload_file_to_yandex_disk(self):
        if not os.path.exists('config.json'):
            print("No config.json file found.")
        self.check_and_refresh_token()  # Обновляем токен, если истек
        try:
            try:
                self.yandex_client.mkdir('/shadowsocks')
            except yadisk.exceptions.DirectoryExistsError:
                pass
            self.yandex_client.upload('config.json', constants.YANDEX_DISK_FILE_PATH, overwrite=True)
            print("File uploaded successfully")
        except yadisk.exceptions.UnauthorizedError:
            print("Unauthorized access. Check your token.")
        except Exception as e:
            print(f"Failed to upload file. Error: {e}")

    def download_config_from_yandex_disk(self):
        if os.path.exists('config.json'):
            print("You already have a config, to download new one delete existing.")
        self.yandex_client.download(constants.YANDEX_DISK_FILE_PATH, 'config.json', overwrite=True)


if __name__ == '__main__':
    YandexClient().upload_file_to_yandex_disk()
