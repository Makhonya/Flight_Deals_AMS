import requests
import os
SHEET_ENDPOINT = os.getenv('SHEET_ENDPOINT')
BITLY_TOKEN = os.getenv('BITLY_TOKEN')


class DataManager:
    # get users info for sending emails
    def get_users(self):
        response = requests.get(f'{SHEET_ENDPOINT}/users')
        return response.json()['users']

    def get_sheet_data(self):
        response = requests.get(f'{SHEET_ENDPOINT}/prices')
        return response.json()

    def put_iata_code(self, iata_dict: dict):
        # put request to update iata codes
        id = [*iata_dict][0]
        code = iata_dict[id]
        endpoint = f'{SHEET_ENDPOINT}/prices/{id}'
        payload = {
            'price':
                {
                    'iataCode': code
                }
        }
        response = requests.put(endpoint, json=payload)
        response.raise_for_status()

    def update_price(self, id, link, price, stop_overs):
        # function to update sheet with the lowest destination city along with the booking link
        endpoint = f'{SHEET_ENDPOINT}/prices/{id}'
        payload = {
            'price':
                {
                    'lowestPrice': price,
                    'destination': self.shorten_link(link),
                    'stopovers': "Direct" if stop_overs == 0 else stop_overs
                }
        }
        requests.put(endpoint, json=payload)

    def put_email(self, first_name, last_name, email):
        endpoint = f'{SHEET_ENDPOINT}/users/'
        payload = {
            'user':
                {
                    'firstName': first_name,
                    'lastName': last_name,
                    'email': email
                }
        }
        requests.post(endpoint, json=payload)

    def shorten_link(self, link: str) -> str:
        """
        Shortens the link using bit.ly
        :param link: str
        :return: str
        """
        header = {
            'Authorization': f'Bearer {BITLY_TOKEN}',
            'Content-Type': 'application/json'
        }
        payload = {
            'long_url': link
        }
        response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=header, json=payload)
        link = response.json()['link']
        return link