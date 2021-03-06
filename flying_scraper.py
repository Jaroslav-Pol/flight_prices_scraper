from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import date, timedelta
import pandas as pd
import time

result_dict = {
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

driver = webdriver.Chrome(executable_path='C:/Users/jaros/Desktop/Python/WebScraping/chromedriver.exe')


def search_flights(origin, destination, dep_after_days, return_fl_after_days, save_to, url, currency):
    """This function search flights from initial data"""
    driver.get(url)
    for i in range(len(dep_after_days)):
        # 1. Iterates through all given departure dates
        global depart_year
        global return_year
        flight_after_days = dep_after_days[i]

        # 2. Selecting origin and destination
        Select(driver.find_element(By.ID, 'depairportcode')).select_by_value(origin)
        time.sleep(2)
        Select(driver.find_element(By.ID, 'arrvairportcode')).select_by_value(destination)
        time.sleep(2)

        # 3. Selecting departure date
        depart_date = date.today() + timedelta(days=flight_after_days)
        depart_month = str(depart_date.month - 1)  # -1 because options are from 0 to 11
        depart_day = str(depart_date.day)
        depart_year = str(depart_date.year)

        # 3.1 Opens calendar and selects given date
        driver.find_element(By.ID, 'date_from').click()
        time.sleep(1)  # wait until it opens
        Select(driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/select')).select_by_value(
            depart_month)
        driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/table/tbody').find_element(By.LINK_TEXT,
                                                                                               depart_day).click()
        time.sleep(1)

        # 4. Selecting return date
        return_date = depart_date + timedelta(days=return_fl_after_days)
        return_month = str(return_date.month - 1)
        return_day = str(return_date.day)
        return_year = str(return_date.year)

        # 4.1 Opens calendar and selects given date
        driver.find_element(By.ID, 'date_to').click()
        time.sleep(1)  # wait until it opens
        Select(driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/select')).select_by_value(
            return_month)
        driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/table/tbody').find_element(By.LINK_TEXT,
                                                                                               return_day).click()
        time.sleep(1)

        # 5. Selecting currency
        Select(driver.find_element(By.XPATH, '//*[@id="frmFlight"]/div[1]/div[3]/select')).select_by_value(currency)
        time.sleep(1)

        # 6. Clicks search button
        driver.find_element(By.ID, 'searchFlight').click()

        # 7. Calls function for another page
        flight_selector()

    # 8. Saves results and quits driver
    save_results(save_to)
    driver.quit()


def date_formatter(fl_time, fl_date, fl_year):
    """Formats time and date, and join them together"""
    formatted_time = fl_time.text.strip().upper()
    formatted_date = fl_date.text.strip().replace(',', '')
    return formatted_time + ' ' + formatted_date + ' ' + fl_year


def flight_selector():
    """Selects all possible flight combinations"""

    # 1. Finding how much possible flight we have
    total_outb_fl = len(
        driver.find_element(By.XPATH, '//*[@id="book-form"]/div[1]').find_elements(By.CLASS_NAME, 'fly5-result'))
    total_inb_fl = len(
        driver.find_element(By.XPATH, '//*[@id="book-form"]/div[2]/div[2]').find_elements(By.CLASS_NAME, 'fly5-result'))

    # 2. Iterates through all possible flight combinations
    for a in range(total_outb_fl):
        for b in range(total_inb_fl):
            # 2.1 Creates list for outbound and inbound flights
            outb_fl_list = driver.find_element(By.XPATH, '//*[@id="book-form"]/div[1]').find_elements(
                By.CLASS_NAME,
                'fly5-result')
            inb_fl_list = driver.find_element(By.XPATH, '//*[@id="book-form"]/div[2]/div[2]').find_elements(
                By.CLASS_NAME, 'fly5-result')
            # time.sleep method added to check visually how its going, better use wait.until method from selenium
            # also this method is needed to wait until JS is working (like collapse element, etc.)
            time.sleep(1)

            # 2.2 Clicks on outbound flight
            outb_fl_list[a].click()
            time.sleep(1)
            outb_fl_list[a].find_element(By.CLASS_NAME, 'select-flight').click()  # selects cheapest(first) flight
            time.sleep(1)

            # 2.3 Clicks on inbound flight
            inb_fl_list[b].click()
            time.sleep(1)
            inb_fl_list[b].find_element(By.CLASS_NAME, 'select-flight').click()  # selects cheapest(first) flight
            time.sleep(1)

            # 2.4 Clicks on continue button and goes to another page
            driver.find_element(By.ID, 'continue-btn').click()
            time.sleep(1)

            # 2.5 Calling price_scraper
            price_scraper()
            driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.HOME)  # Going page up, not necessary
            time.sleep(1)

    # 3. Going back to previous page
    driver.back()


def price_scraper():
    """Scrapes all required data(price, taxes, times, etc.)"""

    # 1. Scraping airport names
    outb_dep_air = driver.find_element(By.XPATH, '//*[@id="fsummary"]/div[1]/div[2]/div[1]').text
    outb_arr_air = driver.find_element(By.XPATH, '//*[@id="fsummary"]/div[1]/div[2]/div[3]').text
    inb_dep_air = driver.find_element(By.XPATH, '//*[@id="fsummary"]/div[2]/div[2]/div[1]').text
    inb_arr_air = driver.find_element(By.XPATH, '//*[@id="fsummary"]/div[2]/div[2]/div[3]').text

    # 2. Scraping date and time
    time_list = driver.find_elements(By.CLASS_NAME, 'fly5-ftime')
    date_list = driver.find_elements(By.CLASS_NAME, 'fly5-fdate')
    outb_dep_time = date_formatter(time_list[0], date_list[0], depart_year)
    outb_arr_time = date_formatter(time_list[1], date_list[1], depart_year)
    inb_dep_time = date_formatter(time_list[2], date_list[2], return_year)
    inb_arr_time = date_formatter(time_list[3], date_list[3], return_year)

    # 3. Scraping prices
    # To access 'View breakdown button(to scrape taxes), we need to scroll down the page,
    # otherwise button is hidden under another button(send message)
    time.sleep(1)
    driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.END)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="fsummary"]/div[4]/a').click()  # need to wait for element to be located
    time.sleep(1)
    total_price = float(driver.find_element(By.CLASS_NAME, 'fly5-price').text)
    taxes = float(driver.find_element(By.XPATH, '//*[@id="breakdown"]/div/div[1]/div[2]/span').text) + float(
        driver.find_element(By.XPATH, '//*[@id="breakdown"]/div/div[2]/div[2]/span').text)

    # 4. Adding results to dictionary
    result_dict['outbound_departure_airport'].append(outb_dep_air)
    result_dict['outbound_arrival_airport'].append(outb_arr_air)
    result_dict['outbound_departure_time'].append(outb_dep_time)
    result_dict['outbound_arrival_time'].append(outb_arr_time)
    result_dict['inbound_departure_airport'].append(inb_dep_air)
    result_dict['inbound_arrival_airport'].append(inb_arr_air)
    result_dict['inbound_departure_time'].append(inb_dep_time)
    result_dict['inbound_arrival_time'].append(inb_arr_time)
    result_dict['total_price'].append(total_price)
    result_dict['taxes'].append(taxes)

    # 5. Going to previous page
    driver.back()


def save_results(save_to):
    """Saves results to csv file"""
    df = pd.DataFrame(result_dict)
    df.to_csv(save_to, index=False, encoding='utf-8')
