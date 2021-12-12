from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

ORIG_SOURCE_CITY = 'AMS'
sheet = DataManager()
flight_search = FlightSearch()
notification = NotificationManager()
data = sheet.get_sheet_data()['prices']

switch = input("Do you want to sign up or find the deals? Type 'deals' or 'sign up': ").lower()
clear_price = input("Do you want to clear the current prices? (y/n) ")
clear = False
match clear_price:
    case "y":
        clear = True


match switch:
    case 'deals':
        # check if the there is item without iata code
        cities_wout_iata = []
        for row in data:
            if not row['iataCode']:
                cities_wout_iata.append({row['id']: row['city']})
        for city in cities_wout_iata:
            # call the function to find iata code and put this in the sheet
            value = flight_search.get_cities(city)
            sheet.put_iata_code(value)

        for item in data:
            flight = flight_search.search_flight(ORIG_SOURCE_CITY, item['iataCode'])
            if clear:
                item['lowestPrice'] = 100000
            if flight and flight.price < item['lowestPrice']:
                # update sheet with the destination city and the lowest price for the flight
                sheet.update_price(item['id'], flight.link, flight.price, flight.stop_overs)
                # message handler
                message = f'Low price alert!\n Only {flight.price} EUR to fly ' \
                        f' from {flight.source_city}-{flight.source_iata} ' \
                        f'to {flight.dest_city}-{flight.dest_iata}. Flight date: {flight.dates}'
                if flight.stop_overs > 0:
                    message += f' Flight has {flight.stop_overs} stop over, via {flight.via_city}'

                # SMS notification
                #notification.send_message(message=message)
                users = sheet.get_users()
                first_names = [row['firstName'] for row in users]
                emails = [row['email'] for row in users]
                # Email notification
                #notification.send_email(first_names, emails, flight.link, message)

    case 'sign up':
        print("Welcome to my Flight club!")
        if input("Do you want to sign up? Y or N: ").lower() == "y":
            name = input("What is you first name?\n")
            last_name = input("What is you last name?\n")
            email = input("What is you email?\n")
            if input("Please type your email again.\n") == email:
                print("You're in the club!")
                sheet.put_email(name, last_name, email)
            else:
                print("Emails are not the same.")
