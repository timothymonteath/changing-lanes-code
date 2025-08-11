import pandas as pd
import numpy as np
import os
import re
from collections import Counter


df = pd.read_csv('motor_data.csv')

# making in and outs

inward =  df.groupby(['Deal Number']).filter(lambda x: (x['AcquirorMotor'].sum() == 0) & (x['TargetMotor'].sum() > 0))

outward =  df.groupby(['Deal Number']).filter(lambda x: (x['AcquirorMotor'].sum() > 0) & (x['TargetMotor'].sum() == 0))

# counting

# Counter takes a list of the sectors, with na's dropped, as in complex multiple company deals not all may have classifiers
# and then takes the most common sector, 1 specifies the most common, then 0 the first value returned and then 0 for the label

out = outward.groupby('Deal Number').agg({'Target primary NAICS 2017 code' : lambda x: str(Counter(x.dropna()).most_common(1))[2:4]})

inw = inward.groupby('Deal Number').agg({'Acquiror primary NAICS 2017 code' : lambda x: str(Counter(x.dropna()).most_common(1))[2:4]})

out = out.reset_index()
inw = inw.reset_index()

out = out.groupby('Target primary NAICS 2017 code').count()
inw = inw.groupby('Acquiror primary NAICS 2017 code').count()

out = out.reset_index()
inw = inw.reset_index()

out.columns = ['Code', 'Outward']
inw.columns = ['Code', 'Inward']

sector_dict = {'11' : 'Agriculture, Forestry, Fishing and Hunting',
               '21' : 'Mining',
               '22' : 'Utilities',
               '23' : 'Construction',
               '31' : 'Manufacturing',
               '32' : 'Manufacturing',
               '33' : 'Manufacturing',
               '42' : 'Wholesale Trade',
               '44' : 'Retail Trade',
               '45' : 'Retail Trade',
               '48' : 'Transportation and Warehousing',
               '49' : 'Transportation and Warehousing',
               '51' : 'Information',
               '52' : 'Finance and Insurance',
               '53' : 'Real Estate Rental and Leasing',
               '54' : 'Professional, Scientific, and Technical Services',
               '55' : 'Management of Companies and Enterprises',
               '56' : 'Administrative and Support and Waste Management and Remediation Service',
               '61' : 'Educational Services',
               '62' : 'Health Care and Social Assistance',
               '71' : 'Arts, Entertainment, and Recreation',
               '72' : 'Accommodation and Food Services',
               '81' : 'Other Services (except Public Administration)',
               '92' : 'Public Administration'}

out['Code'] = out['Code'].apply(lambda x: sector_dict.get(x))
inw['Code'] = inw['Code'].apply(lambda x: sector_dict.get(x))

out.loc[out['Code'].isnull() == True, 'Code'] = 'Unclassified'
inw.loc[inw['Code'].isnull() == True, 'Code'] = 'Unclassified'

out = out.groupby('Code').agg({'Outward' : 'sum'})
inw = inw.groupby('Code').agg({'Inward' : 'sum'})

out = out.reset_index()
inw = inw.reset_index()

merg = out.merge(inw, on = 'Code', how='outer')

merg.to_csv('04_industry_in_out.csv')
