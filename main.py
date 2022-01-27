"""
Task
Using the following website www.fly540.com you need to collect required data for ALL round trip flight
combinations from NBO (Nairobi) to MBA (Mombasa) departing 10 and 20 days from the current date
and returning 7 days after the departure date. The required data:
o departure airport, arrival airport - Outbound and inbound departure and arrival flight IATA airport
code extracted from the source (it is a three-letter geocode designating many airports and
metropolitan areas around the world)
o departure time, arrival time - Time including date in any human understandable format extracted
from the source.
o cheapest fare price - final price which would be paid by the customer for the selected outbound
and inbound flight.
2. After finishing the task above, please implement additional logic to extract taxes with the same flight
combinations described above:
o taxes - There can be many different types of taxes included in the final p
"""
from flying_scraper import search_flights

# Initial data
url = 'https://www.fly540.com/'
origin = 'NBO'
destination = 'MBA'
dep_after_days = [10, 20]
return_fl_after_days = 7
currency = 'USD'
save_to = 'results2.csv'  # csv

if __name__ == '__main__':
    search_flights(origin, destination, dep_after_days, return_fl_after_days, save_to, url, currency)
