
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from urllib.request import urlopen
import numpy as np
import os

os.chdir('../data/PANN/')

with open('test.csv', 'w') as out_file:
    out_file.write('date,actual_mean_temp,actual_min_temp,actual_max_temp,'
                   'average_min_temp,average_max_temp,'
                   'record_min_temp,record_max_temp,'
                   'record_min_temp_year,record_max_temp_year,'
                   'actual_precipitation,average_precipitation,'
                   'record_precipitation\n')

with open('1987-12-1.html') as in_file:
    soup = BeautifulSoup(in_file.read(), 'html.parser')

    weather_data = soup.find(id='historyTable').find_all('span', class_='wx-value')
    weather_data_units = soup.find(id='historyTable').find_all('td')

    actual_mean_temp = weather_data[0].text
    actual_max_temp = weather_data[2].text
    actual_min_temp = weather_data[5].text

    actual_mean_temp
