import pandas as pd
import numpy as np
import os
import re

df = pd.read_csv('motor_data.csv')

intra = df.groupby(['Deal Number']).filter(lambda x: (x['AcquirorMotor'].sum() > 0) & (x['TargetMotor'].sum() > 0))

###################################
# intra
###################################

# note this is the same code for each section, intra, inward and outward with only the directions changed

# make a df grouped by deal number of the codes for the coutries involved in each deal

intra_country_code = intra.groupby('Deal Number').agg({'Acquiror country' : lambda x: set(x.dropna()),
                                                  'Target country' : lambda x: set(x.dropna())})

intra_country_code = intra_country_code.reset_index()
intra_country_code.columns = ['Deal Number', 'Acquiror Country Code', 'Target Country Code']

# make the same as above but with a count, so that later any deal with more than one code is classed as international

intra_country_count = intra.groupby('Deal Number').agg({'Acquiror country' : lambda x: len(set(x.dropna())),
                                                        'Target country' : lambda x: len(set(x.dropna()))})

intra_country_count = intra_country_count.reset_index()
intra_country_count.columns = ['Deal Number', 'Acquiror Country Count', 'Target Country Count']

# then do a group by year and value (first only) so that we can group by this for the final graph

intra_year_value = intra.groupby('Deal Number').agg({'Deal value adj' : lambda x: x.iat[0],
                                               'Year' : lambda x: x.iat[0]})

intra_year_value = intra_year_value.reset_index()

intra_year_value.columns = ['Deal Number', 'Deal value adj', 'Year']

# then merge all of the three dfs above together

intra_all = pd.merge(intra_year_value, intra_country_count, on='Deal Number' )
intra_all = pd.merge(intra_all, intra_country_code, on='Deal Number')


# domestic deals must only have matching country codes eg GB == GB and have no more than one country count on either side of the deal

domestic = intra_all[(intra_all['Acquiror Country Code'] == intra_all['Target Country Code']) & (intra_all['Acquiror Country Count'] == 1) & (intra_all['Target Country Count'] == 1)]

# interntantional is then anything not in the domestic deal set

international = intra_all[(intra_all['Deal Number'].isin(domestic['Deal Number'].to_list()) == False)]

# then do totals by grouping by year and adding up the value and count

domestic_years = domestic.groupby('Year').agg({'Deal value adj' : 'sum',
                                               'Target Country Count' :  'count'})

domestic_years = domestic_years.reset_index()
domestic_years.columns = ['Year', 'Domestic Deal value adj', 'Domestic Deals Count']


international_years = international.groupby('Year').agg({'Deal value adj' : 'sum',
                                               'Target Country Count' :  'count'})

international_years = international_years.reset_index()
international_years.columns = ['Year', 'International Deal value adj', 'International Deals Count']

out = pd.merge(international_years, domestic_years, on='Year')

out.to_csv('03_int-national_intra.csv')

#########################
# INWARD
#########################

inward =  df.groupby(['Deal Number']).filter(lambda x: (x['AcquirorMotor'].sum() == 0) & (x['TargetMotor'].sum() > 0))


inward_country_code = inward.groupby('Deal Number').agg({'Acquiror country' : lambda x: set(x.dropna()),
                                                  'Target country' : lambda x: set(x.dropna())})

inward_country_code = inward_country_code.reset_index()
inward_country_code.columns = ['Deal Number', 'Acquiror Country Code', 'Target Country Code']

# make the same as above but with a count, so that later any deal with more than one code is classed as international

inward_country_count = inward.groupby('Deal Number').agg({'Acquiror country' : lambda x: len(set(x.dropna())),
                                                        'Target country' : lambda x: len(set(x.dropna()))})

inward_country_count = inward_country_count.reset_index()
inward_country_count.columns = ['Deal Number', 'Acquiror Country Count', 'Target Country Count']

# then do a group by year and value (first only) so that we can group by this for the final graph 

inward_year_value = inward.groupby('Deal Number').agg({'Deal value adj' : lambda x: x.iat[0],
                                               'Year' : lambda x: x.iat[0]})

inward_year_value = inward_year_value.reset_index()

inward_year_value.columns = ['Deal Number', 'Deal value adj', 'Year']

# then merge all of the three dfs above together

inward_all = pd.merge(inward_year_value, inward_country_count, on='Deal Number' )
inward_all = pd.merge(inward_all, inward_country_code, on='Deal Number')


# domestic deals must only have matching country codes eg GB == GB and have no more than one country count on either side of the deal 

domestic = inward_all[(inward_all['Acquiror Country Code'] == inward_all['Target Country Code']) & (inward_all['Acquiror Country Count'] == 1) & (inward_all['Target Country Count'] == 1)]

# interntantional is then anything not in the domestic deal set

international = inward_all[(inward_all['Deal Number'].isin(domestic['Deal Number'].to_list()) == False)]

domestic_years = domestic.groupby('Year').agg({'Deal value adj' : 'sum',
                                               'Target Country Count' :  'count'})

domestic_years = domestic_years.reset_index()
domestic_years.columns = ['Year', 'Domestic Deal value adj', 'Domestic Deals Count']


international_years = international.groupby('Year').agg({'Deal value adj' : 'sum',
                                               'Target Country Count' :  'count'})

international_years = international_years.reset_index()
international_years.columns = ['Year', 'International Deal value adj', 'International Deals Count']

out = pd.merge(international_years, domestic_years, on='Year')

out.to_csv('03_int-national_inward.csv')


#########################
# OUTWARD
#########################

outward =  df.groupby(['Deal Number']).filter(lambda x: (x['AcquirorMotor'].sum() > 0) & (x['TargetMotor'].sum() == 0))

outward_country_code = outward.groupby('Deal Number').agg({'Acquiror country' : lambda x: set(x.dropna()),
                                                  'Target country' : lambda x: set(x.dropna())})

outward_country_code = outward_country_code.reset_index()
outward_country_code.columns = ['Deal Number', 'Acquiror Country Code', 'Target Country Code']

# make the same as above but with a count, so that later any deal with more than one code is classed as international

outward_country_count = outward.groupby('Deal Number').agg({'Acquiror country' : lambda x: len(set(x.dropna())),
                                                        'Target country' : lambda x: len(set(x.dropna()))})

outward_country_count = outward_country_count.reset_index()
outward_country_count.columns = ['Deal Number', 'Acquiror Country Count', 'Target Country Count']

# then do a group by year and value (first only) so that we can group by this for the final graph 

outward_year_value = outward.groupby('Deal Number').agg({'Deal value adj' : lambda x: x.iat[0],
                                               'Year' : lambda x: x.iat[0]})

outward_year_value = outward_year_value.reset_index()

outward_year_value.columns = ['Deal Number', 'Deal value adj', 'Year']

# then merge all of the three dfs above together

outward_all = pd.merge(outward_year_value, outward_country_count, on='Deal Number' )
outward_all = pd.merge(outward_all, outward_country_code, on='Deal Number')


# domestic deals must only have matching country codes eg GB == GB and have no more than one country count on either side of the deal 

domestic = outward_all[(outward_all['Acquiror Country Code'] == outward_all['Target Country Code']) & (outward_all['Acquiror Country Count'] == 1) & (outward_all['Target Country Count'] == 1)]

# interntantional is then anything not in the domestic deal set

international = outward_all[(outward_all['Deal Number'].isin(domestic['Deal Number'].to_list()) == False)]

# then do totals by grouping by year and adding up the value and count

domestic_years = domestic.groupby('Year').agg({'Deal value adj' : 'sum',
                                               'Target Country Count' :  'count'})

domestic_years = domestic_years.reset_index()
domestic_years.columns = ['Year', 'Domestic Deal value adj', 'Domestic Deals Count']


international_years = international.groupby('Year').agg({'Deal value adj' : 'sum',
                                               'Target Country Count' :  'count'})

international_years = international_years.reset_index()
international_years.columns = ['Year', 'International Deal value adj', 'International Deals Count']

out = pd.merge(international_years, domestic_years, on='Year')

out.to_csv('03_int-national_outward.csv')

