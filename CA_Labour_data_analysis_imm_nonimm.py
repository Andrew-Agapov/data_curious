# -*- coding: utf-8 -*-
"""
In this example I am examining Open Data from Canadian government
on Labour force characteristics of immigrants by sex and age group,
three-month moving average, unadjusted for seasonality (2006-2021)

CSV dowloaded from: https://open.canada.ca/data/en/dataset/ae01fd0c-7f86-4d49-8ea3-84834ccdc3b7
filename: 14100084.csv --> please put this file into your working Python
directory to be able to run this script.

Packages used: numpy, pandas, matplotlib

In this analysis I am looking at unemployment data from dataset:
    1) What is the long-term trend in unemployment rates over 2006-2021
    2) What are the unemployment rates differences in Canadians born in Canada, and immigrants?
    3) Are there differences in unemployment rates in different categories of immigrants?
    4) Are there differences in employment characteristics structues among immigrants and non-immigrants?

Created on Sat Dec 11 15:12:03 2021

@author: Andriy Ahapov
"""

# Let's start with importing pandas package:
import pandas as pd

# Read csv data file and pass it to veriable labour_data
labour_data = pd.read_csv("14100084.csv")

# Let's have a look at first 5 lines of the DataFrame:
print(labour_data.iloc[0:5,:])

# Not all columns are displayed, let's see the shape of the DataFrame:
print(labour_data.shape)

# 136080 rows and 18 columns. Seems like too many columns for our analysis.
# Let's explore column names and see if we can drop some of them out
print(labour_data.columns)

# We can see a list of column names: 'REF_DATE', 'GEO', 'DGUID', 'Immigrant status',
# 'Labour force characteristics', 'Sex', 'Age group', 'UOM', 'UOM_ID',
# 'SCALAR_FACTOR', 'SCALAR_ID', 'VECTOR', 'COORDINATE', 'VALUE', 'STATUS', 
# SYMBOL', 'TERMINATED', 'DECIMALS'

# We can already say which columns we most likely don't need, 
# but let's check some of them for unique values to be 100% sure:
print(labour_data['GEO'].unique()) # Canada is the only GEO, drop it
print(labour_data['DGUID'].unique()) # Only one value, drop it
print(labour_data['Immigrant status'].unique()) # We will definitely need this
print(labour_data['Labour force characteristics'].unique()) #We will need this as well
print(labour_data['Sex'].unique()) # We will need this
print(labour_data['Age group'].unique()) # We will need this
print(labour_data['UOM'].unique()) # We would need this
print(labour_data['UOM_ID'].unique()) # We won't need UOM id
print(labour_data['SCALAR_FACTOR'].unique()) # this is either thousands (for Persons UOM) or units (for %). We can drop this.
print(labour_data['SCALAR_ID'].unique()) # No value for us, we'll drop it
print(labour_data['VECTOR'].unique()) # No value for us, we'll drop it
print(labour_data['COORDINATE'].unique()) # No value for us, we'll drop it
print(labour_data['STATUS'].unique()) # Not valuable, we'll drop it
print(labour_data['SYMBOL'].unique()) # Empty column, drop
print(labour_data['TERMINATED'].unique()) # Empty column, drop
print(labour_data['DECIMALS'].unique()) # Only '1' value in column, drop

# let's subset DataFrame to include only REF_DATE, Immigrant Status, 
# Labour force characteristics, Sex, Age group, VALUE, UOM
# we also placed the column VALUE before UOM for convenience

labour_filtered = labour_data [['REF_DATE', 'Immigrant status', 'Labour force characteristics','Sex', 'Age group','VALUE', 'UOM']]

print(labour_filtered.shape)
# Now we have only 7 columns which will be much more convenient to use

# Now let's create filters which we will use later to filter DataFrame set
# In column 'Immigrant status' we have 6 categories:  'Total population', 
# 'Landed immigrants', 'Immigrants, landed 5 or less years earlier',
# 'Immigrants, landed more than 5 to 10 years earlier',
# 'Immigrants, landed more than 10 years earlier', 'Born in Canada'.
# Let's create according filters:
total_population = labour_filtered['Immigrant status'] == 'Total population'
landed_immigrants = labour_filtered['Immigrant status'] == 'Landed immigrants'
newcomers = labour_filtered['Immigrant status'] == 'Immigrants, landed 5 or less years earlier'
settled_residents = labour_filtered['Immigrant status'] == 'Immigrants, landed more than 5 to 10 years earlier'
immigrated_over_10_ya = labour_filtered['Immigrant status'] == 'Immigrants, landed more than 10 years earlier'
born_in_ca = labour_filtered['Immigrant status'] == 'Born in Canada'

# Since the dataset has data for women, men and both sexes together, we need a filter there as well"
men = labour_filtered['Sex'] == 'Males'
women = labour_filtered['Sex'] == 'Females'
both_sexes = labour_filtered['Sex'] == 'Both sexes'

# Same for age groups:
over_15_years = labour_filtered['Age group'] == '15 years and over'
_15to24_years = labour_filtered['Age group'] == '15 to 24 years'
_25to54_years = labour_filtered['Age group'] == '25 to 54 years'
over_55_years = labour_filtered['Age group'] == '55 years and over'

# Finally, filters for labour force characteristics and off to the races!
population = labour_filtered['Labour force characteristics'] == 'Population'
labour_force = labour_filtered['Labour force characteristics'] == 'Labour force'
employment = labour_filtered['Labour force characteristics'] == 'Employment'
full_time_employment = labour_filtered['Labour force characteristics'] == 'Full-time employment'
part_time_employment = labour_filtered['Labour force characteristics'] == 'Part-time employment'
unemployment = labour_filtered['Labour force characteristics'] == 'Unemployment'
not_in_labour_force = labour_filtered['Labour force characteristics'] == 'Not in labour force'
unemployment_rate = labour_filtered['Labour force characteristics'] == 'Unemployment rate'
participation_rate = labour_filtered['Labour force characteristics'] == 'Participation rate'
employment_rate = labour_filtered['Labour force characteristics'] == 'Employment rate'

# Now let's go to looking at data

import matplotlib.pyplot as plt

# let's agree to look at 25-54 y.o. age group as they are the primary workforce group
# let's filter to Unemployed immigrants, born in canada and total pop in 25-40 y.o. age group
unemployed_adults_total = labour_filtered[total_population & _15to24_years & unemployment_rate & both_sexes]
unemployed_non_immigrants = labour_filtered[born_in_ca & _15to24_years & unemployment_rate & both_sexes]
unemployed_immigrants = labour_filtered[landed_immigrants & _15to24_years & unemployment_rate & both_sexes]

unemployed_newcomers = labour_filtered[newcomers & _15to24_years & unemployment_rate & both_sexes]
unemployed_settled_residents = labour_filtered[settled_residents & _15to24_years & unemployment_rate & both_sexes]
unemployed_immigrated_over_10_ya = labour_filtered[immigrated_over_10_ya & _15to24_years & unemployment_rate & both_sexes]

# now let's build the plots!

plt.plot(unemployed_adults_total['REF_DATE'],unemployed_adults_total['VALUE'], label = 'All 25-54 y.o.')
plt.plot(unemployed_immigrants['REF_DATE'], unemployed_immigrants['VALUE'], label = 'Immigrants')
plt.plot(unemployed_non_immigrants['REF_DATE'], unemployed_non_immigrants['VALUE'], label = 'Born in Canada')
plt.legend(loc='upper left')
plt.title('Unemployment rate in Total Population, Immigrants, and People Born in Canada, 25-54 y.o.')
plt.show()

# We can see that there was a decreasing long-term trend in Unemployment until a recent spike among all groups
# We also see that immigrants tend to experience higher levels of unemployment vs people born in Canada

# Let's look at different immigrant categories:
plt.plot(unemployed_newcomers['REF_DATE'], unemployed_newcomers['VALUE'], label = 'Newcomers')
plt.plot(unemployed_settled_residents['REF_DATE'], unemployed_settled_residents['VALUE'], label = "Settled 5-10 y.a.")
plt.plot(unemployed_immigrated_over_10_ya['REF_DATE'], unemployed_immigrated_over_10_ya['VALUE'], label = 'Came > 10 y.a.')
plt.plot(unemployed_non_immigrants['REF_DATE'], unemployed_non_immigrants['VALUE'], label = 'Born in Canada')
plt.legend(loc='upper left')
plt.title('Unemployment rate in Total Population, Immigrant categories, and People Born in Canada, 25-54 y.o.')
plt.show()

# Line chart looks too busy to analyze, let's try looking at boxplot instead:
    
import numpy as np

ue_locals_box = np.array(unemployed_non_immigrants['VALUE'])
ue_immigrants_box = np.array(unemployed_immigrants['VALUE'])
ue_newcomers_box = np.array(unemployed_newcomers['VALUE'])
ue_settled_box = np.array(unemployed_settled_residents['VALUE'])
ue_rooted_box = np.array(unemployed_immigrated_over_10_ya['VALUE'])

boxplot_ue_data = [ue_locals_box, ue_immigrants_box, ue_newcomers_box, ue_settled_box, ue_rooted_box]

plt.boxplot(boxplot_ue_data, labels = ['Born in Canada', 'All immigrants', 'Newcomers', 'Settled 5-10 y.a.', 'Came > 10 y.a.'])
plt.xticks(fontsize=8, rotation=45)
plt.grid(axis = 'y')
plt.title('Unemployment rates variations')
plt.show()

# We can see that Newcomers expect much higher levels of unemployment vs people Born in Canada,
# Unemployment levels decrease for immigrants as they live longer in Canada
# For immigrants living >10 years in Canada, unemployment levels are close to those born in Canada

#let's compare shares of populations and shares of unemployed populations in immigrants and non-immigrants:
unemployed_qty = labour_filtered['Labour force characteristics'] == 'Unemployment'
pop_qty = labour_filtered['Labour force characteristics'] == 'Population'
    
qty_ue_imm = labour_filtered[landed_immigrants & _15to24_years & unemployed_qty & both_sexes]
qty_ue_born = labour_filtered[born_in_ca & _15to24_years & unemployed_qty & both_sexes]

qty_ue_imm_mean = qty_ue_imm['VALUE'].mean()
qty_ue_born_mean = qty_ue_born['VALUE'].mean()

qty_imm_pop = labour_filtered[landed_immigrants & _15to24_years & pop_qty & both_sexes]
qty_born_pop = labour_filtered[born_in_ca & _15to24_years & pop_qty & both_sexes]

qty_imm_pop_mean = qty_imm_pop['VALUE'].mean()
qty_born_pop_mean = qty_born_pop['VALUE'].mean()

fig, (ax1,ax2) = plt.subplots(1,2,figsize=(10,10)) #ax1,ax2 refer to two pies

labels = ' Unemp. immigrants', 'Unemp. locals'
unemp_shares = [qty_ue_imm_mean, qty_ue_born_mean]
ax1.pie(unemp_shares,labels = labels,autopct = '%1.1f%%') #plot first pie


labels = 'Total immigrants', 'Total locals'
pop_shares = [qty_imm_pop_mean, qty_born_pop_mean]
ax2.pie(pop_shares,labels = labels,autopct = '%1.1f%%') #plot second pie


# We can see that immigrants are slightly over-represented in unemployed population
# They comprise 13.6% of population and 14.3% of unemployed population in Canada