import requests


class Locations:
    """A class used to retrieve the IATA code for specific locations from the Kiwi API."""

    def __init__(self, api_key):
        """
        Initialize the Locations class.
        
        Parameters:
        - api_key (str): The API key used to authenticate with the Kiwi API.
        """
        self.api_key = api_key
        self.endpoint = "https://tequila-api.kiwi.com/locations/query"

    def get_iata_code(self, location):
        """
        Retrieve the IATA code for the specified location.
        
        Parameters:
        - location (str): The name of the location for which the IATA code is required.

        Returns:
        - str: The IATA code of the location if found.
        - None: If the IATA code for the location is not found.
        """
        headers = {
            "apikey": self.api_key,
        }
        params = {
            "term": location,
        }
        response = requests.get(self.endpoint, params=params, headers=headers)
        data = response.json()
        if "locations" in data and len(data["locations"]) > 0:
            return data["locations"][0]["code"]
        else:
            return None
