from typing import List, Dict


class Transformer:

    @staticmethod
    def clean_data(data: List[Dict]) -> List[Dict]:
        """Transform the data

        Args:
            data (List[Dict]): The CSV file data

        Returns:
            List[Dict]: CSV data transformed
        """

        for k, v in enumerate(data):
            data[k]["name"] = v["name"].title()
            data[k]["age"] = int(v["age"])
            data[k]["city"] = v["city"].title()
        return data
