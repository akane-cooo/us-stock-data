import argparse
import os

from dotenv import load_dotenv

from downloader import Downloader
from dump import DumpDataAll


def get_config():
    load_dotenv()
    config = {
        "endpoint": os.getenv("STORAGE_ENDPOINT"),
        "access_key": os.getenv("STORAGE_ACCESS_KEY_ID"),
        "secret_key": os.getenv("STORAGE_SECRET_ACCESS_KEY"),
        "folder": os.getenv("DATA_PATH"),
        "local_path": os.getenv("LOCAL_PATH"),
    }
    return config


def main(*, mode: str = "all"):
    if mode not in ["all", "download, dump"]:
        raise ValueError(f"Invalid mode: {mode}")
    config = get_config()
    if mode in ("all", "download"):
        downloader = Downloader(config)
        downloader.download_stocks()
    if mode in ("all", "dump"):
        dumper = DumpDataAll(
            data_path=f"{config['local_path']}/csv",
            qlib_dir=f"{config['local_path']}/us_stock",
            date_field_name="date",
            symbol_field_name="symbol",
            include_fields="open,high,low,close,volume,vwap,factor",
            file_suffix=".csv",
            freq="day",
        )
        dumper.dump()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "download", "dump"), default="all")
    main()
