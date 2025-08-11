import pandas as pd
import numpy as np
import os
import re

df = pd.read_csv('motor_data.csv')

# basic counts

intra = df.groupby(['Deal Number']).filter(lambda x: (x['AcquirorMotor'].sum() > 0) & (x['TargetMotor'].sum() > 0))

inward =  df.groupby(['Deal Number']).filter(lambda x: (x['AcquirorMotor'].sum() == 0) & (x['TargetMotor'].sum() > 0))

outward =  df.groupby(['Deal Number']).filter(lambda x: (x['AcquirorMotor'].sum() > 0) & (x['TargetMotor'].sum() == 0))

# intra tables
intra_year = intra.groupby(['Deal Number']).agg({'Deal value adj' : lambda x: x.iat[0],
                                                  'Year' : lambda x: x.iat[0]})

intra_year = intra_year.reset_index()

intra_year_value = intra_year.groupby('Year').agg({'Deal value adj': 'sum'})
intra_year_volume = intra_year.groupby('Year').agg({'Deal value adj': 'count'})

intra_year_volume = intra_year_volume.reset_index()
intra_year_value = intra_year_value.reset_index()


# inward tables
inward_year = inward.groupby(['Deal Number']).agg({'Deal value adj' : lambda x: x.iat[0],
                                                  'Year' : lambda x: x.iat[0]})


inward_year = inward_year.reset_index()

inward_year_value = inward_year.groupby('Year').agg({'Deal value adj': 'sum'})
inward_year_volume = inward_year.groupby('Year').agg({'Deal value adj': 'count'})

inward_year_volume = inward_year_volume.reset_index()
inward_year_value = inward_year_value.reset_index()

# outward tables
outward_year = outward.groupby(['Deal Number']).agg({'Deal value adj' : lambda x: x.iat[0],
                                                  'Year' : lambda x: x.iat[0]})


outward_year = outward_year.reset_index()

outward_year_value = outward_year.groupby('Year').agg({'Deal value adj': 'sum'})
outward_year_volume = outward_year.groupby('Year').agg({'Deal value adj': 'count'})

outward_year_volume = outward_year_volume.reset_index()
outward_year_value = outward_year_value.reset_index()

# combining tables

outward_year_value = outward_year_value.set_axis(['Year', 'Outward Value'], axis=1)
inward_year_value = inward_year_value.set_axis(['Year', 'Inward Value'], axis=1)
intra_year_value = intra_year_value.set_axis(['Year', 'Intra Value'], axis=1)

outward_year_volume = outward_year_volume.set_axis(['Year', 'Outward Volume'], axis=1)
inward_year_volume = inward_year_volume.set_axis(['Year', 'Inward Volume'], axis=1)
intra_year_volume = intra_year_volume.set_axis(['Year', 'Intra Volume'], axis=1)

out = outward_year_value.merge(inward_year_value, on='Year')
out = out.merge(intra_year_value, on='Year')

out.to_csv('02_motor_year_value.csv')


out = outward_year_volume.merge(inward_year_volume, on='Year')
out = out.merge(intra_year_volume, on='Year')

out.to_csv('02_motor_year_volume.csv')

