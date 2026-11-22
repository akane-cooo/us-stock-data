import os

from dotenv import load_dotenv

from downloader import Downloader


def get_config():
    load_dotenv()
    config = {
        "endpoint": os.getenv("STORAGE_ENDPOINT"),
        "access_key": os.getenv("STORAGE_ACCESS_KEY_ID"),
        "secret_key": os.getenv("STORAGE_SECRET_ACCESS_KEY"),
        "folder": os.getenv("DATA_PATH"),
    }
    return config


def main():
    config = get_config()
    downloader = Downloader(config)
    downloader.download_stocks()


if __name__ == "__main__":
    main()
