from unittest import case
import requests
import os
from datetime import datetime, timedelta
from dateutil import relativedelta
from flight_data import FlightData
import time
import pprint

KIWI_ENDPOINT = 'https://tequila-api.kiwi.com'
API_KEY = os.getenv('API_KEY')
today = datetime.today().strftime('%d/%m/%Y')


class FlightSearch:
    def __init__(self):
        """
        Pick either the desired dates or find the cheapest in 6 months.
        The result already includes tickets for 2 persons.
        """
        self.headers = {
            'apikey': API_KEY
        }
        self.flight_type = "oneway"
        self.six_months = (datetime.today() + relativedelta.relativedelta(months=6)).strftime('%d/%m/%Y')
        self.return_day = self.six_months

        dates = input("Would you like to find for some specific dates? (y/n) ")
        match dates:
            case "n":        
                # use relativedelta to find 6 months date
                self.today = (datetime.today() + timedelta(days=1)).strftime('%d/%m/%Y') 
                self.flight_type = "oneway"                
            case "y":
                self.today = input("Pick the starting date of the trip. YYYY-MM-DD: ")
                self.return_day = input("Pick the return date. YYYY-MM-DD: ")
                self.flight_type = "round"

    def get_cities(self, city) -> dict:
        """
        Gets the iata code for the city and returns row_id, it in key: value pair.
        This makes it ease to update the row afterwards
        """
        id = [*city]
        payload = {
            'term': city.values(),
            'location_types': 'city'
        }
        response = requests.get(f'{KIWI_ENDPOINT}/locations/query', headers=self.headers, params=payload)
        result = response.json()
        return {id[0]: result['locations'][0]['code']}

    def search_flight(self, source_iata, dest_iata) -> FlightData:
        """
        Send a get request to kiwi and gather all flights, cheapest first.
        Take the first one and return it as FlightData object
        :param source_iata: iata code for source city
        :param dest_iata: iata code for destination city
        :return: flight: FlightData object
        """
        endpoint = f'{KIWI_ENDPOINT}/search'
        payload = {
            'fly_from': f'city:{source_iata}',
            'fly_to': dest_iata,
            'date_from': self.today,
            'date_to': self.six_months,
            'return_from': self.return_day,
            'return_to': self.return_day,
            'flight_type': self.flight_type,
            'adults': 2,
            'curr': 'EUR',
            'max_stopovers': 0,
            'sort': 'price',
            'asc': 1,
            'limit': 10
        }
        # Catch if there is no flight from this source to this dest.
        flag = True
        # Keep trying to find something until we have 3 or more stop overs between source and dest.
        # Return None in this case.
        while flag and payload['max_stopovers'] < 3:
            try:
                response = requests.get(endpoint, headers=self.headers, params=payload).json()['data'][0]
            except IndexError:
                print(f"There is no flights with {payload['max_stopovers']} from this city")
                payload['max_stopovers'] += 1
            else:
                flag = False
        if payload['max_stopovers'] >= 3:
            print("There are no flights at all :(")
            return None

        # Creating FlightData object from the flight.
        flight = FlightData(
            source_iata=response['flyFrom'],
            dest_iata=response['cityCodeTo'],
            source_city=response['cityFrom'],
            dest_city=response['cityTo'],
            price=response['price'],
            dates=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(response['dTime'])),
            link=response['deep_link'],
            stop_overs=1 if len(response['route']) > 1 else 0,
            via_city=response['route'][0]['cityTo'] if len(response['route']) > 1 else ""
        )
        return flight

