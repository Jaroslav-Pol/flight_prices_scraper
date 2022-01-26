import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, timedelta
import time
import random
from random import randint

# def wait():
#     return time.sleep(random.uniform(1.5, 3))


year = '2022'  # just as example
driver = webdriver.Chrome(executable_path='C:/Users/jaros/Desktop/Python/WebScraping/chromedriver.exe')
driver.get('https://www.fly540.com/flights/nairobi-to-mombasa?isoneway=0&currency=USD&depairportcode=NBO&'
           'arrvairportcode=MBA&date_from=Thu%2C+3+Feb+2022&date_to=Thu%2C+10+Feb+2022&adult_no=1&children_no=0&'
           'infant_no=0&searchFlight=&change_flight=')
'''this driver only for beta'''

result_dic = {
    'outbound_departure_airport': [],
    'outbound_arrival_airport': [],
    'outbound_departure_time': [],
    'outbound_arrival_time': [],
    'inbound_departure_airport': [],
    'inbound_arrival_airport': [],
    'inbound_departure_time': [],
    'inbound_arrival_time': [],
    'total_price': [],
    'taxes': []
}

outbound_flights_list = driver.find_element(By.XPATH, '//*[@id="book-form"]/div[1]').find_elements(By.CLASS_NAME,
                                                                                                   'fly5-result')
inbound_flights_list = driver.find_element(By.XPATH, '//*[@id="book-form"]/div[2]/div[2]').find_elements(By.CLASS_NAME,
                                                                                                         'fly5-result')

for a in outbound_flights_list:
    time.sleep(2)
    a.click()
    time.sleep(2)
    a.find_element(By.CLASS_NAME, 'select-flight').click()
    for b in inbound_flights_list:
        time.sleep(2)
        b.click()
        time.sleep(2)
        b.find_element(By.CLASS_NAME, 'select-flight').click()
        time.sleep(2)
        driver.find_element(By.ID, 'continue-btn').click()
        time.sleep(5)

        break
    break

'''Scraping airport names'''
outbound_departure_airport = driver.find_element(By.XPATH, '//*[@id="fsummary"]/div[1]/div[2]/div[1]').text
outbound_arrival_airport = driver.find_element(By.XPATH, '//*[@id="fsummary"]/div[1]/div[2]/div[3]').text
inbound_departure_airport = driver.find_element(By.XPATH, '//*[@id="fsummary"]/div[2]/div[2]/div[1]').text
inbound_arrival_airport = driver.find_element(By.XPATH, '//*[@id="fsummary"]/div[2]/div[2]/div[3]').text

'''Scraping dates and times'''


def date_formatter(time, date):
    '''Formats time and date, and join them together'''
    time = time.text.strip().upper()
    date = date.text.strip().replace(',', '')
    return time + ' ' + date + ' ' + year  # reikia dar prideti metus normaliai is paieskos datos


time_list = driver.find_elements(By.CLASS_NAME, 'fly5-ftime')
date_list = driver.find_elements(By.CLASS_NAME, 'fly5-fdate')

outbound_departure_time = date_formatter(time_list[0], date_list[0])
outbound_arrival_time = date_formatter(time_list[1], date_list[1])
inbound_departure_time = date_formatter(time_list[2], date_list[2])
inbound_arrival_time = date_formatter(time_list[3], date_list[3])

'''Scraping prices'''
'''To acces 'View breakdown button(to scrape taxes), we need to scroll down the page, 
otherwise button is hidden under another button(send message)'''
time.sleep(5)

driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.END)
time.sleep(5)
driver.find_element(By.XPATH, '//*[@id="fsummary"]/div[4]/a').click()  # need to wait for element to be located
time.sleep(5)
total_price = float(driver.find_element(By.CLASS_NAME, 'fly5-price').text)
taxes = float(driver.find_element(By.XPATH, '//*[@id="breakdown"]/div/div[1]/div[2]/span').text) + float(
    driver.find_element(By.XPATH, '//*[@id="breakdown"]/div/div[2]/div[2]/span').text)

'''Adding reults to dictionary'''
result_dic['outbound_departure_airport'].append(outbound_departure_airport)
result_dic['outbound_arrival_airport'].append(outbound_arrival_airport)
result_dic['outbound_departure_time'].append(outbound_departure_time)
result_dic['outbound_arrival_time'].append(outbound_arrival_time)
result_dic['inbound_departure_airport'].append(inbound_departure_airport)
result_dic['inbound_arrival_airport'].append(inbound_arrival_airport)
result_dic['inbound_departure_time'].append(inbound_departure_time)
result_dic['inbound_arrival_time'].append(inbound_arrival_time)
result_dic['total_price'].append(total_price)
result_dic['taxes'].append(taxes)

print(result_dic)
