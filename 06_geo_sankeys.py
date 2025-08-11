import pandas as pd
import numpy as np
import os
import re
from collections import Counter

## This file does some final counting for the Sankeys - the counts for all the files are correct
## 06 has been appended to the output files from 05_geography to make clear which files are being used
## by this script

inward = pd.read_csv('06_inward_city_all.csv')

# keeping the top 10 acquiror cities only

acq_count = inward.groupby('Acquiror Standardised City').agg({'Count' : 'sum'})
acq_count = acq_count.reset_index()

### top 10 only !!!

above10acq = list(acq_count[acq_count['Count'] > 9]['Acquiror Standardised City'])

inward = inward[inward['Acquiror Standardised City'].isin(above10acq)]

##

tg_count = inward.groupby('Target Standardised City').agg({'Count' : 'sum'})
tg_count = tg_count.reset_index()
below10tg = list(tg_count[tg_count['Count'] < 10]['Target Standardised City'])

inward.loc[inward['Target Standardised City'].isin(below10tg) == True, 'Target Standardised City'] = inward.loc[inward['Target Standardised City'].isin(below10tg) == True, 'Target name']

tg_count = inward.groupby('Target Standardised City').agg({'Count' : 'sum'})
tg_count = tg_count.reset_index()
below10tg = list(tg_count[tg_count['Count'] < 10]['Target Standardised City'])

inward.loc[inward['Target Standardised City'].isin(below10tg) == True, 'Target Standardised City'] = inward.loc[inward['Target Standardised City'].isin(below10tg) == True, 'Target region']

# Now merging those with less than 10 in the targets list

# remove some rows for 'Middle East' which mistakenly found their way into the into the aq list
inward = inward[inward['Acquiror Standardised City'] != 'Middle East & North Africa']
inward = inward[inward['Acquiror Standardised City'] != 'United States']

tg_count = inward.groupby('Target Standardised City').agg({'Count' : 'sum'})
tg_count = tg_count.reset_index()
below10tg = list(tg_count[tg_count['Count'] < 10]['Target Standardised City'])

inward.loc[inward['Target Standardised City'].isin(below10tg) == True, 'Target Standardised City'] = 'Other'

inward.to_csv('06_inward_cities_over_10.csv')

# Outward

outward = pd.read_csv('06_outward_city_all.csv')

# keeping the top 10 acquiror cities only

acq_count = outward.groupby('Acquiror Standardised City').agg({'Count' : 'sum'})
acq_count = acq_count.reset_index()

### top 10 only !!!

above10acq = list(acq_count[acq_count['Count'] > 9]['Acquiror Standardised City'])

outward = outward[outward['Acquiror Standardised City'].isin(above10acq)]

##

tg_count = outward.groupby('Target Standardised City').agg({'Count' : 'sum'})
tg_count = tg_count.reset_index()
below10tg = list(tg_count[tg_count['Count'] < 10]['Target Standardised City'])

outward.loc[outward['Target Standardised City'].isin(below10tg) == True, 'Target Standardised City'] = outward.loc[outward['Target Standardised City'].isin(below10tg) == True, 'Target name']

tg_count = outward.groupby('Target Standardised City').agg({'Count' : 'sum'})
tg_count = tg_count.reset_index()
below10tg = list(tg_count[tg_count['Count'] < 10]['Target Standardised City'])

outward.loc[outward['Target Standardised City'].isin(below10tg) == True, 'Target Standardised City'] = outward.loc[outward['Target Standardised City'].isin(below10tg) == True, 'Target region']

# remove some rows for 'US' which mistakenly found their way into the into the aq list
outward = outward[outward['Acquiror Standardised City'] != 'US']

outward.loc[outward['Target Standardised City'] == 'US', 'Target Standardised City'] = 'United States'

# Now merging those with less than 10 in the targets list

tg_count = outward.groupby('Target Standardised City').agg({'Count' : 'sum'})
tg_count = tg_count.reset_index()
below10tg = list(tg_count[tg_count['Count'] < 10]['Target Standardised City'])

outward.loc[outward['Target Standardised City'].isin(below10tg) == True, 'Target Standardised City'] = 'Other'



outward.to_csv('06_outward_cities_over_10.csv')

# intra

intra = pd.read_csv('06_intra_city_all.csv')

# keeping the top 10 acquiror cities only

acq_count = intra.groupby('Acquiror Standardised City').agg({'Count' : 'sum'})
acq_count = acq_count.reset_index()

### got up to here need to code for top 10 only !!!

above10acq = list(acq_count[acq_count['Count'] > 9]['Acquiror Standardised City'])

intra = intra[intra['Acquiror Standardised City'].isin(above10acq)]

##

tg_count = intra.groupby('Target Standardised City').agg({'Count' : 'sum'})
tg_count = tg_count.reset_index()
below10tg = list(tg_count[tg_count['Count'] < 10]['Target Standardised City'])

intra.loc[intra['Target Standardised City'].isin(below10tg) == True, 'Target Standardised City'] = intra.loc[intra['Target Standardised City'].isin(below10tg) == True, 'Target name']

tg_count = intra.groupby('Target Standardised City').agg({'Count' : 'sum'})
tg_count = tg_count.reset_index()
below10tg = list(tg_count[tg_count['Count'] < 10]['Target Standardised City'])

intra.loc[intra['Target Standardised City'].isin(below10tg) == True, 'Target Standardised City'] = intra.loc[intra['Target Standardised City'].isin(below10tg) == True, 'Target region']

# remove some rows for 'US' which mistakenly found their way into the into the aq list
intra = intra[intra['Acquiror Standardised City'] != 'US']

intra.loc[intra['Target Standardised City'] == 'US', 'Target Standardised City'] = 'United States'

# Now merging those with less than 10 in the targets list

tg_count = intra.groupby('Target Standardised City').agg({'Count' : 'sum'})
tg_count = tg_count.reset_index()
below10tg = list(tg_count[tg_count['Count'] < 10]['Target Standardised City'])

intra.loc[intra['Target Standardised City'].isin(below10tg) == True, 'Target Standardised City'] = 'Other'


intra.to_csv('06_intra_cities_over_10.csv')

