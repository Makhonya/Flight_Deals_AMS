# object for Flights we found.
class FlightData:
    def __init__(self, source_iata, dest_iata, source_city, dest_city, price, dates, link, stop_overs=0, via_city=""):
        self.source_iata = source_iata
        self.dest_iata = dest_iata
        self.source_city = source_city
        self.dest_city = dest_city
        self.price = price
        self.dates = dates
        self.link = link
        self.stop_overs = stop_overs
        self.via_city = via_city

