from time import process_time

import requests
from dataclasses import dataclass, field
from pathlib import Path
import os



@dataclass()
class FileDownloader:
    path: str
    store_file: Path | None = field(init=False) # Todo find better reference method to root

    def __post_init__(self):
        self.store_file = Path(os.getenv("PROJECT_ROOT", Path(__file__).resolve().parents[4])) / "download" / Path(self.path).name
        self.create_folder()
        self.download()

    def create_folder(self):
        os.makedirs(str(self.store_file.parent), exist_ok=True)

    def download(self):
        response = requests.get(self.path)
        if response.status_code == 200:
            with open(str(self.store_file), "wb") as file:
                file.write(response.content)
            print(f"File downloaded successfully: {self.store_file}")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")

    @property
    def store_path(self) -> Path:
        return self.store_file



if __name__ == "__main__":


    url = "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_gl.csv"

    loader = FileDownloader(url)
