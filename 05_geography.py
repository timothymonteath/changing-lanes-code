import pandas as pd
import numpy as np
import os
import re
from collections import Counter

df = pd.read_csv('motor_data.csv')

# basic counts

intra = df.groupby(['Deal Number']).filter(lambda x: (x['AcquirorMotor'].sum() > 0) & (x['TargetMotor'].sum() > 0))

inward =  df.groupby(['Deal Number']).filter(lambda x: (x['AcquirorMotor'].sum() == 0) & (x['TargetMotor'].sum() > 0))

outward =  df.groupby(['Deal Number']).filter(lambda x: (x['AcquirorMotor'].sum() > 0) & (x['TargetMotor'].sum() == 0))

###################################
# intra
###################################

# note this is the same code for each section, intra, inward and outward with only the directions changed


intra_geo = intra.groupby(['Deal Number']).agg({'Deal value adj' : lambda x: x.iat[0],
                                                  'Target Standardised City' : lambda x: Counter(x.dropna()).most_common(1),
                                                  'Acquiror Standardised City' : lambda x: Counter(x.dropna()).most_common(1),
                                                  'Target country' :  lambda x: Counter(x.dropna()).most_common(1),
                                                  'Acquiror country' : lambda x: Counter(x.dropna()).most_common(1)})

intra_geo = intra_geo.reset_index()

intra_geo['Target Standardised City'] = intra_geo['Target Standardised City'].apply(lambda x: str(x))
intra_geo['Target Standardised City'] = intra_geo['Target Standardised City'].apply(lambda x: re.sub(r"\[\(\'", '', x))
intra_geo['Target Standardised City'] = intra_geo['Target Standardised City'].apply(lambda x: re.sub(r"'[^;]*]", '', x))
intra_geo.loc[intra_geo['Target Standardised City'] == '[]', 'Target Standardised City'] = np.nan

intra_geo['Acquiror Standardised City'] = intra_geo['Acquiror Standardised City'].apply(lambda x: str(x))
intra_geo['Acquiror Standardised City'] = intra_geo['Acquiror Standardised City'].apply(lambda x: re.sub(r"\[\(\'", '', x))
intra_geo['Acquiror Standardised City'] = intra_geo['Acquiror Standardised City'].apply(lambda x: re.sub(r"'[^;]*]", '', x))
intra_geo.loc[intra_geo['Acquiror Standardised City'] == '[]', 'Acquiror Standardised City'] = np.nan


intra_geo['Target country'] = intra_geo['Target country'].apply(lambda x: str(x))
intra_geo['Target country'] = intra_geo['Target country'].apply(lambda x: re.sub(r"\[\(\'", '', x))
intra_geo['Target country'] = intra_geo['Target country'].apply(lambda x: re.sub(r"'[^;]*]", '', x))
intra_geo.loc[intra_geo['Target country'] == '[]', 'Target country'] = np.nan

intra_geo['Acquiror country'] = intra_geo['Acquiror country'].apply(lambda x: str(x))
intra_geo['Acquiror country'] = intra_geo['Acquiror country'].apply(lambda x: re.sub(r"\[\(\'", '', x))
intra_geo['Acquiror country'] = intra_geo['Acquiror country'].apply(lambda x: re.sub(r"'[^;]*]", '', x))
intra_geo.loc[intra_geo['Acquiror country'] == '[]', 'Acquiror country'] = np.nan

intra_geo.loc[intra_geo['Target Standardised City'].isnull() == True, 'Target Standardised City'] = intra_geo.loc[intra_geo['Target Standardised City'].isnull() == True, 'Target country']
intra_geo.loc[intra_geo['Acquiror Standardised City'].isnull() == True, 'Acquiror Standardised City'] = intra_geo.loc[intra_geo['Acquiror Standardised City'].isnull() == True, 'Acquiror country']

intra_geo_country = intra_geo.groupby(['Target country', 'Acquiror country'], dropna=False).agg({'Deal value adj' : 'sum',
                                                                                   'Target country' : 'count'})
intra_geo_country.columns = ['Deal value adj', 'Count']
intra_geo_country = intra_geo_country.reset_index()
intra_geo_country.to_csv('05_intra_country_geography.csv')

intra_country_count_target = intra_geo_country.groupby('Target country').agg({'Count' : 'sum'})
intra_country_count_target = intra_country_count_target.reset_index()
intra_target = intra_country_count_target[intra_country_count_target['Count'] < 10]['Target country'].to_list()

intra_country_count_acq = intra_geo_country.groupby('Acquiror country').agg({'Count' : 'sum'})
intra_country_count_acq = intra_country_count_acq.reset_index()
intra_acquiror = intra_country_count_acq[intra_country_count_acq['Count'] < 10]['Acquiror country'].to_list()

# adding full names and country groups ahead of data visualisation
# this is the data file from the R countrycodes package
iso = pd.read_csv('https://raw.githubusercontent.com/vincentarelbundock/countrycode/main/dictionary/codelist_panel_without_cldr.csv')

isoRR = dict(zip(iso['iso2c'], iso['region']))

intra_country_count_target[intra_country_count_target['Target country'].isin(intra_target) == True]['Target country'].apply(lambda x: isoRR.get(x))

intra_country_count_target.loc[intra_country_count_target['Target country'].isin(intra_target) == True, 'Target country'] = intra_country_count_target[intra_country_count_target['Target country'].isin(intra_target) == True]['Target country'].apply(lambda x: isoRR.get(x))



intra_geo_sankey = intra_geo.groupby(['Target Standardised City', 'Acquiror Standardised City'], dropna=False).agg({'Deal value adj' : 'sum',
                                                                                   'Acquiror Standardised City' : 'count'})

intra_geo_sankey.columns = ['Deal value adj', 'Count']
intra_geo_sankey = intra_geo_sankey.reset_index()

intra_geo_sankey['Target Standardised City'] = intra_geo_sankey['Target Standardised City'].apply(lambda x: re.sub(r'\[\(\"', '', x))
intra_geo_sankey['Acquiror Standardised City'] = intra_geo_sankey['Acquiror Standardised City'].apply(lambda x: re.sub(r'\[\(\"', '', x))

intra_geo_sankey.to_csv('05_intra_geography.csv')

###################################
# inward
###################################

inward_geo = inward.groupby(['Deal Number']).agg({'Deal value adj' : lambda x: x.iat[0],
                                                  'Target Standardised City' : lambda x: Counter(x.dropna()).most_common(1),
                                                  'Acquiror Standardised City' : lambda x: Counter(x.dropna()).most_common(1),
                                                  'Target country' :  lambda x: Counter(x.dropna()).most_common(1),
                                                  'Acquiror country' : lambda x: Counter(x.dropna()).most_common(1)})

inward_geo = inward_geo.reset_index()

inward_geo['Target Standardised City'] = inward_geo['Target Standardised City'].apply(lambda x: str(x))
inward_geo['Target Standardised City'] = inward_geo['Target Standardised City'].apply(lambda x: re.sub(r"\[\(\'", '', x))
inward_geo['Target Standardised City'] = inward_geo['Target Standardised City'].apply(lambda x: re.sub(r"'[^;]*]", '', x))
inward_geo.loc[inward_geo['Target Standardised City'] == '[]', 'Target Standardised City'] = np.nan

inward_geo['Acquiror Standardised City'] = inward_geo['Acquiror Standardised City'].apply(lambda x: str(x))
inward_geo['Acquiror Standardised City'] = inward_geo['Acquiror Standardised City'].apply(lambda x: re.sub(r"\[\(\'", '', x))
inward_geo['Acquiror Standardised City'] = inward_geo['Acquiror Standardised City'].apply(lambda x: re.sub(r"'[^;]*]", '', x))
inward_geo.loc[inward_geo['Acquiror Standardised City'] == '[]', 'Acquiror Standardised City'] = np.nan


inward_geo['Target country'] = inward_geo['Target country'].apply(lambda x: str(x))
inward_geo['Target country'] = inward_geo['Target country'].apply(lambda x: re.sub(r"\[\(\'", '', x))
inward_geo['Target country'] = inward_geo['Target country'].apply(lambda x: re.sub(r"'[^;]*]", '', x))
inward_geo.loc[inward_geo['Target country'] == '[]', 'Target country'] = np.nan

inward_geo['Acquiror country'] = inward_geo['Acquiror country'].apply(lambda x: str(x))
inward_geo['Acquiror country'] = inward_geo['Acquiror country'].apply(lambda x: re.sub(r"\[\(\'", '', x))
inward_geo['Acquiror country'] = inward_geo['Acquiror country'].apply(lambda x: re.sub(r"'[^;]*]", '', x))
inward_geo.loc[inward_geo['Acquiror country'] == '[]', 'Acquiror country'] = np.nan

inward_geo.loc[inward_geo['Target Standardised City'].isnull() == True, 'Target Standardised City'] = inward_geo.loc[inward_geo['Target Standardised City'].isnull() == True, 'Target country']
inward_geo.loc[inward_geo['Acquiror Standardised City'].isnull() == True, 'Acquiror Standardised City'] = inward_geo.loc[inward_geo['Acquiror Standardised City'].isnull() == True, 'Acquiror country']


inward_geo_country = inward_geo.groupby(['Target country', 'Acquiror country'], dropna=False).agg({'Deal value adj' : 'sum',
                                                                                   'Target country' : 'count'})
inward_geo_country.columns = ['Deal value adj', 'Count']
inward_geo_country.to_csv('05_inward_country_geography.csv')



inward_geo_sankey = inward_geo.groupby(['Target Standardised City', 'Acquiror Standardised City'], dropna=False).agg({'Deal value adj' : 'sum',
                                                                                   'Target Standardised City' : 'count'})


inward_geo_sankey.columns = ['Deal value adj', 'Count']
inward_geo_sankey = inward_geo_sankey.reset_index()

inward_geo_sankey['Target Standardised City'] = inward_geo_sankey['Target Standardised City'].apply(lambda x: re.sub(r'\[\(\"', '', str(x)))
inward_geo_sankey['Acquiror Standardised City'] = inward_geo_sankey['Acquiror Standardised City'].apply(lambda x: re.sub(r'\[\(\"', '', str(x)))

inward_geo_sankey.to_csv('05_inward_geography.csv')

###################################
# outward
###################################

outward_geo = outward.groupby(['Deal Number']).agg({'Deal value adj' : lambda x: x.iat[0],
                                                  'Target Standardised City' : lambda x: Counter(x.dropna()).most_common(1),
                                                  'Acquiror Standardised City' : lambda x: Counter(x.dropna()).most_common(1),
                                                  'Target country' :  lambda x: Counter(x.dropna()).most_common(1),
                                                  'Acquiror country' : lambda x: Counter(x.dropna()).most_common(1)})

outward_geo = outward_geo.reset_index()

outward_geo['Target Standardised City'] = outward_geo['Target Standardised City'].apply(lambda x: str(x))
outward_geo['Target Standardised City'] = outward_geo['Target Standardised City'].apply(lambda x: re.sub(r"\[\(\'", '', x))
outward_geo['Target Standardised City'] = outward_geo['Target Standardised City'].apply(lambda x: re.sub(r"'[^;]*]", '', x))
outward_geo.loc[outward_geo['Target Standardised City'] == '[]', 'Target Standardised City'] = np.nan

outward_geo['Acquiror Standardised City'] = outward_geo['Acquiror Standardised City'].apply(lambda x: str(x))
outward_geo['Acquiror Standardised City'] = outward_geo['Acquiror Standardised City'].apply(lambda x: re.sub(r"\[\(\'", '', x))
outward_geo['Acquiror Standardised City'] = outward_geo['Acquiror Standardised City'].apply(lambda x: re.sub(r"'[^;]*]", '', x))
outward_geo.loc[outward_geo['Acquiror Standardised City'] == '[]', 'Acquiror Standardised City'] = np.nan


outward_geo['Target country'] = outward_geo['Target country'].apply(lambda x: str(x))
outward_geo['Target country'] = outward_geo['Target country'].apply(lambda x: re.sub(r"\[\(\'", '', x))
outward_geo['Target country'] = outward_geo['Target country'].apply(lambda x: re.sub(r"'[^;]*]", '', x))
outward_geo.loc[outward_geo['Target country'] == '[]', 'Target country'] = np.nan

outward_geo['Acquiror country'] = outward_geo['Acquiror country'].apply(lambda x: str(x))
outward_geo['Acquiror country'] = outward_geo['Acquiror country'].apply(lambda x: re.sub(r"\[\(\'", '', x))
outward_geo['Acquiror country'] = outward_geo['Acquiror country'].apply(lambda x: re.sub(r"'[^;]*]", '', x))
outward_geo.loc[outward_geo['Acquiror country'] == '[]', 'Acquiror country'] = np.nan

outward_geo.loc[outward_geo['Target Standardised City'].isnull() == True, 'Target Standardised City'] = outward_geo.loc[outward_geo['Target Standardised City'].isnull() == True, 'Target country']
outward_geo.loc[outward_geo['Acquiror Standardised City'].isnull() == True, 'Acquiror Standardised City'] = outward_geo.loc[outward_geo['Acquiror Standardised City'].isnull() == True, 'Acquiror country']

outward_geo_country = outward_geo.groupby(['Target country', 'Acquiror country'], dropna=False).agg({'Deal value adj' : 'sum',
                                                                                   'Target country' : 'count'})
outward_geo_country.columns = ['Deal value adj', 'Count']
outward_geo_country.to_csv('05_outward_country_geography.csv')

outward_geo_sankey = outward_geo.groupby(['Target Standardised City', 'Acquiror Standardised City'], dropna=False).agg({'Deal value adj' : 'sum',
                                                                                   'Acquiror Standardised City' : 'count'})


outward_geo_sankey.columns = ['Deal value adj', 'Count']
outward_geo_sankey = outward_geo_sankey.reset_index()

outward_geo_sankey['Target Standardised City'] = outward_geo_sankey['Target Standardised City'].apply(lambda x: re.sub(r'\[\(\"', '', x))
outward_geo_sankey['Acquiror Standardised City'] = outward_geo_sankey['Acquiror Standardised City'].apply(lambda x: re.sub(r'\[\(\"', '', x))

outward_geo_sankey.to_csv('05_outward_geography.csv')

## then limiting outputs by counts
## aggregating up countries with low counts into region areas for better viz
##
## as above this code repeats for inward, intra, outward with the same code being used but the direction changed

iso = pd.read_csv('https://raw.githubusercontent.com/vincentarelbundock/countrycode/main/dictionary/codelist_panel_without_cldr.csv')

iso2c = dict(zip(iso['iso2c'], iso['country.name.en']))
isoRR = dict(zip(iso['iso2c'], iso['region']))

intra_geo_country.columns = ['Target Country Code', 'Acquiror Country Code'  ,'Deal value adj','Count']

intra_geo_country['Target name'] = intra_geo_country['Target Country Code'].apply(lambda x: iso2c.get(x))
intra_geo_country['Acquiror name'] = intra_geo_country['Acquiror Country Code'].apply(lambda x: iso2c.get(x))
intra_geo_country['Target region'] = intra_geo_country['Target Country Code'].apply(lambda x: isoRR.get(x))
intra_geo_country['Acquiror region'] = intra_geo_country['Acquiror Country Code'].apply(lambda x: isoRR.get(x))

# not all countries are matched, doing this manually

# missing_codes = set(list(intra_geo_country[intra_geo_country['Target name'].isnull() == True]['Target Country Code']) + list(intra_geo_country[intra_geo_country['Acquiror name'].isnull() == True]['Acquiror Country Code']))

intra_geo_country.loc[intra_geo_country['Target Country Code'] == 'BM', 'Target name'] = 'Bermuda'
intra_geo_country.loc[intra_geo_country['Target Country Code'] == 'KY', 'Target name'] = 'Cayman Islands'
intra_geo_country.loc[intra_geo_country['Target Country Code'] == 'PF', 'Target name'] = 'French Polynesia'
intra_geo_country.loc[intra_geo_country['Target Country Code'] == 'PR', 'Target name'] = 'Puerto Rico'
intra_geo_country.loc[intra_geo_country['Target Country Code'] == 'VG', 'Target name'] = 'British Virgin Islands'

intra_geo_country.loc[intra_geo_country['Acquiror Country Code'] == 'BM', 'Acquiror name'] = 'Bermuda'
intra_geo_country.loc[intra_geo_country['Acquiror Country Code'] == 'KY', 'Acquiror name'] = 'Cayman Islands'
intra_geo_country.loc[intra_geo_country['Acquiror Country Code'] == 'PF', 'Acquiror name'] = 'French Polynesia'
intra_geo_country.loc[intra_geo_country['Acquiror Country Code'] == 'PR', 'Acquiror name'] = 'Puerto Rico'
intra_geo_country.loc[intra_geo_country['Acquiror Country Code'] == 'VG', 'Acquiror name'] = 'British Virgin Islands'

intra_geo_country.loc[intra_geo_country['Target Country Code'] == 'BM', 'Target region'] = 'Latin America & Caribbean'
intra_geo_country.loc[intra_geo_country['Target Country Code'] == 'KY', 'Target region'] = 'Latin America & Caribbean'
intra_geo_country.loc[intra_geo_country['Target Country Code'] == 'PF', 'Target region'] = 'Latin America & Caribbean'
intra_geo_country.loc[intra_geo_country['Target Country Code'] == 'PR', 'Target region'] = 'Latin America & Caribbean'
intra_geo_country.loc[intra_geo_country['Target Country Code'] == 'VG', 'Target region'] = 'Latin America & Caribbean'

intra_geo_country.loc[intra_geo_country['Acquiror Country Code'] == 'BM', 'Acquiror region'] = 'Latin America & Caribbean'
intra_geo_country.loc[intra_geo_country['Acquiror Country Code'] == 'KY', 'Acquiror region'] = 'Latin America & Caribbean'
intra_geo_country.loc[intra_geo_country['Acquiror Country Code'] == 'PF', 'Acquiror region'] = 'Latin America & Caribbean'
intra_geo_country.loc[intra_geo_country['Acquiror Country Code'] == 'PR', 'Acquiror region'] = 'Latin America & Caribbean'
intra_geo_country.loc[intra_geo_country['Acquiror Country Code'] == 'VG', 'Acquiror region'] = 'Latin America & Caribbean'


intra_geo_country.to_csv('05_intra_country_geography_all.csv')

## Percent counts for the articles

out_pct = intra_geo_country.groupby(['Acquiror Country Code']).agg({'Count' : 'sum'})
out_pct = out_pct.reset_index()
out_pct['PERCENT'] = out_pct['Count'] / out_pct['Count'].sum() * 100

out_pct.to_csv('05_intra_country_geography_all_count_percent.csv')


## doing some additional region reclassification for the paper

intra_geo_country.loc[intra_geo_country['Target region'] == 'South Asia', 'Target region'] = 'Asia'
intra_geo_country.loc[intra_geo_country['Acquiror region'] == 'South Asia', 'Acquiror region']= 'Asia'

intra_geo_country.loc[intra_geo_country['Target region'] == 'East Asia & Pacific', 'Target region'] = 'Asia'
intra_geo_country.loc[intra_geo_country['Acquiror region'] == 'East Asia & Pacific', 'Acquiror region'] = 'Asia'

# Separating Caribbean

intra_geo_country.loc[intra_geo_country['Target name'] == 'British Virgin Islands', 'Target region'] = 'Caribbean'
intra_geo_country.loc[intra_geo_country['Acquiror name'] == 'British Virgin Islands', 'Acquiror region'] = 'Caribbean'

intra_geo_country.loc[intra_geo_country['Target name'] == 'Cayman Islands', 'Target region'] = 'Caribbean'
intra_geo_country.loc[intra_geo_country['Acquiror name'] == 'Cayman Islands', 'Acquiror region'] = 'Caribbean'

intra_geo_country.loc[intra_geo_country['Target name'] == 'Israel', 'Target region'] = 'Africa & Middle East'
intra_geo_country.loc[intra_geo_country['Acquiror name'] == 'Israel', 'Acquiror region'] = 'Africa and Middle East'

intra_geo_country.loc[intra_geo_country['Target name'] == 'South Africa', 'Target region'] = 'Africa & Middle East'
intra_geo_country.loc[intra_geo_country['Acquiror name'] == 'South Africa', 'Acquiror region'] = 'Africa and Middle East'

# heatmap for countries with more than 10 deals

acq_count = intra_geo_country.groupby('Acquiror Country Code').agg({'Count' : 'sum'})
acq_count = acq_count.reset_index()
below10acq = list(acq_count[acq_count['Count'] < 10]['Acquiror Country Code'])

tg_count = intra_geo_country.groupby('Target Country Code').agg({'Count' : 'sum'})
tg_count = tg_count.reset_index()
below10tg = list(tg_count[tg_count['Count'] < 10]['Target Country Code'])

intra_geo_country.loc[intra_geo_country['Acquiror Country Code'].isin(below10acq) == True, 'Acquiror name'] = intra_geo_country.loc[intra_geo_country['Acquiror Country Code'].isin(below10acq) == True, 'Acquiror region'] 

intra_geo_country.loc[intra_geo_country['Target Country Code'].isin(below10tg) == True, 'Target name'] = intra_geo_country.loc[intra_geo_country['Target Country Code'].isin(below10tg) == True, 'Target region'] 

intra_geo_country.to_csv('05_intra_country_geography_above_10.csv')

# heatmap for countries with more than 20 deals

acq_count = intra_geo_country.groupby('Acquiror Country Code').agg({'Count' : 'sum'})
acq_count = acq_count.reset_index()
below20acq = list(acq_count[acq_count['Count'] < 20]['Acquiror Country Code'])

tg_count = intra_geo_country.groupby('Target Country Code').agg({'Count' : 'sum'})
tg_count = tg_count.reset_index()
below20tg = list(tg_count[tg_count['Count'] < 20]['Target Country Code'])

intra_geo_country.loc[intra_geo_country['Acquiror Country Code'].isin(below20acq) == True, 'Acquiror name'] = intra_geo_country.loc[intra_geo_country['Acquiror Country Code'].isin(below20acq) == True, 'Acquiror region'] 

intra_geo_country.loc[intra_geo_country['Target Country Code'].isin(below20tg) == True, 'Target name'] = intra_geo_country.loc[intra_geo_country['Target Country Code'].isin(below20tg) == True, 'Target region'] 

acq_count = intra_geo_country.groupby('Acquiror name').agg({'Count' : 'sum'})
acq_count = acq_count.reset_index()
below20acq = list(acq_count[acq_count['Count'] < 20]['Acquiror name'])

tg_count = intra_geo_country.groupby('Target name').agg({'Count' : 'sum'})
tg_count = tg_count.reset_index()
below20tg = list(tg_count[tg_count['Count'] < 20]['Target name'])

intra_geo_country.loc[intra_geo_country['Acquiror name'].isin(below20acq) == True, 'Acquiror name'] = 'Other'

intra_geo_country.loc[intra_geo_country['Target name'].isin(below20tg) == True, 'Target name'] = 'Other'

intra_geo_country.to_csv('05_intra_country_geography_above_20.csv')


## then all the above code again but for inward

iso = pd.read_csv('https://raw.githubusercontent.com/vincentarelbundock/countrycode/main/dictionary/codelist_panel_without_cldr.csv')

iso2c = dict(zip(iso['iso2c'], iso['country.name.en']))
isoRR = dict(zip(iso['iso2c'], iso['region']))

inward_geo_country = inward_geo_country.reset_index()

inward_geo_country.columns = ['Target Country Code', 'Acquiror Country Code'  ,'Deal value adj','Count']

inward_geo_country['Target name'] = inward_geo_country['Target Country Code'].apply(lambda x: iso2c.get(x))
inward_geo_country['Acquiror name'] = inward_geo_country['Acquiror Country Code'].apply(lambda x: iso2c.get(x))
inward_geo_country['Target region'] = inward_geo_country['Target Country Code'].apply(lambda x: isoRR.get(x))
inward_geo_country['Acquiror region'] = inward_geo_country['Acquiror Country Code'].apply(lambda x: isoRR.get(x))

# not all countries are matched, doing this manually

# missing_codes = set(list(inward_geo_country[inward_geo_country['Target name'].isnull() == True]['Target Country Code']) + list(inward_geo_country[inward_geo_country['Acquiror name'].isnull() == True]['Acquiror Country Code']))

inward_geo_country.loc[inward_geo_country['Target Country Code'] == 'BM', 'Target name'] = 'Bermuda'
inward_geo_country.loc[inward_geo_country['Target Country Code'] == 'KY', 'Target name'] = 'Cayman Islands'
inward_geo_country.loc[inward_geo_country['Target Country Code'] == 'PF', 'Target name'] = 'French Polynesia'
inward_geo_country.loc[inward_geo_country['Target Country Code'] == 'PR', 'Target name'] = 'Puerto Rico'
inward_geo_country.loc[inward_geo_country['Target Country Code'] == 'VG', 'Target name'] = 'British Virgin Islands'

inward_geo_country.loc[inward_geo_country['Acquiror Country Code'] == 'BM', 'Acquiror name'] = 'Bermuda'
inward_geo_country.loc[inward_geo_country['Acquiror Country Code'] == 'KY', 'Acquiror name'] = 'Cayman Islands'
inward_geo_country.loc[inward_geo_country['Acquiror Country Code'] == 'PF', 'Acquiror name'] = 'French Polynesia'
inward_geo_country.loc[inward_geo_country['Acquiror Country Code'] == 'PR', 'Acquiror name'] = 'Puerto Rico'
inward_geo_country.loc[inward_geo_country['Acquiror Country Code'] == 'VG', 'Acquiror name'] = 'British Virgin Islands'

inward_geo_country.loc[inward_geo_country['Target Country Code'] == 'BM', 'Target region'] = 'Latin America & Caribbean'
inward_geo_country.loc[inward_geo_country['Target Country Code'] == 'KY', 'Target region'] = 'Latin America & Caribbean'
inward_geo_country.loc[inward_geo_country['Target Country Code'] == 'PF', 'Target region'] = 'Latin America & Caribbean'
inward_geo_country.loc[inward_geo_country['Target Country Code'] == 'PR', 'Target region'] = 'Latin America & Caribbean'
inward_geo_country.loc[inward_geo_country['Target Country Code'] == 'VG', 'Target region'] = 'Latin America & Caribbean'

inward_geo_country.loc[inward_geo_country['Acquiror Country Code'] == 'BM', 'Acquiror region'] = 'Latin America & Caribbean'
inward_geo_country.loc[inward_geo_country['Acquiror Country Code'] == 'KY', 'Acquiror region'] = 'Latin America & Caribbean'
inward_geo_country.loc[inward_geo_country['Acquiror Country Code'] == 'PF', 'Acquiror region'] = 'Latin America & Caribbean'
inward_geo_country.loc[inward_geo_country['Acquiror Country Code'] == 'PR', 'Acquiror region'] = 'Latin America & Caribbean'
inward_geo_country.loc[inward_geo_country['Acquiror Country Code'] == 'VG', 'Acquiror region'] = 'Latin America & Caribbean'


inward_geo_country.to_csv('05_inward_country_geography_all.csv')

## Pct

out_pct = inward_geo_country.groupby(['Acquiror Country Code']).agg({'Count' : 'sum'})
out_pct = out_pct.reset_index()
out_pct['PERCENT'] = out_pct['Count'] / out_pct['Count'].sum() * 100

out_pct.to_csv('05_inward_country_geography_all_count_percent.csv')

## doing some additional region reclassification for the paper

inward_geo_country.loc[inward_geo_country['Target region'] == 'South Asia', 'Target region'] = 'Asia'
inward_geo_country.loc[inward_geo_country['Acquiror region'] == 'South Asia', 'Acquiror region']= 'Asia'

inward_geo_country.loc[inward_geo_country['Target region'] == 'East Asia & Pacific', 'Target region'] = 'Asia'
inward_geo_country.loc[inward_geo_country['Acquiror region'] == 'East Asia & Pacific', 'Acquiror region'] = 'Asia'

# Separating Caribbean

inward_geo_country.loc[inward_geo_country['Target name'] == 'British Virgin Islands', 'Target region'] = 'Caribbean'
inward_geo_country.loc[inward_geo_country['Acquiror name'] == 'British Virgin Islands', 'Acquiror region'] = 'Caribbean'

inward_geo_country.loc[inward_geo_country['Target name'] == 'Cayman Islands', 'Target region'] = 'Caribbean'
inward_geo_country.loc[inward_geo_country['Acquiror name'] == 'Cayman Islands', 'Acquiror region'] = 'Caribbean'

inward_geo_country.loc[inward_geo_country['Target name'] == 'Israel', 'Target region'] = 'Africa & Middle East'
inward_geo_country.loc[inward_geo_country['Acquiror name'] == 'Israel', 'Acquiror region'] = 'Africa and Middle East'

inward_geo_country.loc[inward_geo_country['Target name'] == 'South Africa', 'Target region'] = 'Africa & Middle East'
inward_geo_country.loc[inward_geo_country['Acquiror name'] == 'South Africa', 'Acquiror region'] = 'Africa and Middle East'

# heatmap for countries with more than 10 deals

acq_count = inward_geo_country.groupby('Acquiror Country Code').agg({'Count' : 'sum'})
acq_count = acq_count.reset_index()
below10acq = list(acq_count[acq_count['Count'] < 10]['Acquiror Country Code'])

tg_count = inward_geo_country.groupby('Target Country Code').agg({'Count' : 'sum'})
tg_count = tg_count.reset_index()
below10tg = list(tg_count[tg_count['Count'] < 10]['Target Country Code'])

inward_geo_country.loc[inward_geo_country['Acquiror Country Code'].isin(below10acq) == True, 'Acquiror name'] = inward_geo_country.loc[inward_geo_country['Acquiror Country Code'].isin(below10acq) == True, 'Acquiror region'] 

inward_geo_country.loc[inward_geo_country['Target Country Code'].isin(below10tg) == True, 'Target name'] = inward_geo_country.loc[inward_geo_country['Target Country Code'].isin(below10tg) == True, 'Target region'] 

inward_geo_country.to_csv('05_inward_country_geography_above_10.csv')

# heatmap for countries with more than 20 deals

acq_count = inward_geo_country.groupby('Acquiror Country Code').agg({'Count' : 'sum'})
acq_count = acq_count.reset_index()
below20acq = list(acq_count[acq_count['Count'] < 20]['Acquiror Country Code'])

tg_count = inward_geo_country.groupby('Target Country Code').agg({'Count' : 'sum'})
tg_count = tg_count.reset_index()
below20tg = list(tg_count[tg_count['Count'] < 20]['Target Country Code'])

inward_geo_country.loc[inward_geo_country['Acquiror Country Code'].isin(below20acq) == True, 'Acquiror name'] = inward_geo_country.loc[inward_geo_country['Acquiror Country Code'].isin(below20acq) == True, 'Acquiror region'] 

inward_geo_country.loc[inward_geo_country['Target Country Code'].isin(below20tg) == True, 'Target name'] = inward_geo_country.loc[inward_geo_country['Target Country Code'].isin(below20tg) == True, 'Target region'] 

acq_count = inward_geo_country.groupby('Acquiror name').agg({'Count' : 'sum'})
acq_count = acq_count.reset_index()
below20acq = list(acq_count[acq_count['Count'] < 20]['Acquiror name'])

tg_count = inward_geo_country.groupby('Target name').agg({'Count' : 'sum'})
tg_count = tg_count.reset_index()
below20tg = list(tg_count[tg_count['Count'] < 20]['Target name'])

inward_geo_country.loc[inward_geo_country['Acquiror name'].isin(below20acq) == True, 'Acquiror name'] = 'Other'

inward_geo_country.loc[inward_geo_country['Target name'].isin(below20tg) == True, 'Target name'] = 'Other'

inward_geo_country.loc[inward_geo_country['Acquiror name'].isnull(), 'Acquiror name'] = 'Asia'
inward_geo_country.loc[inward_geo_country['Acquiror region'].isnull(), 'Acquiror region'] = 'Asia'

inward_geo_country.to_csv('05_inward_country_geography_above_20.csv')


### outward 


iso = pd.read_csv('https://raw.githubusercontent.com/vincentarelbundock/countrycode/main/dictionary/codelist_panel_without_cldr.csv')

iso2c = dict(zip(iso['iso2c'], iso['country.name.en']))
isoRR = dict(zip(iso['iso2c'], iso['region']))

outward_geo_country = outward_geo_country.reset_index()

outward_geo_country.columns = ['Target Country Code', 'Acquiror Country Code'  ,'Deal value adj','Count']

outward_geo_country['Target name'] = outward_geo_country['Target Country Code'].apply(lambda x: iso2c.get(x))
outward_geo_country['Acquiror name'] = outward_geo_country['Acquiror Country Code'].apply(lambda x: iso2c.get(x))
outward_geo_country['Target region'] = outward_geo_country['Target Country Code'].apply(lambda x: isoRR.get(x))
outward_geo_country['Acquiror region'] = outward_geo_country['Acquiror Country Code'].apply(lambda x: isoRR.get(x))

# not all countries are matched, doing this manually

# missing_codes = set(list(outward_geo_country[outward_geo_country['Target name'].isnull() == True]['Target Country Code']) + list(outward_geo_country[outward_geo_country['Acquiror name'].isnull() == True]['Acquiror Country Code']))

outward_geo_country.loc[outward_geo_country['Target Country Code'] == 'BM', 'Target name'] = 'Bermuda'
outward_geo_country.loc[outward_geo_country['Target Country Code'] == 'KY', 'Target name'] = 'Cayman Islands'
outward_geo_country.loc[outward_geo_country['Target Country Code'] == 'PF', 'Target name'] = 'French Polynesia'
outward_geo_country.loc[outward_geo_country['Target Country Code'] == 'PR', 'Target name'] = 'Puerto Rico'
outward_geo_country.loc[outward_geo_country['Target Country Code'] == 'VG', 'Target name'] = 'British Virgin Islands'

outward_geo_country.loc[outward_geo_country['Acquiror Country Code'] == 'BM', 'Acquiror name'] = 'Bermuda'
outward_geo_country.loc[outward_geo_country['Acquiror Country Code'] == 'KY', 'Acquiror name'] = 'Cayman Islands'
outward_geo_country.loc[outward_geo_country['Acquiror Country Code'] == 'PF', 'Acquiror name'] = 'French Polynesia'
outward_geo_country.loc[outward_geo_country['Acquiror Country Code'] == 'PR', 'Acquiror name'] = 'Puerto Rico'
outward_geo_country.loc[outward_geo_country['Acquiror Country Code'] == 'VG', 'Acquiror name'] = 'British Virgin Islands'

outward_geo_country.loc[outward_geo_country['Target Country Code'] == 'BM', 'Target region'] = 'Latin America & Caribbean'
outward_geo_country.loc[outward_geo_country['Target Country Code'] == 'KY', 'Target region'] = 'Latin America & Caribbean'
outward_geo_country.loc[outward_geo_country['Target Country Code'] == 'PF', 'Target region'] = 'Latin America & Caribbean'
outward_geo_country.loc[outward_geo_country['Target Country Code'] == 'PR', 'Target region'] = 'Latin America & Caribbean'
outward_geo_country.loc[outward_geo_country['Target Country Code'] == 'VG', 'Target region'] = 'Latin America & Caribbean'

outward_geo_country.loc[outward_geo_country['Acquiror Country Code'] == 'BM', 'Acquiror region'] = 'Latin America & Caribbean'
outward_geo_country.loc[outward_geo_country['Acquiror Country Code'] == 'KY', 'Acquiror region'] = 'Latin America & Caribbean'
outward_geo_country.loc[outward_geo_country['Acquiror Country Code'] == 'PF', 'Acquiror region'] = 'Latin America & Caribbean'
outward_geo_country.loc[outward_geo_country['Acquiror Country Code'] == 'PR', 'Acquiror region'] = 'Latin America & Caribbean'
outward_geo_country.loc[outward_geo_country['Acquiror Country Code'] == 'VG', 'Acquiror region'] = 'Latin America & Caribbean'


outward_geo_country.to_csv('05_outward_country_geography_all.csv')

## Pcts

out_pct = outward_geo_country.groupby(['Acquiror Country Code']).agg({'Count' : 'sum'})
out_pct = out_pct.reset_index()
out_pct['PERCENT'] = out_pct['Count'] / out_pct['Count'].sum() * 100

out_pct.to_csv('05_outward_country_geography_all_count_percent.csv')



## doing some additional region reclassification for the paper

outward_geo_country.loc[outward_geo_country['Target region'] == 'South Asia', 'Target region'] = 'Asia'
outward_geo_country.loc[outward_geo_country['Acquiror region'] == 'South Asia', 'Acquiror region']= 'Asia'

outward_geo_country.loc[outward_geo_country['Target region'] == 'East Asia & Pacific', 'Target region'] = 'Asia'
outward_geo_country.loc[outward_geo_country['Acquiror region'] == 'East Asia & Pacific', 'Acquiror region'] = 'Asia'

# Separating Caribbean

outward_geo_country.loc[outward_geo_country['Target name'] == 'British Virgin Islands', 'Target region'] = 'Caribbean'
outward_geo_country.loc[outward_geo_country['Acquiror name'] == 'British Virgin Islands', 'Acquiror region'] = 'Caribbean'

outward_geo_country.loc[outward_geo_country['Target name'] == 'Cayman Islands', 'Target region'] = 'Caribbean'
outward_geo_country.loc[outward_geo_country['Acquiror name'] == 'Cayman Islands', 'Acquiror region'] = 'Caribbean'

outward_geo_country.loc[outward_geo_country['Target name'] == 'Israel', 'Target region'] = 'Africa & Middle East'
outward_geo_country.loc[outward_geo_country['Acquiror name'] == 'Israel', 'Acquiror region'] = 'Africa and Middle East'

outward_geo_country.loc[outward_geo_country['Target name'] == 'South Africa', 'Target region'] = 'Africa & Middle East'
outward_geo_country.loc[outward_geo_country['Acquiror name'] == 'South Africa', 'Acquiror region'] = 'Africa and Middle East'

# heatmap for countries with more than 10 deals

acq_count = outward_geo_country.groupby('Acquiror Country Code').agg({'Count' : 'sum'})
acq_count = acq_count.reset_index()
below10acq = list(acq_count[acq_count['Count'] < 10]['Acquiror Country Code'])

tg_count = outward_geo_country.groupby('Target Country Code').agg({'Count' : 'sum'})
tg_count = tg_count.reset_index()
below10tg = list(tg_count[tg_count['Count'] < 10]['Target Country Code'])

outward_geo_country.loc[outward_geo_country['Acquiror Country Code'].isin(below10acq) == True, 'Acquiror name'] = outward_geo_country.loc[outward_geo_country['Acquiror Country Code'].isin(below10acq) == True, 'Acquiror region'] 

outward_geo_country.loc[outward_geo_country['Target Country Code'].isin(below10tg) == True, 'Target name'] = outward_geo_country.loc[outward_geo_country['Target Country Code'].isin(below10tg) == True, 'Target region'] 

outward_geo_country.to_csv('05_outward_country_geography_above_10.csv')
# heatmap for countries with more than 20 deals

acq_count = outward_geo_country.groupby('Acquiror Country Code').agg({'Count' : 'sum'})
acq_count = acq_count.reset_index()
below20acq = list(acq_count[acq_count['Count'] < 20]['Acquiror Country Code'])

tg_count = outward_geo_country.groupby('Target Country Code').agg({'Count' : 'sum'})
tg_count = tg_count.reset_index()
below20tg = list(tg_count[tg_count['Count'] < 20]['Target Country Code'])

outward_geo_country.loc[outward_geo_country['Acquiror Country Code'].isin(below20acq) == True, 'Acquiror name'] = outward_geo_country.loc[outward_geo_country['Acquiror Country Code'].isin(below20acq) == True, 'Acquiror region'] 

outward_geo_country.loc[outward_geo_country['Target Country Code'].isin(below20tg) == True, 'Target name'] = outward_geo_country.loc[outward_geo_country['Target Country Code'].isin(below20tg) == True, 'Target region'] 

acq_count = outward_geo_country.groupby('Acquiror name').agg({'Count' : 'sum'})
acq_count = acq_count.reset_index()
below20acq = list(acq_count[acq_count['Count'] < 20]['Acquiror name'])

tg_count = outward_geo_country.groupby('Target name').agg({'Count' : 'sum'})
tg_count = tg_count.reset_index()
below20tg = list(tg_count[tg_count['Count'] < 20]['Target name'])

outward_geo_country.loc[outward_geo_country['Acquiror name'].isin(below20acq) == True, 'Acquiror name'] = 'Other'

outward_geo_country.loc[outward_geo_country['Target name'].isin(below20tg) == True, 'Target name'] = 'Other'

outward_geo_country.to_csv('05_outward_country_geography_above_20.csv')

################
### then all over again but by city!
################

intra_geo = intra.groupby(['Deal Number']).agg({'Deal value adj' : lambda x: x.iat[0],
                                                  'Target Standardised City' : lambda x: Counter(x.dropna()).most_common(1),
                                                  'Acquiror Standardised City' : lambda x: Counter(x.dropna()).most_common(1),
                                                  'Target country' :  lambda x: Counter(x.dropna()).most_common(1),
                                                  'Acquiror country' : lambda x: Counter(x.dropna()).most_common(1)})

intra_geo = intra_geo.reset_index()

intra_geo['Target Standardised City'] = intra_geo['Target Standardised City'].apply(lambda x: str(x))
intra_geo['Target Standardised City'] = intra_geo['Target Standardised City'].apply(lambda x: re.sub(r"\[\(\'", '', x))
intra_geo['Target Standardised City'] = intra_geo['Target Standardised City'].apply(lambda x: re.sub(r"'[^;]*]", '', x))
intra_geo.loc[intra_geo['Target Standardised City'] == '[]', 'Target Standardised City'] = np.nan

intra_geo['Acquiror Standardised City'] = intra_geo['Acquiror Standardised City'].apply(lambda x: str(x))
intra_geo['Acquiror Standardised City'] = intra_geo['Acquiror Standardised City'].apply(lambda x: re.sub(r"\[\(\'", '', x))
intra_geo['Acquiror Standardised City'] = intra_geo['Acquiror Standardised City'].apply(lambda x: re.sub(r"'[^;]*]", '', x))
intra_geo.loc[intra_geo['Acquiror Standardised City'] == '[]', 'Acquiror Standardised City'] = np.nan


intra_geo['Target country'] = intra_geo['Target country'].apply(lambda x: str(x))
intra_geo['Target country'] = intra_geo['Target country'].apply(lambda x: re.sub(r"\[\(\'", '', x))
intra_geo['Target country'] = intra_geo['Target country'].apply(lambda x: re.sub(r"'[^;]*]", '', x))
intra_geo.loc[intra_geo['Target country'] == '[]', 'Target country'] = np.nan

intra_geo['Acquiror country'] = intra_geo['Acquiror country'].apply(lambda x: str(x))
intra_geo['Acquiror country'] = intra_geo['Acquiror country'].apply(lambda x: re.sub(r"\[\(\'", '', x))
intra_geo['Acquiror country'] = intra_geo['Acquiror country'].apply(lambda x: re.sub(r"'[^;]*]", '', x))
intra_geo.loc[intra_geo['Acquiror country'] == '[]', 'Acquiror country'] = np.nan

intra_geo.loc[intra_geo['Target Standardised City'].isnull() == True, 'Target Standardised City'] = intra_geo.loc[intra_geo['Target Standardised City'].isnull() == True, 'Target country']
intra_geo.loc[intra_geo['Acquiror Standardised City'].isnull() == True, 'Acquiror Standardised City'] = intra_geo.loc[intra_geo['Acquiror Standardised City'].isnull() == True, 'Acquiror country']

### then doing regions

iso = pd.read_csv('https://raw.githubusercontent.com/vincentarelbundock/countrycode/main/dictionary/codelist_panel_without_cldr.csv')

iso2c = dict(zip(iso['iso2c'], iso['country.name.en']))
isoRR = dict(zip(iso['iso2c'], iso['region']))

intra_geo.columns = ['Deal Number', 'Deal value adj', 'Target Standardised City', 'Acquiror Standardised City', 'Target Country Code', 'Acquiror Country Code']

intra_geo['Target name'] = intra_geo['Target Country Code'].apply(lambda x: iso2c.get(x))
intra_geo['Acquiror name'] = intra_geo['Acquiror Country Code'].apply(lambda x: iso2c.get(x))
intra_geo['Target region'] = intra_geo['Target Country Code'].apply(lambda x: isoRR.get(x))
intra_geo['Acquiror region'] = intra_geo['Acquiror Country Code'].apply(lambda x: isoRR.get(x))

# not all countries are matched, doing this manually

# missing_codes = set(list(intra_geo[intra_geo['Target name'].isnull() == True]['Target Country Code']) + list(intra_geo[intra_geo['Acquiror name'].isnull() == True]['Acquiror Country Code']))

intra_geo.loc[intra_geo['Target Country Code'] == 'BM', 'Target name'] = 'Bermuda'
intra_geo.loc[intra_geo['Target Country Code'] == 'KY', 'Target name'] = 'Cayman Islands'
intra_geo.loc[intra_geo['Target Country Code'] == 'PF', 'Target name'] = 'French Polynesia'
intra_geo.loc[intra_geo['Target Country Code'] == 'PR', 'Target name'] = 'Puerto Rico'
intra_geo.loc[intra_geo['Target Country Code'] == 'VG', 'Target name'] = 'British Virgin Islands'

intra_geo.loc[intra_geo['Acquiror Country Code'] == 'BM', 'Acquiror name'] = 'Bermuda'
intra_geo.loc[intra_geo['Acquiror Country Code'] == 'KY', 'Acquiror name'] = 'Cayman Islands'
intra_geo.loc[intra_geo['Acquiror Country Code'] == 'PF', 'Acquiror name'] = 'French Polynesia'
intra_geo.loc[intra_geo['Acquiror Country Code'] == 'PR', 'Acquiror name'] = 'Puerto Rico'
intra_geo.loc[intra_geo['Acquiror Country Code'] == 'VG', 'Acquiror name'] = 'British Virgin Islands'

intra_geo.loc[intra_geo['Target Country Code'] == 'BM', 'Target region'] = 'Latin America & Caribbean'
intra_geo.loc[intra_geo['Target Country Code'] == 'KY', 'Target region'] = 'Latin America & Caribbean'
intra_geo.loc[intra_geo['Target Country Code'] == 'PF', 'Target region'] = 'Latin America & Caribbean'
intra_geo.loc[intra_geo['Target Country Code'] == 'PR', 'Target region'] = 'Latin America & Caribbean'
intra_geo.loc[intra_geo['Target Country Code'] == 'VG', 'Target region'] = 'Latin America & Caribbean'

intra_geo.loc[intra_geo['Acquiror Country Code'] == 'BM', 'Acquiror region'] = 'Latin America & Caribbean'
intra_geo.loc[intra_geo['Acquiror Country Code'] == 'KY', 'Acquiror region'] = 'Latin America & Caribbean'
intra_geo.loc[intra_geo['Acquiror Country Code'] == 'PF', 'Acquiror region'] = 'Latin America & Caribbean'
intra_geo.loc[intra_geo['Acquiror Country Code'] == 'PR', 'Acquiror region'] = 'Latin America & Caribbean'
intra_geo.loc[intra_geo['Acquiror Country Code'] == 'VG', 'Acquiror region'] = 'Latin America & Caribbean'

# x.iat[0] returns the first value in the row of this group, i.e. in this case the country or region in which the city is located
intra_geo_sankey = intra_geo.groupby(['Target Standardised City', 'Acquiror Standardised City'], dropna=False).agg({'Deal value adj' : 'sum',
                                                                                                      'Acquiror Standardised City' : 'count',
                                                                                                      'Target name' : lambda x: x.iat[0],
                                                                                                      'Acquiror name' : lambda x: x.iat[0],
                                                                                                      'Target region' : lambda x: x.iat[0],
                                                                                                      'Acquiror region' : lambda x: x.iat[0]})

intra_geo_sankey.columns = ['Deal value adj', 'Count', 'Target name', 'Acquiror name', 'Target region', 'Acquiror region']

intra_geo_sankey = intra_geo_sankey.reset_index()

intra_geo_sankey.to_csv('05_intra_city_all.csv')

## Percent counts for the articles

out_pct = intra_geo_sankey.groupby(['Acquiror Standardised City']).agg({'Count' : 'sum'})
out_pct = out_pct.reset_index()
out_pct['PERCENT'] = out_pct['Count'] / out_pct['Count'].sum() * 100

out_pct.to_csv('05_intra_city_all_pct.csv')


acq_count = intra_geo_sankey.groupby('Acquiror Standardised City').agg({'Count' : 'sum'})
acq_count = acq_count.reset_index()
below10acq = list(acq_count[acq_count['Count'] < 10]['Acquiror Standardised City'])
abv10acq = list(acq_count[acq_count['Count'] > 10]['Acquiror Standardised City'])


tg_count = intra_geo_sankey.groupby('Target Standardised City').agg({'Count' : 'sum'})
tg_count = tg_count.reset_index()
below10tg = list(tg_count[tg_count['Count'] < 10]['Target Standardised City'])

intra_geo_sankey.loc[intra_geo_sankey['Acquiror Standardised City'].isin(below10acq) == True, 'Acquiror Standardised City'] = intra_geo_sankey.loc[intra_geo_sankey['Acquiror Standardised City'].isin(below10acq) == True, 'Acquiror name'] 

intra_geo_sankey.loc[intra_geo_sankey['Target Standardised City'].isin(below10tg) == True, 'Target Standardised City'] = intra_geo_sankey.loc[intra_geo_sankey['Target Standardised City'].isin(below10tg) == True, 'Target name'] 

intra_geo_sankey_above_10 = intra_geo_sankey[intra_geo_sankey['Acquiror Standardised City'].isin(abv10acq) == True]
#
intra_geo_sankey_above_10.to_csv('05_intra_city_above_10.csv')


intra_geo_sankey['Target Standardised City'] = intra_geo_sankey['Target Standardised City'].apply(lambda x: str(x))
intra_geo_sankey['Target Standardised City'] = intra_geo_sankey['Target Standardised City'].apply(lambda x: re.sub(r"\[\(\'", '', x))
intra_geo_sankey['Target Standardised City'] = intra_geo_sankey['Target Standardised City'].apply(lambda x: re.sub(r"'[^;]*]", '', x))
intra_geo_sankey.loc[intra_geo_sankey['Target Standardised City'] == '[]', 'Target Standardised City'] = np.nan

intra_geo_sankey['Acquiror Standardised City'] = intra_geo_sankey['Acquiror Standardised City'].apply(lambda x: str(x))
intra_geo_sankey['Acquiror Standardised City'] = intra_geo_sankey['Acquiror Standardised City'].apply(lambda x: re.sub(r"\[\(\'", '', x))
intra_geo_sankey['Acquiror Standardised City'] = intra_geo_sankey['Acquiror Standardised City'].apply(lambda x: re.sub(r"'[^;]*]", '', x))
intra_geo_sankey.loc[intra_geo_sankey['Acquiror Standardised City'] == '[]', 'Acquiror Standardised City'] = np.nan

#################
## by city inward
#################

inward_geo = inward.groupby(['Deal Number']).agg({'Deal value adj' : lambda x: x.iat[0],
                                                  'Target Standardised City' : lambda x: Counter(x.dropna()).most_common(1),
                                                  'Acquiror Standardised City' : lambda x: Counter(x.dropna()).most_common(1),
                                                  'Target country' :  lambda x: Counter(x.dropna()).most_common(1),
                                                  'Acquiror country' : lambda x: Counter(x.dropna()).most_common(1)})

inward_geo = inward_geo.reset_index()

inward_geo['Target Standardised City'] = inward_geo['Target Standardised City'].apply(lambda x: str(x))
inward_geo['Target Standardised City'] = inward_geo['Target Standardised City'].apply(lambda x: re.sub(r"\[\(\'", '', str(x)))
inward_geo['Target Standardised City'] = inward_geo['Target Standardised City'].apply(lambda x: re.sub(r"'[^;]*]", '', str(x)))
inward_geo.loc[inward_geo['Target Standardised City'] == '[]', 'Target Standardised City'] = np.nan

inward_geo['Acquiror Standardised City'] = inward_geo['Acquiror Standardised City'].apply(lambda x: str(x))
inward_geo['Acquiror Standardised City'] = inward_geo['Acquiror Standardised City'].apply(lambda x: re.sub(r"\[\(\'", '', str(x)))
inward_geo['Acquiror Standardised City'] = inward_geo['Acquiror Standardised City'].apply(lambda x: re.sub(r"'[^;]*]", '', str(x)))
inward_geo.loc[inward_geo['Acquiror Standardised City'] == '[]', 'Acquiror Standardised City'] = np.nan


inward_geo['Target country'] = inward_geo['Target country'].apply(lambda x: str(x))
inward_geo['Target country'] = inward_geo['Target country'].apply(lambda x: re.sub(r"\[\(\'", '', str(x)))
inward_geo['Target country'] = inward_geo['Target country'].apply(lambda x: re.sub(r"'[^;]*]", '', str(x)))
inward_geo.loc[inward_geo['Target country'] == '[]', 'Target country'] = np.nan

inward_geo['Acquiror country'] = inward_geo['Acquiror country'].apply(lambda x: str(x))
inward_geo['Acquiror country'] = inward_geo['Acquiror country'].apply(lambda x: re.sub(r"\[\(\'", '', str(x)))
inward_geo['Acquiror country'] = inward_geo['Acquiror country'].apply(lambda x: re.sub(r"'[^;]*]", '', str(x)))
inward_geo.loc[inward_geo['Acquiror country'] == '[]', 'Acquiror country'] = np.nan

inward_geo.loc[inward_geo['Target Standardised City'].isnull() == True, 'Target Standardised City'] = inward_geo.loc[inward_geo['Target Standardised City'].isnull() == True, 'Target country']
inward_geo.loc[inward_geo['Acquiror Standardised City'].isnull() == True, 'Acquiror Standardised City'] = inward_geo.loc[inward_geo['Acquiror Standardised City'].isnull() == True, 'Acquiror country']

### then doing regions

iso = pd.read_csv('https://raw.githubusercontent.com/vincentarelbundock/countrycode/main/dictionary/codelist_panel_without_cldr.csv')

iso2c = dict(zip(iso['iso2c'], iso['country.name.en']))
isoRR = dict(zip(iso['iso2c'], iso['region']))

inward_geo.columns = ['Deal Number', 'Deal value adj', 'Target Standardised City', 'Acquiror Standardised City', 'Target Country Code', 'Acquiror Country Code']

inward_geo['Target name'] = inward_geo['Target Country Code'].apply(lambda x: iso2c.get(x))
inward_geo['Acquiror name'] = inward_geo['Acquiror Country Code'].apply(lambda x: iso2c.get(x))
inward_geo['Target region'] = inward_geo['Target Country Code'].apply(lambda x: isoRR.get(x))
inward_geo['Acquiror region'] = inward_geo['Acquiror Country Code'].apply(lambda x: isoRR.get(x))

# not all countries are matched, doing this manually

# missing_codes = set(list(inward_geo[inward_geo['Target name'].isnull() == True]['Target Country Code']) + list(inward_geo[inward_geo['Acquiror name'].isnull() == True]['Acquiror Country Code']))

inward_geo.loc[inward_geo['Target Country Code'] == 'BM', 'Target name'] = 'Bermuda'
inward_geo.loc[inward_geo['Target Country Code'] == 'KY', 'Target name'] = 'Cayman Islands'
inward_geo.loc[inward_geo['Target Country Code'] == 'PF', 'Target name'] = 'French Polynesia'
inward_geo.loc[inward_geo['Target Country Code'] == 'PR', 'Target name'] = 'Puerto Rico'
inward_geo.loc[inward_geo['Target Country Code'] == 'VG', 'Target name'] = 'British Virgin Islands'

inward_geo.loc[inward_geo['Acquiror Country Code'] == 'BM', 'Acquiror name'] = 'Bermuda'
inward_geo.loc[inward_geo['Acquiror Country Code'] == 'KY', 'Acquiror name'] = 'Cayman Islands'
inward_geo.loc[inward_geo['Acquiror Country Code'] == 'PF', 'Acquiror name'] = 'French Polynesia'
inward_geo.loc[inward_geo['Acquiror Country Code'] == 'PR', 'Acquiror name'] = 'Puerto Rico'
inward_geo.loc[inward_geo['Acquiror Country Code'] == 'VG', 'Acquiror name'] = 'British Virgin Islands'

inward_geo.loc[inward_geo['Target Country Code'] == 'BM', 'Target region'] = 'Latin America & Caribbean'
inward_geo.loc[inward_geo['Target Country Code'] == 'KY', 'Target region'] = 'Latin America & Caribbean'
inward_geo.loc[inward_geo['Target Country Code'] == 'PF', 'Target region'] = 'Latin America & Caribbean'
inward_geo.loc[inward_geo['Target Country Code'] == 'PR', 'Target region'] = 'Latin America & Caribbean'
inward_geo.loc[inward_geo['Target Country Code'] == 'VG', 'Target region'] = 'Latin America & Caribbean'

inward_geo.loc[inward_geo['Acquiror Country Code'] == 'BM', 'Acquiror region'] = 'Latin America & Caribbean'
inward_geo.loc[inward_geo['Acquiror Country Code'] == 'KY', 'Acquiror region'] = 'Latin America & Caribbean'
inward_geo.loc[inward_geo['Acquiror Country Code'] == 'PF', 'Acquiror region'] = 'Latin America & Caribbean'
inward_geo.loc[inward_geo['Acquiror Country Code'] == 'PR', 'Acquiror region'] = 'Latin America & Caribbean'
inward_geo.loc[inward_geo['Acquiror Country Code'] == 'VG', 'Acquiror region'] = 'Latin America & Caribbean'

# this is where the missing values were coming from, filling in the NaNs in acq citys so that we get the correct count
inward_geo.loc[inward_geo['Acquiror Standardised City'].isna() == True, 'Acquiror Standardised City'] = 'Other'

# x.iat[0] returns the first value in the row of this group, i.e. in this case the country or region in which the city is located
inward_geo_sankey = inward_geo.groupby(['Target Standardised City', 'Acquiror Standardised City'], dropna=False).agg({'Deal value adj' : 'sum',
                                                                                                      'Target Country Code' : 'count',
                                                                                                      'Target name' : lambda x: x.iat[0],
                                                                                                      'Acquiror name' : lambda x: x.iat[0],
                                                                                                      'Target region' : lambda x: x.iat[0],
                                                                                                      'Acquiror region' : lambda x: x.iat[0]})


inward_geo_sankey = inward_geo_sankey.reset_index()
inward_geo_sankey.columns = ['Target Standardised City', 'Acquiror Standardised City','Deal value adj', 'Count', 'Target name', 'Acquiror name', 'Target region', 'Acquiror region']

inward_geo_sankey.to_csv('05_inward_city_all.csv')

## Percent counts for the articles

out_pct = inward_geo_sankey.groupby(['Acquiror Standardised City']).agg({'Count' : 'sum'})
out_pct = out_pct.reset_index()
out_pct['PERCENT'] = out_pct['Count'] / out_pct['Count'].sum() * 100

out_pct.to_csv('05_inward_city_all_pct.csv')




acq_count = inward_geo_sankey.groupby('Acquiror Standardised City').agg({'Count' : 'sum'})
acq_count = acq_count.reset_index()
below10acq = list(acq_count[acq_count['Count'] < 10]['Acquiror Standardised City'])
abv10acq = list(acq_count[acq_count['Count'] > 10]['Acquiror Standardised City'])


tg_count = inward_geo_sankey.groupby('Target Standardised City').agg({'Count' : 'sum'})
tg_count = tg_count.reset_index()
below10tg = list(tg_count[tg_count['Count'] < 10]['Target Standardised City'])

inward_geo_sankey.loc[inward_geo_sankey['Acquiror Standardised City'].isin(below10acq) == True, 'Acquiror Standardised City'] = inward_geo_sankey.loc[inward_geo_sankey['Acquiror Standardised City'].isin(below10acq) == True, 'Acquiror name'] 

inward_geo_sankey.loc[inward_geo_sankey['Target Standardised City'].isin(below10tg) == True, 'Target Standardised City'] = inward_geo_sankey.loc[inward_geo_sankey['Target Standardised City'].isin(below10tg) == True, 'Target name'] 

inward_geo_sankey_above_10 = inward_geo_sankey[inward_geo_sankey['Acquiror Standardised City'].isin(abv10acq) == True]
#
inward_geo_sankey_above_10.to_csv('05_inward_city_above_10.csv')

###########
### outward
###########

outward_geo = outward.groupby(['Deal Number']).agg({'Deal value adj' : lambda x: x.iat[0],
                                                  'Target Standardised City' : lambda x: Counter(x.dropna()).most_common(1),
                                                  'Acquiror Standardised City' : lambda x: Counter(x.dropna()).most_common(1),
                                                  'Target country' :  lambda x: Counter(x.dropna()).most_common(1),
                                                  'Acquiror country' : lambda x: Counter(x.dropna()).most_common(1)})

outward_geo = outward_geo.reset_index()

outward_geo['Target Standardised City'] = outward_geo['Target Standardised City'].apply(lambda x: str(x))
outward_geo['Target Standardised City'] = outward_geo['Target Standardised City'].apply(lambda x: re.sub(r"\[\(\'", '', x))
outward_geo['Target Standardised City'] = outward_geo['Target Standardised City'].apply(lambda x: re.sub(r"'[^;]*]", '', x))
outward_geo.loc[outward_geo['Target Standardised City'] == '[]', 'Target Standardised City'] = np.nan

outward_geo['Acquiror Standardised City'] = outward_geo['Acquiror Standardised City'].apply(lambda x: str(x))
outward_geo['Acquiror Standardised City'] = outward_geo['Acquiror Standardised City'].apply(lambda x: re.sub(r"\[\(\'", '', x))
outward_geo['Acquiror Standardised City'] = outward_geo['Acquiror Standardised City'].apply(lambda x: re.sub(r"'[^;]*]", '', x))
outward_geo.loc[outward_geo['Acquiror Standardised City'] == '[]', 'Acquiror Standardised City'] = np.nan


outward_geo['Target country'] = outward_geo['Target country'].apply(lambda x: str(x))
outward_geo['Target country'] = outward_geo['Target country'].apply(lambda x: re.sub(r"\[\(\'", '', x))
outward_geo['Target country'] = outward_geo['Target country'].apply(lambda x: re.sub(r"'[^;]*]", '', x))
outward_geo.loc[outward_geo['Target country'] == '[]', 'Target country'] = np.nan

outward_geo['Acquiror country'] = outward_geo['Acquiror country'].apply(lambda x: str(x))
outward_geo['Acquiror country'] = outward_geo['Acquiror country'].apply(lambda x: re.sub(r"\[\(\'", '', x))
outward_geo['Acquiror country'] = outward_geo['Acquiror country'].apply(lambda x: re.sub(r"'[^;]*]", '', x))
outward_geo.loc[outward_geo['Acquiror country'] == '[]', 'Acquiror country'] = np.nan

outward_geo.loc[outward_geo['Target Standardised City'].isnull() == True, 'Target Standardised City'] = outward_geo.loc[outward_geo['Target Standardised City'].isnull() == True, 'Target country']
outward_geo.loc[outward_geo['Acquiror Standardised City'].isnull() == True, 'Acquiror Standardised City'] = outward_geo.loc[outward_geo['Acquiror Standardised City'].isnull() == True, 'Acquiror country']

### then doing regions

iso = pd.read_csv('https://raw.githubusercontent.com/vincentarelbundock/countrycode/main/dictionary/codelist_panel_without_cldr.csv')

iso2c = dict(zip(iso['iso2c'], iso['country.name.en']))
isoRR = dict(zip(iso['iso2c'], iso['region']))

outward_geo.columns = ['Deal Number', 'Deal value adj', 'Target Standardised City', 'Acquiror Standardised City', 'Target Country Code', 'Acquiror Country Code']

outward_geo['Target name'] = outward_geo['Target Country Code'].apply(lambda x: iso2c.get(x))
outward_geo['Acquiror name'] = outward_geo['Acquiror Country Code'].apply(lambda x: iso2c.get(x))
outward_geo['Target region'] = outward_geo['Target Country Code'].apply(lambda x: isoRR.get(x))
outward_geo['Acquiror region'] = outward_geo['Acquiror Country Code'].apply(lambda x: isoRR.get(x))

# not all countries are matched, doing this manually

# missing_codes = set(list(outward_geo[outward_geo['Target name'].isnull() == True]['Target Country Code']) + list(outward_geo[outward_geo['Acquiror name'].isnull() == True]['Acquiror Country Code']))

outward_geo.loc[outward_geo['Target Country Code'] == 'BM', 'Target name'] = 'Bermuda'
outward_geo.loc[outward_geo['Target Country Code'] == 'KY', 'Target name'] = 'Cayman Islands'
outward_geo.loc[outward_geo['Target Country Code'] == 'PF', 'Target name'] = 'French Polynesia'
outward_geo.loc[outward_geo['Target Country Code'] == 'PR', 'Target name'] = 'Puerto Rico'
outward_geo.loc[outward_geo['Target Country Code'] == 'VG', 'Target name'] = 'British Virgin Islands'

outward_geo.loc[outward_geo['Acquiror Country Code'] == 'BM', 'Acquiror name'] = 'Bermuda'
outward_geo.loc[outward_geo['Acquiror Country Code'] == 'KY', 'Acquiror name'] = 'Cayman Islands'
outward_geo.loc[outward_geo['Acquiror Country Code'] == 'PF', 'Acquiror name'] = 'French Polynesia'
outward_geo.loc[outward_geo['Acquiror Country Code'] == 'PR', 'Acquiror name'] = 'Puerto Rico'
outward_geo.loc[outward_geo['Acquiror Country Code'] == 'VG', 'Acquiror name'] = 'British Virgin Islands'

outward_geo.loc[outward_geo['Target Country Code'] == 'BM', 'Target region'] = 'Latin America & Caribbean'
outward_geo.loc[outward_geo['Target Country Code'] == 'KY', 'Target region'] = 'Latin America & Caribbean'
outward_geo.loc[outward_geo['Target Country Code'] == 'PF', 'Target region'] = 'Latin America & Caribbean'
outward_geo.loc[outward_geo['Target Country Code'] == 'PR', 'Target region'] = 'Latin America & Caribbean'
outward_geo.loc[outward_geo['Target Country Code'] == 'VG', 'Target region'] = 'Latin America & Caribbean'

outward_geo.loc[outward_geo['Acquiror Country Code'] == 'BM', 'Acquiror region'] = 'Latin America & Caribbean'
outward_geo.loc[outward_geo['Acquiror Country Code'] == 'KY', 'Acquiror region'] = 'Latin America & Caribbean'
outward_geo.loc[outward_geo['Acquiror Country Code'] == 'PF', 'Acquiror region'] = 'Latin America & Caribbean'
outward_geo.loc[outward_geo['Acquiror Country Code'] == 'PR', 'Acquiror region'] = 'Latin America & Caribbean'
outward_geo.loc[outward_geo['Acquiror Country Code'] == 'VG', 'Acquiror region'] = 'Latin America & Caribbean'

# x.iat[0] returns the first value in the row of this group, i.e. in this case the country or region in which the city is located
outward_geo_sankey = outward_geo.groupby(['Target Standardised City', 'Acquiror Standardised City'], dropna=False).agg({'Deal value adj' : 'sum',
                                                                                                      'Acquiror Standardised City' : 'count',
                                                                                                      'Target name' : lambda x: x.iat[0],
                                                                                                      'Acquiror name' : lambda x: x.iat[0],
                                                                                                      'Target region' : lambda x: x.iat[0],
                                                                                                      'Acquiror region' : lambda x: x.iat[0]})

outward_geo_sankey.columns = ['Deal value adj', 'Count', 'Target name', 'Acquiror name', 'Target region', 'Acquiror region']

outward_geo_sankey = outward_geo_sankey.reset_index()

outward_geo_sankey.to_csv('05_outward_city_all.csv')

## Percent counts for the articles

out_pct = outward_geo_sankey.groupby(['Acquiror Standardised City']).agg({'Count' : 'sum'})
out_pct = out_pct.reset_index()
out_pct['PERCENT'] = out_pct['Count'] / out_pct['Count'].sum() * 100

out_pct.to_csv('05_outward_city_all_pct.csv')


acq_count = outward_geo_sankey.groupby('Acquiror Standardised City').agg({'Count' : 'sum'})
acq_count = acq_count.reset_index()
below10acq = list(acq_count[acq_count['Count'] < 10]['Acquiror Standardised City'])
abv10acq = list(acq_count[acq_count['Count'] > 10]['Acquiror Standardised City'])


tg_count = outward_geo_sankey.groupby('Target Standardised City').agg({'Count' : 'sum'})
tg_count = tg_count.reset_index()
below10tg = list(tg_count[tg_count['Count'] < 10]['Target Standardised City'])

outward_geo_sankey.loc[outward_geo_sankey['Acquiror Standardised City'].isin(below10acq) == True, 'Acquiror Standardised City'] = outward_geo_sankey.loc[outward_geo_sankey['Acquiror Standardised City'].isin(below10acq) == True, 'Acquiror name'] 

outward_geo_sankey.loc[outward_geo_sankey['Target Standardised City'].isin(below10tg) == True, 'Target Standardised City'] = outward_geo_sankey.loc[outward_geo_sankey['Target Standardised City'].isin(below10tg) == True, 'Target name'] 

outward_geo_sankey_above_10 = outward_geo_sankey[outward_geo_sankey['Acquiror Standardised City'].isin(abv10acq) == True]
#
outward_geo_sankey_above_10.to_csv('05_outward_city_above_10.csv')
