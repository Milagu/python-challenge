#!/usr/bin/env python
# coding: utf-8

# ### Heroes Of Pymoli Data Analysis
# * Of the 1163 active players, the vast majority are male (84%). There also exists, a smaller, but notable proportion of female players (14%).
# 
# * Our peak age demographic falls between 20-24 (44.8%) with secondary groups falling between 15-19 (18.60%) and 25-29 (13.4%).  
# -----

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[172]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# Raw data file
file_to_load = "Resources/purchase_data.csv"

# Read purchasing file and store into pandas data frame
purchase_data = pd.read_csv(file_to_load)


# ## Player Count

# * Display the total number of players
# 

# In[174]:


total_players = purchase_data['SN'].nunique()
print("Total number of players is %d" %total_players)


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[175]:


# Basic calculations to obtain the required values listed above
unique_items = len(purchase_data['Item ID'].unique())
avg_price = round(purchase_data['Price'].mean(),2)
num_purchases = len(purchase_data)
total_revenue = round(purchase_data['Price'].sum(),2)

# Create a summary dataframe to hold the calculations
summary_dict = {'Number of Unique Items':[unique_items],
                  'Average Price':[avg_price],
                  'Number of Purchases':[num_purchases],
                  'Total Revenue':[total_revenue]
                 }
summary_df = pd.DataFrame.from_dict(summary_dict)

#Let's give the data a cleaner formatting
summary_df['Average Price'] = summary_df['Average Price'].astype(float).map("${:.2f}".format)
summary_df['Total Revenue'] = summary_df['Total Revenue'].astype(float).map("${:,.2f}".format)

# Display the formatted summary dataframe
summary_df.head()


# # Gender Demographics

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[217]:


# Group the data by gender and obtain the groupwise players count
gender_groups = purchase_data.groupby('Gender')['SN'].nunique()

# Create a new dataframe to hold the grouped values
gender_df = pd.DataFrame(gender_groups)

# Rename the column 'SN' in the grouped dataframe
gender_df = gender_df.rename(columns={'SN':'Total Count'})

# Compute Gender-wise Percentage of Players (total_players is from our prev. block of code)
gender_df['Percentage of Players'] = round(gender_df['Total Count']/total_players*100,2)

# Set display format for the computed value above
gender_df['Percentage of Players'] = gender_df['Percentage of Players'].map('{:,.2f}'.format)

# List the dataframe contents with top 3 Total counts first (alternative to a sort asc. on Total Count)
gender_df.nlargest(3,'Total Count')


# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, etc. by gender
# 
# 
# * For normalized purchasing, divide total purchase value by purchase count, by gender
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[177]:


# Group the data by gender and get the purchase count, avg. purchase price etc.
gender_groups = purchase_data.groupby('Gender').aggregate({'SN': 'size', 'Price': {'Average' : 'mean', 'Total': 'sum'}})

# Compute Avg Total Purchase per person and add it to the grouped Series object above
gender_groups['Avg Total Purchase per Person'] = round(gender_groups['Price']['Total'] / gender_df['Total Count'],2)

# Aggregation adds a second level of header row, which can be flattend out after dropping the top level
gender_groups.columns = gender_groups.columns.droplevel(0)

# Copy the grouped data onto a dataframe (to use a few cool pandas methods later)
purch_anal_df = pd.DataFrame(gender_groups)

# Set the column headers
purch_anal_df = purch_anal_df.rename(columns = {' ': 'Gender',
                                'size': 'Purchase Count',
                                'Average': 'Average Purchase Price',
                                'Total': 'Total Purchase Value',
                                '':'Avg Total Purchase per Person'})

# Set the display format
purch_anal_df['Average Purchase Price'] = purch_anal_df['Average Purchase Price'].map('${:,.2f}'.format)
purch_anal_df['Total Purchase Value'] = purch_anal_df['Total Purchase Value'].map('${:,.2f}'.format)
purch_anal_df['Avg Total Purchase per Person'] = purch_anal_df['Avg Total Purchase per Person'].map('${:,.2f}'.format)

# Display results
purch_anal_df


# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[178]:


# Establish bins, labels for the bins for age
age_bins = [0, 9.90, 14.90, 19.90, 24.90, 29.90, 34.90, 39.90, 99999]
group_names = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

# Categorize the players using the age bins
purch_data_by_age = pd.cut(purchase_data['Age'], age_bins, labels = group_names)

# Compute players by agegroup and Total players
purch_data_by_age = purch_data_by_age.value_counts()
total_players = purch_data_by_age.sum()

# Copy the grouped data onto a dataframe (to use a few cool pandas methods later)
agegroup_df = pd.DataFrame(purch_data_by_age)

# Rename the column
agegroup_df = agegroup_df.rename(columns={'Age':'Total Count'})

# Compute Gender-wise Percentage of Players
agegroup_df['Percentage of Players'] = round((agegroup_df['Total Count']/total_players)*100,2)

#Reorder the row & column sequence
row_seq = [ "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+","<10"]
agegroup_df = agegroup_df.reindex(row_seq)
agegroup_df = agegroup_df[['Percentage of Players','Total Count']]

#Display
agegroup_df


# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, etc. in the table below
# 
# 
# * Calculate Normalized Purchasing
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[179]:


# Group the data by age and get the purchase count, avg. purchase price, total purchase value etc.
purch_by_agegroup = purchase_data.groupby(pd.cut(purchase_data['Age'], age_bins, labels = group_names)).aggregate({'Age': 'size', 'SN':'nunique','Price': {'Average' : 'mean', 'Total': 'sum'}})
purch_by_agegroup['Avg Total Purchase per Person'] = round((purch_by_agegroup['Price']['Total'] / purch_by_agegroup['SN']['nunique']),2)

# Aggregation adds a second level of header row, which can be flattend out after dropping the top level
purch_by_agegroup.columns = purch_by_agegroup.columns.droplevel(0)

# Copy the grouped data onto a dataframe (to use the cool methods of a dataframe later)
purch_by_agegroup_df = pd.DataFrame(purch_by_agegroup)

#Re order the row & column sequence
row_seq = [ "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+","<10"]
purch_by_agegroup_df = purch_by_agegroup_df.reindex(row_seq)

# Flatten out the header row
purch_by_agegroup_df.reset_index()

# Set the column headers
purch_by_agegroup_df = purch_by_agegroup_df.rename(columns = {'': '',
                                                              'size': 'Purchase Count',
                                                              'Average': 'Average Purchase Price',
                                                              'Total': 'Total Purchase Value',
                                                              '':'Avg Total Purchase per Person'})

# Set the display format
purch_by_agegroup_df['Average Purchase Price'] = purch_by_agegroup_df['Average Purchase Price'].map('${:,.2f}'.format)
purch_by_agegroup_df['Total Purchase Value'] = purch_by_agegroup_df['Total Purchase Value'].map('${:,.2f}'.format)
purch_by_agegroup_df['Avg Total Purchase per Person'] = purch_by_agegroup_df['Avg Total Purchase per Person'].map('${:,.2f}'.format)

#Drop the unwanted column from the final display, which was useful to compute the Avg Total Purchase per person
purch_by_agegroup_df.drop(columns = ['nunique'], axis=1)


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[180]:


# Group the data by Players(SN) and get the purchase count, avg. purchase price, total purchase value etc.
spenders = purchase_data.groupby('SN').aggregate({'SN': 'size', 'Price': {'Average' : 'mean', 'Total': 'sum'}})

# Copy the grouped data onto a dataframe (to use the cool methods of a dataframe later)
spenders_df = pd.DataFrame(spenders)

# Aggregation adds a second level of header row, which can be flattend out after dropping the top level
spenders.columns = spenders.columns.droplevel(0)

# Flatten out the header row
spenders_df.reset_index()

# Set the column headers
spenders_df = spenders_df.rename(columns = {'size': 'Purchase Count',
                                            'Average': 'Average Purchase Price',
                                            'Total': 'Total Purchase Value'})

# List the dataframe contents with top 5 Total Purchase Values
top_five_spenders_df = spenders_df.nlargest(5,'Total Purchase Value')

# Set the display format
top_five_spenders_df['Average Purchase Price'] = top_five_spenders_df['Average Purchase Price'].map('${:,.2f}'.format)
top_five_spenders_df['Total Purchase Value'] = top_five_spenders_df['Total Purchase Value'].map('${:,.2f}'.format)

# Display results
top_five_spenders_df


# # Most Popular Items

# #* Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# #* Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value
# 
# 
# #* Create a summary data frame to hold the results
# 
# 
# #* Sort the purchase count column in descending order
# 
# 
# #* Optional: give the displayed data cleaner formatting
# 
# 
# #* Display a preview of the summary data frame
# 
# 

# In[216]:


# Let's get the basic calculations (aggregated values) into a dataframe along with Item Names
popular = purchase_data.groupby(['Item ID','Item Name']).aggregate({'Purchase ID':'size', 'Price': {'Average' : 'mean', 'Total': 'sum'}})

# Aggregation adds a second level of header row, which can be flattend out after dropping the top level
popular.columns = popular.columns.droplevel(0)

# Copy the grouped data onto a dataframe (to use the cool methods of a dataframe later)
popular_df = pd.DataFrame(popular)

# Flatten out the header row
popular_df.reset_index()

# Rename the columns
popular_df = popular_df.rename(columns = {'size': 'Purchase Count',
                                           'Average': 'Item Price',
                                           'Total': 'Total Purchase Value'
                                         })
#List most popular 5
pop_summary_df = popular_df.sort_values(by='Purchase Count', ascending=False).head(5)

# Set the display format
pop_summary_df['Purchase Count'] = pop_summary_df['Purchase Count'].map('{:,.0f}'.format)
pop_summary_df['Item Price'] = pop_summary_df['Item Price'].map('${:,.2f}'.format)
pop_summary_df['Total Purchase Value'] = pop_summary_df['Total Purchase Value'].map('${:,.2f}'.format)

# Display Summary
pop_summary_df


# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[215]:


#Most Profitable
profitable_df = popular_df.nlargest(5, 'Total Purchase Value')

# Set the display format
profitable_df['Purchase Count'] = profitable_df['Purchase Count'].map('{:,.0f}'.format)
profitable_df['Item Price'] = profitable_df['Item Price'].map('${:,.2f}'.format)
profitable_df['Total Purchase Value'] = profitable_df['Total Purchase Value'].map('${:,.2f}'.format)

# Display Summary
profitable_df

