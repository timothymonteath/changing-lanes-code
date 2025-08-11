import pandas as pd
import numpy as np
import os
import re

# load in the BvD data

df = pd.read_csv('Final_All_v5.csv')

# drop rows without NAICS codes

df[df['Target primary NAICS 2017 code'].isnull() == False]['Target primary NAICS 2017 code'].apply(lambda x: str(int(round(x, 0))))
df[df['Acquiror primary NAICS 2017 code'].isnull() == False]['Acquiror primary NAICS 2017 code'].apply(lambda x: str(int(round(x, 0))))

# Keep only these columns used in the analysis

cols = ['Deal Number', 'Deal value', 'Target name', # drop old food cols and index
       'Target country', 'Target BvD ID', 'Acquiror name', 'Acquiror country',
       'Acquiror BvD ID', 'Completed date', 'Assumed completion date',
       'Last update', 'Deal editorial', 'Deal comments', 'Category of source',
       'Source documentation', 'Target postcode', 'Target city',
       'Target phone', 'Target Postcode Additional', 'Target City Additional',
       'Target Country Additional', 'Target Phone number Additional',
       'Acquiror postcode', 'Acquiror city', 'Acquiror phone',
       'Acquiror Postcode Additional', 'Acquiror City Additional',
       'Acquiror Country Additional', 'Target NAICS 2017 code(s)',
       'Target primary NAICS 2017 code', 'Acquiror NAICS 2017 code(s)',
       'Acquiror primary NAICS 2017 code', 'Target ISIN number',
       'Target ticker symbol', 'Acquiror ISIN number',
       'Acquiror ticker symbol', 'Estimated Value', 'Year',
       'Target FULL Address', 'Acquiror FULL Address', 'Target FULL Address 2',
       'Acquiror FULL Address 2', 'TargetUUID', 'AcquirorUUID', 'TargetUUID2',
       'AcquirorUUID2', 'Acquiror Phone number Additional',
       'Target Standardised City', 'Target Long', 'Target Lat',
       'Target Classifier', 'Acquiror Standardised City', 'Acquiror Long',
       'Acquiror Lat', 'Acquiror Classifier', 'Target Loc Standardisation',
       'Acquiror Loc Standardisation',
       'TargetPharma', 'AcquirorPharma', 'TargetMotor', 'AcquirorMotor',
       'TargetFinance', 'AcquirorFinance', 'TargetIt', 'AcquirorIt',
       'TargetEnergy', 'AcquirorEnergy', 'TargetCountryMissmatch',
       'AcquirorCountryMissmatch']

df = df[cols]

## defining the motor industry

motor_list = range(336100,336399,1)

df.loc[(df['Target primary NAICS 2017 code'].isnull() == False) & (df['Target primary NAICS 2017 code'].isin(motor_list) == True), 'TargetMotor'] = 1

df.loc[(df['Acquiror primary NAICS 2017 code'].isnull() == False) & (df['Acquiror primary NAICS 2017 code'].isin(motor_list) == True), 'AcquirorMotor'] = 1

motor = df.groupby('Deal Number').filter(lambda x: (x['AcquirorMotor'].sum() > 0) | (x['TargetMotor'].sum() > 0))

# GDP deflator and
# making sure all deals are within our date range

motor = motor[(motor['Year'] > 2000) & (motor['Year'] <= 2020)]

gdp = pd.read_csv('https://api.db.nomics.world/v22/series/WB/WDI/A-NY.GDP.DEFL.ZS.AD-USA.csv')

gdp.columns = ['Year', 'GDP_Deflator']

gdp['Adj_2010'] = 100 * (gdp['GDP_Deflator'] / 91.862508)
gdp.loc[gdp['Year'] == 2020, ['10M_Adj_2010']] = 11711898.628216067

deflator_dict = dict(zip(gdp['Year'], gdp['Adj_2010']))

motor['Deflator'] = motor['Year'].apply(lambda x: deflator_dict.get(x))

motor['Deal value adj'] = motor['Deal value'] * (100 / motor['Deflator'])

motor.to_csv('motor_data.csv')

