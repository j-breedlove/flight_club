import os

from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()


class SMSClient:
    """A class used to send SMS alerts via the Twilio API when a cheaper flight is found."""

    def __init__(self, flight_search):
        """
        Initialize the SMSClient class.
        
        Parameters:
        - flight_search (FlightSearch): An instance of the FlightSearch class.
        """
        # Load sensitive information from .env file
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.flight_search = flight_search
        self.client = Client(self.account_sid, self.auth_token)

    def send_sms(self, iata_code, FROM, FROM_CITY, city, flight_data):
        """
        Send an SMS alert if a cheaper flight is found.
        
        Parameters:
        - iata_code (str): The IATA code of the destination city.
        - FROM (str): The departure city's IATA code.
        - FROM_CITY (str): The name of the departure city.
        - city (str): The name of the destination city.
        - flight_data (dict): A dictionary containing flight data.
        """
        if flight_data:
            message_body = f"Low Price Alert! from {FROM_CITY}-{FROM} to {city}-{iata_code}. Price: ${flight_data['price']}"
            message = self.client.messages.create(
                from_=os.getenv("TWILIO_PHONE_FROM"),
                body=message_body,
                to=os.getenv("TWILIO_PHONE_TO")
            )
            print(message.sid)
