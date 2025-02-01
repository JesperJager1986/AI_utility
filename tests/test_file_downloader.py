import unittest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
import sys
import os

# Ensure the parent directory is in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from AI_utility.src.download.FileDownLoader import FileDownloader

class TestFileDownloader(unittest.TestCase):

    def setUp(self):
        """Initialize test variables."""
        self.url = "https://example.com/test.csv"
        self.default_store_path = Path("download/test.csv")

    def test_init(self):
        """Test initialization of FileDownloader."""
        downloader = FileDownloader(self.url)
        self.assertEqual(downloader.path, self.url)
        self.assertEqual(downloader.store_file, self.default_store_path)

    @patch("os.makedirs")
    def test_create_folder(self, mock_makedirs):
        """Test folder creation."""
        downloader = FileDownloader(self.url)
        downloader.create_folder()
        mock_makedirs.assert_called_once_with(self.default_store_path.parent, exist_ok=True)

    @patch("requests.get")
    @patch("builtins.open", new_callable=mock_open)
    def test_download_success(self, mock_open, mock_requests_get):
        """Test successful download."""
        mock_requests_get.return_value = MagicMock(status_code=200, content=b"Fake Data")

        downloader = FileDownloader(self.url)
        result = downloader.download()

        mock_requests_get.assert_called_once_with(self.url)
        mock_open.assert_called_once_with(self.default_store_path, "wb")
        self.assertTrue(result)

    @patch("requests.get")
    def test_download_failure(self, mock_requests_get):
        """Test failed download (404)."""
        mock_requests_get.return_value = MagicMock(status_code=404)

        downloader = FileDownloader(self.url)
        result = downloader.download()

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
