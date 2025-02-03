import yfinance as yf
from dataclasses import dataclass
from pathlib import Path
import os


@dataclass
class DataFromYFinance:
    ticker: str
    unique_columns: str = "Datetime"

    def __post_init__(self):
        self.df = self.get_data_from_yfinance()
        self.store_file = Path(os.getenv("PROJECT_ROOT", Path(__file__).resolve().parents[4])) / "download" / f"{self.ticker}.csv"
        self.save()

    def get_data_from_yfinance(self):
        data = yf.download(self.ticker, period="1d", interval="1m")  # 1-day data, 1-minute interval
        return data

    def save(self):
        self.df.columns = self.df.columns.get_level_values(0)
        self.df.to_csv(self.store_file)



if __name__ == "__main__":
    hest = DataFromYFinance("AAPL")