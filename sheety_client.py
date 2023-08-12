import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

load_dotenv()


class SheetyClient:
    """A class used to interact with the Sheety API for various operations."""

    def __init__(self):
        """
        Initialize the SheetyClient class.
        """
        self.sheety_deals_endpoint = "https://api.sheety.co/ae30d62180f467f989768c95d8b5229f/pythonFlightDeals/prices"
        self.sheety_users_endpoint = "https://api.sheety.co/ae30d62180f467f989768c95d8b5229f/pythonFlightDeals/users"

        # Load sensitive information from .env file
        SHEETY_USERNAME = os.getenv("SHEETY_USERNAME")
        SHEETY_PASSWORD = os.getenv("SHEETY_PASSWORD")
        self.basic_auth = HTTPBasicAuth(SHEETY_USERNAME, SHEETY_PASSWORD)

    def get_city_data(self):
        """
        Retrieve data for all cities from the Sheety API.

        Returns:
        - dict: A dictionary containing data for all cities.
        """
        sheety_request = requests.get(self.sheety_deals_endpoint, auth=self.basic_auth)
        sheety_data = sheety_request.json()
        return sheety_data

    def update_city_data(self, city_id, iata_code):
        """
        Update the IATA code for a specific city in the Sheety API.
        
        Parameters:
        - city_id (int): The ID of the city to be updated.
        - iata_code (str): The IATA code for the city.

        Returns:
        - dict: A dictionary containing the updated data for the city.
        """
        update_url = f"{self.sheety_deals_endpoint}/{city_id}"
        iata_code_data = {
            "price": {"iataCode": iata_code}
        }
        sheety_update = requests.put(update_url, json=iata_code_data, auth=self.basic_auth)
        return sheety_update.json()

    def add_user(self, FIRST, LAST, EMAIL):
        """
        Add a new user to the Sheety API.
        
        Parameters:
        - FIRST (str): The first name of the user.
        - LAST (str): The last name of the user.
        - EMAIL (str): The email of the user.

        Returns:
        - dict: A dictionary containing data for the added user.
        """
        user_data = {
            "user": {
                "firstName": FIRST,
                "lastName": LAST,
                "email": EMAIL,
            }
        }
        sheety_post = requests.post(self.sheety_users_endpoint, json=user_data, auth=self.basic_auth)
        return sheety_post.json()
