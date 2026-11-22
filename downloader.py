import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd
from pyarrow import fs
from tqdm import tqdm

LOCAL_DATA_FOLDER = "data"
LOCAL_STOCK_FOLDER = f"{LOCAL_DATA_FOLDER}/csv"
STOCK_LIST_FILE = "./us_stock_list.csv"
REQUIRED_FIELDS = ["access_key", "secret_key", "endpoint", "folder"]

MAX_WORKERS = 6


logger = logging.getLogger(__name__)


class Downloader:
    def __init__(self, config: dict[str, str | None]):
        # check env variables
        for key in REQUIRED_FIELDS:
            value = config.get(key, None)
            if not value or len(value) == 0:
                raise ValueError(f"missing env variable: {key}")
            if key == "endpoint" and value.startswith("http"):
                raise ValueError(
                    "the http/https prefix should be excluded from the endpoint"
                )
        # check local stock list
        stock_list = pd.read_csv(STOCK_LIST_FILE)["symbol"].to_list()
        if len(stock_list) == 0:
            raise ValueError(
                "failed to load stock list, please check us_stock_list.csv file"
            )
        # initialize file system
        storage = fs.S3FileSystem(
            access_key=config["access_key"],
            secret_key=config["secret_key"],
            endpoint_override=config["endpoint"],
            scheme="https",
            region="auto",
        )
        self.stock_list = stock_list
        self.fs = storage
        self.endpoint = config["endpoint"]
        # ensure the folder exists
        self.remote_folder = config["folder"]
        self.local_folder = LOCAL_STOCK_FOLDER
        path = Path(self.local_folder)
        path.mkdir(parents=True, exist_ok=True)

    def download_single_stock(self, symbol: str):
        """
        read stock parquet file and save to local as csv
        """
        remote_file_path = f"{self.remote_folder}/{symbol}.parquet"
        local_file_path = f"{self.local_folder}/{symbol}.csv"
        df = pd.read_parquet(
            f"{remote_file_path}", engine="pyarrow", filesystem=self.fs
        )
        if "index" in df.columns:
            df = df.drop(columns=["index"])
        df.to_csv(f"{local_file_path}")

    def download_stocks(self):
        """
        download all stocks listed on the us_stock_list.csv
        """
        self._clear_path()
        stock_list = self.stock_list
        failed_tasks = []
        with (
            tqdm(total=len(stock_list), desc="downloading stocks") as progress_bar,
            ThreadPoolExecutor(
                max_workers=MAX_WORKERS, thread_name_prefix="download_stocks"
            ) as executor,
        ):
            futures = {
                executor.submit(self.download_single_stock, symbol): symbol
                for symbol in stock_list
            }
            for future in as_completed(futures):
                symbol = futures[future]
                try:
                    future.result()
                except Exception as exc:  # noqa: BLE001
                    failed_tasks.append(symbol)
                    logger.warning(f"failed to download data for {symbol}: {exc!s}")
                finally:
                    progress_bar.update()
        if len(failed_tasks) > 0:
            logger.warning(f"failed symbols: [{', '.join(failed_tasks)}]")

    def _clear_path(self):
        folder = Path(self.local_folder)
        for file in folder.glob("*.csv"):
            if file.is_file():
                file.unlink()
