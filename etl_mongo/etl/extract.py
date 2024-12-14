from typing import List, Dict
from pandas import read_csv


class Extractor:

    @staticmethod
    def from_csv(file_path: str) -> List[Dict]:
        """Read CSV file

        Args:
            file_path (str): Path to CSV file location

        Returns:
            List[Dict]: Data from CSV file
        """

        data = read_csv(file_path).to_dict("records")
        return data
