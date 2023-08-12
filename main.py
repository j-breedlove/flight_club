import os

from dotenv import load_dotenv

from flight_search import FlightSearch
from locations import Locations
from sheety_client import SheetyClient
from sms_client import SMSClient

load_dotenv()

# Load sensitive information from .env file
FLIGHT_LOCATIONS_API_KEY = os.getenv("FLIGHT_LOCATIONS_API_KEY")
FLIGHT_ENDPOINT = "https://tequila-api.kiwi.com"
FROM = "SMF"
FROM_CITY = "Sacramento"

# Collect user input
FIRST_NAME = input("What is your first name? ").title().strip()
LAST_NAME = input("What is your last name? ").title().strip()
EMAIL = input("What is your email? ").lower().strip()
CONFIRM_EMAIL = input("Type your email again. ").lower().strip()

# Initialize necessary classes
locations = Locations(FLIGHT_LOCATIONS_API_KEY)
sheety_client = SheetyClient()
flight_search = FlightSearch(FROM)
sms_client = SMSClient(flight_search)

# Add user to the club if emails match
if EMAIL == CONFIRM_EMAIL:
    print("Welcome to the club!")
    sheety_client.add_user(FIRST_NAME, LAST_NAME, EMAIL)
else:
    print("Emails do not match. Try again.")

# Iterate over cities, get IATA codes, and check for flight prices
for city in sheety_client.get_city_data()['prices']:
    iata_code = locations.get_iata_code(city["city"])
    if iata_code:
        city["iataCode"] = iata_code
        flight_data = flight_search.search_prices(iata_code)
        sheety_client.update_city_data(city["id"], iata_code)
        sms_client.send_sms(iata_code, FROM, FROM_CITY, city["city"], flight_data)
        if flight_data:
            print(f"Cheaper flight found from {FROM} to {city['city']}-{iata_code}. Price: ${flight_data['price']}")
        else:
            print(f"No cheaper flights found to {city['city']}-{iata_code}")
    else:
        print(f"No IATA code found for {city['city']}")
