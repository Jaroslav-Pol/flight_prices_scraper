'''
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
'''

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from datetime import date, timedelta
import time
from random import randint

'''Initial data'''
origin = 'NBO'
destination = 'MBA'
flight_after_days = 10
return_flight_after_days = 7

driver = webdriver.Chrome(executable_path='C:/Users/jaros/Desktop/Python/WebScraping/chromedriver.exe')
driver.get('https://www.fly540.com/')


def search_flights():
    """This function search flights from """
    '''Selecting origin and destination'''
    Select(driver.find_element(By.ID, 'depairportcode')).select_by_value(origin)
    time.sleep(1)
    Select(driver.find_element(By.ID, 'arrvairportcode')).select_by_value(destination)
    time.sleep(1)

    '''Selecting departure date'''
    depart_date = date.today() + timedelta(days=flight_after_days)
    depart_month = str(depart_date.month - 1)  # -1 because options are from 0 to 11
    depart_day = str(depart_date.day)

    driver.find_element(By.ID, 'date_from').click()
    time.sleep(1)  # ?????? do we need this???
    Select(driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/select')).select_by_value(depart_month)
    driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/table/tbody').find_element(By.LINK_TEXT,
                                                                                           depart_day).click()
    time.sleep(1)

    '''Selecting return date'''
    return_date = depart_date + timedelta(days=return_flight_after_days)
    return_month = str(return_date.month - 1)
    return_day = str(return_date.day)

    driver.find_element(By.ID, 'date_to').click()
    time.sleep(1)
    Select(driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/select')).select_by_value(return_month)
    driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/table/tbody').find_element(By.LINK_TEXT,
                                                                                           return_day).click()
    time.sleep(1)

    '''Selecting currency'''

    Select(driver.find_element(By.XPATH, '//*[@id="frmFlight"]/div[1]/div[3]/select')).select_by_value('USD')
    time.sleep(1)

    '''Search flights button click'''
    driver.find_element(By.ID, 'searchFlight').click()


def select_flight():
    pass
