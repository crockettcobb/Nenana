from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from urllib.request import urlopen
import numpy as np
import os


def parse_station(station):
    '''
    This function parses the web pages downloaded from wunderground.com
    into a flat CSV file for the station you provide it.
    Make sure to run the wunderground scraper first so you have the web
    pages downloaded.
    '''
    # no daily average data is available for the Nenana weather station
    # prior to 1 JAN 1949
    years = np.arange(1949, 2017)

    os.chdir('C:/Users/crock/Documents/GitHub/Nenana/data/')

    # exclude_list = [datetime(year=1971, month=3, day=31),
    #                 datetime(year=1971, month=4, day=4)]
    with open('{}.csv'.format(station), 'w') as out_file:
        out_file.write('date,actual_mean_temp, \n')#,actual_min_temp,\
                        #actual_max_temp,\n')
        for y in years:
        # You can change the dates here if you prefer to parse a different range
            current_date = datetime(year=y, month=10, day=1)
            end_date = datetime(year=y+1, month=4, day=1)

            while current_date != end_date:

                with open('{}/{}-{}-{}.html'.format(station,
                                                    current_date.year,
                                                    current_date.month,
                                                    current_date.day)) as in_file:
                    soup = BeautifulSoup(in_file.read(), 'html.parser')

                    weather_data = soup.find(id='historyTable').find_all('span', class_='wx-value')
                    weather_data_units = soup.find(id='historyTable').find_all('td')

                    actual_mean_temp = weather_data[0].text
                    # actual_max_temp = weather_data[1].text
                    # actual_min_temp = weather_data[4].text

                    out_file.write('{}-{}-{},'.format(current_date.year, current_date.month, current_date.day))
                    out_file.write(','.join([actual_mean_temp]))
                    out_file.write('\n')
                    # print(current_date)
                    current_date += timedelta(days=1)
                    # if current_date in exclude_list:
                    #     current_date += timedelta(days=1)


# Parse the stations used in this article
for station in ['PANN']:
    parse_station(station)
