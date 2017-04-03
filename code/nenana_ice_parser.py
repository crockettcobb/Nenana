import os

import pandas as pd
import numpy as np

def to_seconds(s):
    hr, min, sec = [float(x) for x in s.split(':')]
    return hr*3600 + min*60 + sec


def parse_nenana():
    ''' Parse the Nenana Ice Classic tripod out ice data
    and ensure that the Julian decimal calendar dates match
    the plaintext dates'''

    os.chdir('../data/')

    df = pd.read_csv('tripod_dates.csv')
    df.columns
    df.Year = df.Year.apply(str)
    df['Date'] = df.Month_Day + ' ' + df.Year
    df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    df = df.set_index('datetime')
    df['DOY'] = df.index.dayofyear
    df.head()

    df['hour'] = df.index.hour
    df['minute'] = df.index.minute
    df['JDOY'] = (df.hour*3600 + df.minute*60)/86400+df.index.dayofyear

    df['ice_out'] = df.index
    df.columns

    df[['Year', 'ice_out', 'JDOY']].to_csv('parsed_data.csv', index=False)
