#!/usr/bin/env python
# coding: utf-8

# In[287]:


import sqlite3
import pandas as pd
import os

# changing the "current working directory"
os.chdir('/home/ec2-user/SageMaker/')

# load csv file into pandas dataframe
# reference: https://stackoverflow.com/a/28802613 
csvfile = "resources/phase3/simfin/us-income-ttm.csv"

dfUSINCOME = pd.read_csv(csvfile, sep=';') # reference https://stackoverflow.com/a/24606473
dfUSINCOME.columns = df.columns.str.replace(' ', '') # remove spaces in column names

# instructions for how to create a database file: https://www.sqlitetutorial.net/sqlite-python/creating-database/
# let create an empty database
db_file = "simfim.sqlite" # we need a name for our db file
conn = sqlite3.connect(db_file) # sqlite will create this file for us
table_name = "tblSimFin" # we need a name for our db table

# now we have everyting we need for our reference line above.
# let's put it together

dfUSINCOME.to_sql(table_name, conn, if_exists='replace', index=False)


# In[153]:


con = sqlite3.connect("resources/phase3/sp500/sp500.sqlite")


# In[ ]:





# In[59]:


#Q1 Observe the years with the highest differnce between High and Low in SP500
# Quick code to see lowest open ever
dfSP500[dfSP500.Open == min(dfSP500.Open)]


# In[ ]:





# In[ ]:





# In[386]:


#Create dataframe grouped by year and find the high for the year

dfsp500yearHigh = dfSP500.groupby(['year'], as_index = False)["High"].max()


# In[387]:


dfsp500yearHigh.head(10)


# In[361]:


#same as above except find the lowest low

dfsp500Low = dfSP500.groupby(['year'], as_index = False)["Low"].min()


# In[362]:


dfsp500Low.head(10)


# In[366]:


#Joining the two dataframes to create one where each year is grouped and has highest high along with lowest low


dfSP500MinMax = dfsp500yearHigh.set_index('year').join(dfsp500Low.set_index('year'))


# In[367]:


dfSP500MinMax.head(10)


# In[370]:


#Converting values to numeric values for subtraction


dfSP500MinMax['High'] = pd.to_numeric(dfSP500MinMax['High'])
dfSP500MinMax['Low'] = pd.to_numeric(dfSP500MinMax['Low'])


# In[371]:


dfSP500MinMax.head(10)


# In[372]:


#Create column to show difference between max High and min Low


dfSP500MinMax['Difference'] = dfSP500MinMax.High - dfSP500MinMax.Low


# In[373]:


dfSP500MinMax.head(10)


# In[376]:


#Sorting values descending order by difference.



dfSP500MinMax = dfSP500MinMax.sort_values(by = 'Difference', ascending = False)


# In[377]:


#Our Final Answer
#Years ordered by difference between highest high and lowest low throughout the year
#I created a years column earlier in the database, but on my review I think I accidentally deleted the code but the dataframe did not change


dfSP500MinMax.head(10)


# In[157]:


dfUSINCOME.columns


# In[160]:


#Q2
#Find Companies with 2x RD costs as SGA in 2018 sorted by Basic Shares
#Rename Research & Development as RD
dfUSINCOME = dfUSINCOME.rename(columns= {"Research&Development":"RD"})
dfUSINCOME = dfUSINCOME.rename(columns= {"Selling,General&Administrative":"SGA"})


# In[187]:


#Editing DB to only have those were RD costs are 2 times SGA costs
dfRD = dfUSINCOME[dfUSINCOME.RD > (2 * dfUSINCOME.SGA)]


# In[188]:


#Only wanted those in year 2018
dfRD = dfRD[dfRD.FiscalYear == 2018]


# In[197]:


#Sorting by basic shares descending

dfRD = dfRD.sort_values(by='Shares(Basic)', ascending = False)


# In[383]:


#Companies with RD costs 2x SGA Costs in year 2018, sorted by Basic Shares and Operating Income included
dfRD2 = dfRD[['Ticker', 'FiscalYear', 'RD', 'SGA', 'Shares(Basic)', 'OperatingIncome(Loss)']]


# In[384]:


dfRD2.head(10)


# In[211]:


dfUSINCOME = dfUSINCOME.rename(columns= {"OperatingIncome(Loss)":"OperatingIncome"})


# In[217]:


dfUSINCOME.columns


# In[228]:


dfUSINCOME[dfUSINCOME.OperatingIncome == max(dfUSINCOME.OperatingIncome)]


# In[239]:


dfUSINCOME = dfUSINCOME.rename(columns= {"Selling,General&Administrative":"SGA"})


# In[278]:


#Q3 Find the top earners by average Operating Income
#Sort Values by Operating Income

dfYear = dfUSINCOME.sort_values('OperatingIncome', ascending = False)


# In[271]:


#GroupBy Ticker Symbol and find Mean Operating Income

dfTopEarners = dfYear.groupby(["Ticker"], as_index = False)["OperatingIncome"].mean()


# In[273]:


dfTopEarners.head(10)


# In[276]:


#Sorting by Mean Operating Income


dfTopEarners = dfTopEarners.sort_values(by = 'OperatingIncome', ascending = False)


# In[277]:


#Our Top 10 Companies by Mean operating Income and our Answer
#Looks like the largest mean operating income belongs to Exon Mobile
dfTopEarners.head(10)


# In[409]:


#Q4
#What years had the largest revenu



dfRevenue = dfUSINCOME.groupby(['FiscalYear'], as_index = False)["Revenue"].max()


# In[411]:


dfRevenue.sort_values(by = "Revenue", ascending = False)


# In[412]:


#Q5
#What Fiscal Quarter shows the highest Average Revenues
#Decided on asking the question of who has the highest sum of Net Extraordinary Gains

#This was to find max of Operating Expense by Fiscal Quarter
dfAvgRev = dfUSINCOME.groupby(['FiscalPeriod'], as_index = False)["OperatingExpenses"].max()


# In[414]:


dfAvgRev.head(10)


# In[434]:


#an attempt

dfTicker = dfUSINCOME[["Ticker", "NetExtraordinaryGains(Losses)"]]


# In[436]:


dfTicker.head(5)


# In[446]:


#Group by Ticker symbol and show sum of Net Extraordinary Gains



dfGroup = dfTicker.groupby(['Ticker'], as_index = False)["NetExtraordinaryGains(Losses)"].sum()


# In[471]:


#Renamed Column to Net Gains

dfGroup = dfGroup.rename(columns = {"NetExtraordinaryGains(Losses)":"NetGains"})


# In[ ]:





# In[472]:


#Filter out all gains less than 0
dfGroup = dfGroup[dfGroup.NetGains > 0]


# In[475]:


#Sort by NetGains descending


dfGroup = dfGroup.sort_values(by = 'NetGains', ascending = False)


# In[476]:


#Our answer to top companies by sum of Net Gains

dfGroup.head(10)

