
# coding: utf-8

# In[1]:

get_ipython().magic('matplotlib inline')


# In[2]:

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from tpot import TPOTRegressor


# In[3]:

results = pd.read_csv('../data/parsed_data.csv')


# In[4]:

results['ice_out'] = pd.to_datetime(results['ice_out'])
results.head()
results1 = results[(results.Year>=1950)&(results.Year<=2016)][['Year', 'JDOY']].copy()
results1.columns = ['Year', 'iceout']


# In[5]:

df = pd.read_csv('../data/PANN2.csv', parse_dates=['date'], index_col='date')
df = df.dropna(how='all', axis=1)
df['doy'] = df.index.dayofyear


df['year'] = df.index.year
# push OCT, NOV, and DEC into the appropriate Ice Classic Results Year
df['year'] = np.where(df.index.month == 10, df.year+1, df.year)
df['year'] = np.where(df.index.month == 11, df.year+1, df.year)
df['year'] = np.where(df.index.month == 12, df.year+1, df.year)

df = df.resample('W-MON').mean()
df['week'] = df.index.week


# In[6]:

df.columns = ['actual_mean_temp', 'wind', 'doy', 'year', 'week']

df_temp = df[['actual_mean_temp', 'doy', 'week', 'year']]
df_wind = df[['wind', 'doy', 'week', 'year']]


# In[ ]:




# In[7]:

df2 = pd.pivot_table(df_temp, values='actual_mean_temp', columns='week', index='year')
df2 = df2.dropna(how='all', axis=1).copy()

df3 = pd.pivot_table(df_wind, values='wind', columns='week', index='year')
df3 = df3.dropna(how='all', axis=1).copy()


# In[8]:

col_names = df2.columns.tolist()
col_names_corr = []
for col in col_names:
    col = 'temp'+str(col)
    col_names_corr.append(col)
    
col_names_w = df3.columns.tolist()
col_names_corr_w = []
for col in col_names_w:
    col = 'wind'+str(col)
    col_names_corr_w.append(col)


# In[9]:

df2.columns = col_names_corr
df3.columns = col_names_corr_w


# In[10]:

df4 = df2.merge(results1, how='inner', left_index=True, right_on='Year')
df5 = df4.merge(df3, how='inner', left_on="Year", right_index=True)
df_hold = df5[(df5.Year<=2016)&(df5.Year>=2013)].copy()
df5 = df5[df5.Year<2014]
df5 = df5.drop(['Year'], axis=1)
df_hold = df_hold.drop(['Year'], axis=1)


# In[11]:

df5 = df5.fillna(method='ffill').fillna(method='bfill')


# In[12]:

features = df5.columns.tolist()
features = [x for x in features if x != 'iceout']


# In[13]:

y = df5.iceout.values
X = df5[features].values


# In[19]:

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10)


# In[ ]:




# In[20]:

tpot = TPOTRegressor(generations=40, population_size=300, verbosity=2, scoring='r2', warm_start=False, cv=7)
tpot.fit(X_train, y_train)
print(tpot.score(X_test, y_test))


# In[ ]:



