import click
import constants
from backups.yandex import YandexClient


@click.command()
@click.option(
    "--platform",
    default='yadisk',
    type=click.Choice([constants.YADISK_PLATFORM]),
    help=f"platform slug",
)
def backup(platform: str):
    if not (constants.YANDEX_CLIENT_ID and constants.YANDEX_CLIENT_SECRET):
        print("You must specify application client id and client secret")
    if platform == constants.YADISK_PLATFORM:
        YandexClient().download_config_from_yandex_disk()


if __name__ == "__main__":
    backup()
