import datetime as dt
import os
import requests
from dotenv import load_dotenv

from sheety_client import SheetyClient

load_dotenv()

# Load sensitive information from .env file
KIWI_API_KEY = os.getenv("KIWI_API_KEY")
HEADERS = {
    "apikey": os.getenv("HEADERS_APIKEY")
}
KIWI_ENDPOINT = "https://tequila-api.kiwi.com"
FLIGHT_SEARCH_ENDPOINT = f"{KIWI_ENDPOINT}/v2/search"


class FlightSearch(SheetyClient):
    """A class used to retrieve flight prices for specific routes from the Kiwi API."""

    def __init__(self, FROM):
        """
        Initialize the FlightSearch class.
        
        Parameters:
        - FROM (str): The departure city's IATA code.
        """
        super().__init__()
        self.sheety_request = requests.get(self.sheety_deals_endpoint, auth=self.basic_auth)
        self.sheety_data = self.sheety_request.json()
        self.FROM = FROM

    def search_prices(self, iata_code):
        """
        Search for the prices of flights between the departure city and the given IATA code.
        
        Parameters:
        - iata_code (str): The IATA code of the destination city.

        Returns:
        - dict: A dictionary containing the flight cost and departure city if a cheaper price is found.
        - None: If no cheaper price is found or an error occurs.
        """
        flight_search_params = {
            "fly_from": self.FROM,
            "fly_to": iata_code,
            "dateFrom": dt.datetime.now().strftime("%d/%m/%Y"),
            "dateTo": (dt.datetime.now() + dt.timedelta(days=180)).strftime("%d/%m/%Y"),
            "partner": os.getenv("KIWI_PARTNER"),
            "curr": "USD",
        }

        response = requests.get(FLIGHT_SEARCH_ENDPOINT, flight_search_params, headers=HEADERS)
        try:
            data = response.json()
            if not data.get('data'):
                raise ValueError(f"No flights found for {self.FROM}-{iata_code}")

            price_list = [price['price'] for price in data['data']]
            lowest_price = [price['lowestPrice'] for price in self.sheety_data['prices']]
            flight_cost = min(price_list)

            if flight_cost < lowest_price[0]:
                return {"price": flight_cost, "from_city": self.FROM}
            else:
                return None

        except ValueError as ve:
            print(f"ValueError: {ve}")
            return None
        except Exception as e:
            print(f"Exception: {e}")
            return None
