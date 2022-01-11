# -*- coding: utf-8 -*-
"""
Looking at short term rental registrations in Toronto
short-term-rental-registrations-data.csv
downloaded from City of Toronto open data portal:
    https://open.toronto.ca/dataset/short-term-rentals-registration/

@author: Andriy Ahapov
"""
import pandas as pd
import numpy as np

df = pd.read_csv('short-term-rental-registrations-data.csv')

print('The dataset has', df.shape[0], 'rows, and', df.shape[1], 'columns')

n = list(range(0,df.shape[1]))

for i in n:
    print("Column ", df.columns[i], 'has ', df.iloc[:,i].isna().sum(), 'empty values')
    
df = df.dropna()

print(df.shape)

# Now let's group to rentals:

by_ward_and_postal = df.groupby(['ward_number','postal_code']).agg({'_id':'count'})
by_ward_only = df.groupby('ward_number').agg({'_id':'count'})
# We can see that the index type is float, we need to change to integer
by_ward_only.index = by_ward_only.index.astype(int)

import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
ax.bar(by_ward_only.index, by_ward_only['_id'])
ax.set_ylabel("Amount of short term rentals")
ax.set_xlabel("Ward number")

#We see one ward overexceeding in short term rentals. However we don't know
# how that compares to population. Let's try and find Population data by ward
# we have downloaded Toronto population by wards data from City portal

df2 = pd.read_csv("to_pop_by_ward.csv")

pop_by_ward = df2.groupby('Ward').sum()

ax2 = ax.twinx()
ax2.plot(pop_by_ward, color='r')
ax2.set_ylabel("Population")

plt.title("Short-term rentals and population by ward")

# It would be good to see also # of short term rentals by '000 people
# We would need to merge two dataframes together, and calculate the ratio

rent_pop_by_ward = by_ward_only.join(pop_by_ward)
rent_pop_by_ward = rent_pop_by_ward.rename(columns={'_id':'rentals', 'Population':'population'})

rent_pop_by_ward['rent_per_10kpop'] = round(rent_pop_by_ward['rentals'] / (rent_pop_by_ward['population']/10000),2)


med_rent = rent_pop_by_ward['rent_per_10kpop'].median()

rent_colors = list()

for value in rent_pop_by_ward['rent_per_10kpop']:
    if value > med_rent:
        rent_colors.append('r')
    else:
        rent_colors.append('g')

fig = plt.figure()
ax = fig.add_subplot(111)

ax.bar(rent_pop_by_ward.index, rent_pop_by_ward['rent_per_10kpop'], color=rent_colors)
plt.title("Short term rentals per 10k population by city ward")

# We see that 14 out of 25 wards have higher than median short term rentals
# per 10k population
# Ward 10 has an extremely high amount of short-term rentals
# Let's have a closer look inside ward 10 and postal codes wihtin it

ward_10 = by_ward_and_postal.loc[10]

fig, ax = plt.subplots()
ax.bar(ward_10.index, ward_10['_id'], color=['g','g','g','r','g','r','g','g'])
ax.set_xlabel("Postal code")
ax.set_ylabel("Short term licenses")
plt.title("Short term rental licenses in ward 10")

print(ward_10)

by_postal_only = df.groupby('postal_code').agg({'_id':'count'})
sorted_codes = by_postal_only.sort_values(by='_id', ascending=False)
total_rentals = sorted_codes['_id'].sum()

sorted_codes['share'] = round((sorted_codes['_id'] / total_rentals)*100,0)

top_sorted = sorted_codes[sorted_codes['share']>2]
fig, ax = plt.subplots()
ax.bar(top_sorted.index, top_sorted['share'])
ax.set_xticklabels(top_sorted.index,rotation = 90)
ax.set_ylabel("% share of city short term rentals")
plt.title("Share of short term rentals by postal code")

pop_post_codes = pd.read_csv('Pop_by_postal_code.csv')
pop_post_codes = pop_post_codes.set_index('postal_code')

codes_and_pop = sorted_codes.join(pop_post_codes, how='left')

codes_and_pop['rent_per_10kpop'] = round(codes_and_pop['_id'] / (codes_and_pop['population']/10000),2)
codes_and_pop['empty_dwellings'] = codes_and_pop['private_dwellings'] - codes_and_pop['dwellings_occupied']
