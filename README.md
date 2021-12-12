# Flight_Deals_AMS

Project for viewing the cheapest flight deals from Netherlands to other countries.

## About

This application finds the cheapest flights for 2 adults:

- from today up to 6 months in future. (Picks one-way flight)

- according to the provided dates. (Picks round trip)

## Configuration

This project requires Python 3.10.

Sample sheet [example](https://docs.google.com/spreadsheets/d/1L5dLuKqe2JLCVsnpOSp6E50R6OUXWRUILcfyfzMYA1s/edit?usp=sharing)
The sheet should have at least the name of the city and the min price (I took some big number e.g. 100000 at first)

In oder to use it, need to set up sheety.co, bit.ly and tequila-api.kiwi.com accounts at least (twilio is optional, can be commented along with send_email function call if you don't want to be notified).

1) For sheety.co configuration you need to change "SHEET_ENDPOINT" var as well as add you own sheet to your account and enable "GET", "POST", "PUT".
2) Bit.ly requires 'BITLY_TOKEN', which you can get after signing up.
3) For tequila.kiwi.com you'll need API_KEY which you can get after signing up and registring an application.
