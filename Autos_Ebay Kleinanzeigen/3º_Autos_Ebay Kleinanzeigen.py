#!/usr/bin/env python
# coding: utf-8

# # Analysis of Auto Trade Classifieds in the platform of Ebay Kleinanzeigen (German Ebay portal for small classifieds)

# In[1]:


import numpy as np
import pandas as pd

autos = pd.read_csv('autos.csv', encoding ='Latin-1')


# In[2]:


autos


# In[3]:


info_autos = autos.info()
TOP_5_autos = autos.head(5)
LAST_5_autos = autos.tail(5)


# ### The DS contains 20 cols, being most of them strings (15) and only 5 integers. And 50.000 rows!
# ### From a first glympse we can tell that there are labels that need to be renamed, e g, yearOfRegistration, offerType, nrOfPictures. They are mainly written using CamelCase, instead of Pythons preferred snake_case. Columns that need to be retyped, e g, price. And columns that need to be completed due to the lack of values, e g, notRepairedDamage, fuelType, model, gearbox. These cols present cases of null values, not much, but they do.
# ### We need to do some basic Data Cleaning in the DS

# In[4]:


print(autos.columns)


# In[5]:


autos.rename(columns={'dateCrawled': 'date_crawled', 'name': 'name', 'seller':'seller', 'offerType':'offer_type', 'price': 'price', 'abtest': 'abtest',
       'vehicleType': 'vehicle_type', 'yearOfRegistration': 'registration_year', 'gearbox': 'gearbox', 'powerPS': 'power_ps', 'model': 'model',
       'odometer': 'odometer', 'monthOfRegistration': 'registration_month', 'fuelType': 'fuel_type', 'brand': 'brand',
       'notRepairedDamage': 'unrepaired_damage', 'dateCreated': 'ad_created', 'nrOfPictures': 'pics_number', 'postalCode': 'postal_code',
       'lastSeen': 'last_seen'}, inplace=True)


# In[6]:


autos.head(5)


# ### We just renamed all the cols, and changed them to a more Pythonic readable way. Changing them from CamelCase to Snake_case.
# ### Doing so we are not only harmonizing our DS but also preventing us from making any typo related mistakes.

# In[7]:


autos.describe(include='all')


# In[8]:


autos['pics_number'].value_counts()


# #### The column *pics_number* is populated only with the value 0. Therefore, there is no analytical value in having this column in our DataFrame (DF)

# In[9]:


autos['seller'].value_counts()



# #### The column *seller* has also no relevance in our DF, since all values point into the direction of private sales, and only one datapoint appear to be a comercial add. We can drop this column. 

# In[10]:


autos['offer_type'].value_counts()


# #### The same applies to *offer_type* col

# In[11]:


autos['price'].value_counts()


# #### The column *price* is a int64 type, but it has symbols in it and not only numbers. It needs to be cleaned!

# In[12]:


autos['odometer'].value_counts()


# #### Same thing applies to the *odometer* col. Although it is an integer type column we still have to deal with symbols in it (km). A cleansing need to be done!

# In[13]:


print(autos['abtest'].head(10))


# In[14]:


autos['power_ps'].max()


# #### The *power_ps* col has for sure an error in its max data point. Its retreiving the value of 17700. No car has that many horse power! Needs to be looked into and solved!

# In[15]:


autos['registration_month'].min()


# In[16]:


autos['registration_month'].value_counts()


# #### This column presents an abnormal number of 0's for a registration month. They should begin in 1 (first month of the year), and end in 12 (the last month). So more deepth into this trend should be taken care!

# In[17]:


autos['ad_created'].head(10)


# In[18]:


autos['postal_code'].head()


# In[19]:


autos['registration_year'].min()


# In[20]:


autos['registration_year'].max()


# In[21]:


autos['registration_year'].value_counts()


# #### In the col *registration_year* we have a similar problem as in the col *registration_month*. But here both on the max and min values (9999 and 1000). This data for sure is wrong. It can't be possible for a car to be registered on the year 1000 as in the year 9999!

# ### Both *price* and *odometer* are numeric cols saved as text in our DF, and with symbols in them. What we are goint to do next is clean this cols, convert them to a numeric type, and rename them

# In[22]:


# cleaning and converting the price col:
autos['price'] = autos['price'].str.replace('$', '').str.replace(',','').astype('int64')


# In[23]:


autos['price'].head(3)


# In[24]:


# cleaning and converting the odometer col:
autos['odometer'] = autos['odometer'].str.replace('km', '').str.replace(',','').astype('int64')


# In[25]:


autos.rename(columns={'odometer':'odometer_km'}, inplace=True)


# In[26]:


autos['odometer_km'].head(3)


# #### Investigating deeper these 2 cols (*price* and *odometer_km*) and looking for outliers in both of them

# In[27]:


autos['price'].describe()


# In[28]:


#autos['price'].unique().shape
#autos['price'].describe()
#autos['price'].max()
#autos['price'].min()
autos['price'].value_counts().sort_index(ascending=False).head(20)
#autos['odometer_km'].describe()
#autos['odometer_km'].value_counts().sort_index(ascending=True).tail(20)


# In[29]:


autos['price'].value_counts().sort_index(ascending=True).head(50)


# In[30]:


autos[autos['price'] >= 999990].head(9)


# #### In the cols *odometer_km* we could not detect any incongruences/outliers in the data points. 
# #### The same thing cant't be said about the col *price*. Here we could find several inconsistencies. Plenty of data points with the value 0 (#1421), as also some data points with unrealistic high price values for used cars (>999990). E.g., Fiat_Punto for 12345678€; Volkswagen_Jetta_GT for 999990€; Ford_Focus_Turnier_1.6_16V_Style for 999999€! 
# #### What we decided to do was to define a cut-off for the col *price* and remove these outliers. Applying a filter (boolean indexing) to remove all the prices that stood between 99€ and no more than 999990€:

# In[31]:


autos = autos[(autos['price'] < 999990) & (autos['price'] >= 99)]
#autos['price'] = autos[autos['price'].between(99,999990)]


# In[32]:


autos['price'].describe()


# In[33]:


autos.shape


# In[34]:


autos_date_crawled_dist = autos['date_crawled'].value_counts()


# In[35]:


date_crawled = autos['date_crawled'].str[:10]


# In[36]:


date_crawled.head()


# In[37]:


date_crawled.value_counts(dropna=False, normalize=True).sort_index(ascending=True)


# #### All Data was crawled between the beginning of month 03 (March) and month 04 (April) of the year 2016. 

# In[38]:


ad_created = autos['ad_created'].str[:10]


# In[39]:


ad_created.value_counts(dropna=False, normalize=True).sort_index(ascending=True)


# #### While all the ads crawled were created in the website between month 05 (May) of 2015 and month 04 (April) of 2016. So we have approximately 1 year of Data in our DataSet.
# #### The day that collected more ads being 03-04-2016 with approximately 4% of all the ads crawled. 

# In[40]:


ad_created_month = autos['ad_created'].str[:7]


# In[41]:


ad_created_month.value_counts(dropna=False, normalize=True)


# #### The month with more data points in our DS is March 2016 (83,7%), followed by April (16,1%). 
# #### This is related to the time when the Data was crawled, months 03 beginning of 04, and the rotation of the ads in the website - high!

# In[42]:


last_seen = autos['last_seen'].str[:10]


# In[43]:


last_seen.value_counts(dropna=False, normalize=True).sort_index(ascending=True)


# #### This col is ranged as the date_crawled col!

# In[44]:


autos['registration_year'].describe()


# #### From the descriptive analysis of this col we can observe that the average year of registration for the vehicles offered is 2004. But its also visible that we have multiple data points that are probably not correct. We have a min value of 1000 and a max value of 9999. This registration dates can't be right!

# In[45]:


autos['registration_year'].value_counts(normalize=True).sort_index()


# In[46]:


autos[autos['registration_year'] == 2017].head(10)


# #### Because our data was crawled during the years of 2015-2016 we cannot have registration years in our ads that goes beyond the year of 2016. Nor registrations prior to 1900 (the first car was invented around 1885/1886)
# #### Although the amount of data representing the *registration_year* of 2017 is still meaningful, accruing to approx 3%, we still have to remove this data points because they mislead our analysis with false conclusions!
# #### Data prior to the *registration_year* of 1900 is not so significant!
# #### We now are going to assume a cut-off for our *registration_year* col between 1900-2016 and filter our data:

# In[47]:


autos = autos[(autos['registration_year'] >= 1900) & (autos['registration_year'] <= 2016)]


# In[48]:


autos['registration_year'].value_counts(normalize=True).sort_index(ascending=True)


# #### Checking the unique values in the *brand* col:

# In[49]:


autos['brand'].unique()


# In[50]:


autos['brand'].value_counts().head(20)


# ### VW comes highlighted at number 1 being by far the brand with more cars advertised in Ebay Kleinenanzeigen, with 9803 ads. Followed by BMW with 5109 ads.
# ### Closing top 3 with most ads comes the brand Opel, with 4975 offers. Closely followed by Mercedes with 4480.
# ### The last manufacturer from the top 20 brands in our DataSet is Mini. Offering a scarce 408 cars for sale!

# In[51]:


top_20_brands_mean_price = {}
top_20 = autos['brand'].value_counts().head(20)

for b in top_20.index:
    autos_top_20 = autos[autos['brand'] == b]
    avg_price_top_20 = round(autos_top_20['price'].mean(),2)
    top_20_brands_mean_price[b] = avg_price_top_20

print(sorted(top_20_brands_mean_price.items(), key=lambda kv: kv[1]))


# #### Our top 5 pricey from the 20 most common brands in our ads are: 
#     Mini - 10639.45€; 
#     Audi - 9380.72€; 
#     Mercedes Benz - 8672.65€; 
#     BMW - 8378.43€; 
#     Skoda - 6409.61€
# #### The bottom 5 from the 20 most common brands in our ads are are:
#     Smart - 3596.4€;
#     Peugeot - 3113.86€;
#     Opel - 3003.16€;
#     Fiat - 2827.68€;
#     Renault - 2493.88€

# #### Now we are going to aggregate our most common 20 brands in our ads by their average (avg) mileage in order to check if there is any relation between avg mileage and avg price:

# In[52]:


top_20_brands_mean_mileage = {}

for b in top_20.index:
    autos_top_20 = autos[autos['brand'] == b]
    avg_mileage_top_20 = round(autos_top_20['odometer_km'].mean(),2)
    top_20_brands_mean_mileage[b] = avg_mileage_top_20

print(top_20_brands_mean_mileage)


# #### Combining both dictionaries, avg_price and avg_mileage, into 1 DataFrame in order to facilitate their comparison and any links between both of them:

# In[53]:


mileage_top_20_series = pd.Series(top_20_brands_mean_mileage)


# In[54]:


price_top_20_series = pd.Series(top_20_brands_mean_price)


# In[55]:


mileage_price_top_20_df = pd.DataFrame(mileage_top_20_series, columns=['top_20_brands_mean_mileage'])
mileage_price_top_20_df.info()


# In[56]:


mileage_price_top_20_df.head()


# In[57]:


mileage_price_top_20_df['top_20_brands_mean_price'] = price_top_20_series


# In[58]:


mileage_price_top_20_df.head(20)


# ### The relation between avg_mileage and avg_price is obvious, and we can explain why mini used cars are the most expensive ones although being a middle price range brand!
# ### Mini is the brand with less mileage on its used cars, an avg of 88308.82 km's. While top brands like BMW, Mercedes Benz, and Audi are among the ones with more mileage on an avg. Scoring 132673.71; 131025.67; 129245.40 km's, respectively!
# ### This might explain in part why these 3 brands, although top ones, all come after mini in their avg_price, due to their high mileage numbers, and why Skoda, although an entry/middle price range brand comes in 5th with an avg_price of 6409.61€, perhaps sustained by their short avg_mileage, compared to our top 3 brands, with 110906.70 km's

# ### Now, while still working with our top 20 brands, let's try to investigate if there is any relation between the age of the cars, average price and  their average mileage!
# #### First we will need to creat a column only for the number of years of our cars. All we have is their registration year, and the last time the ad has been seen. With this info we can obtain their number of years.

# In[59]:


autos['last_seen'].describe()


# In[60]:


autos['last_seen_year'] = autos['last_seen'].str.split('-').str[0].astype(int)


# In[61]:


autos['last_seen_year'].head()


# In[62]:


autos


# In[63]:


autos['n_years'] = autos['last_seen_year'] - autos['registration_year']


# In[64]:


autos['n_years'].describe()


# #### With our new column (*n_years*) created and added to our DataFrame (DF), we can now calculate the avg number of years for our top 20 brands, and assess the relationship between avg_years, avg_price and avg_mileage for our top 20 brands!
# #### We can also check that the avg number of years for all the ads from our DF is around 13 years!

# In[65]:


top_20_brands_mean_n_years = {}

for b in top_20.index:
    autos_top_20 = autos[autos['brand'] == b]
    avg_n_years_top_20 = round(autos_top_20['n_years'].mean(),2)
    top_20_brands_mean_n_years[b] = avg_n_years_top_20
    
print(top_20_brands_mean_n_years)


# #### It's immediatly visible what's our number 1 brand in terms of aging: Volvo, with an average of 15 years (15.4).
# #### At number 2 with and avg of almost 14 years we have Mercedes Benz (13.95) 
# #### And closing our top 3 for the average number of years for our top 20 brands in Ebay Kleinenanzeige, we have Opel, with and avg of 13.74 years!
# #### Is there any relationship between age and price, or between age, price, and mileage?? Let's find out!!

# In[66]:


n_years_top_20_series = pd.Series(top_20_brands_mean_n_years)


# In[67]:


mileage_price_top_20_df['top_20_brands_mean_n_years'] = n_years_top_20_series


# In[68]:


mileage_price_top_20_df.head(20)


# ### The relationship between these 3 inputs is pretty obvious!
# ### Now we have a better explanation why Mini comes taged with the highest avg price, less km's and the less aged of our top 20 brands with an average of 8 years!
# ### Skoda enters our top 5 pricey cars probably due to their mix of low age (9.45 years) and not so high mileage
# ### Volvo, despite its mix between high avg mileage and high avg years, doesn't come with the lowest price tag. This is probably better explained due to the fact that their car models aim a more medium/high segment, thus with higher price tags than Renault or Opel, for example!
# ### Regarding our top 3 brands, and the more comparable ones due to their nature in terms of segment, Mercedes Benz, BMW, and Audi, it's clear why Audi comes at second in terms of avg price. It is the brand both with less avg mileage and avg number of years, 129245.40 km's and 11.83 years. And although these 3 brands, from all our top 20 brands, are probably tagged with the higher prices when they are new, none of the 3 come at number 1 in the avg price for used cars! the reason being almost certainly the mix between high number of years and high mileage! 
# ### It is importante to point out that a more precise analysis would to be made if we had an average price of the cars as new, and compare not the most popular ones in our DF, but the ones from the same segment, with similar sell as new price tags!

# ### Next let's investigate if there is a difference in price between cars that have unrepaired damage and cars that don't have unrepaired damage not only for our top 20 brands, but for all the ads in our DataFrame. And if there is a difference, let's try to calculate it's magnitude!
# 
# ##### But first let's replace any german words we might have in our col *unrepaired_damage* for english ones:

# In[69]:


autos['unrepaired_damage'].value_counts(dropna=False)


# In[70]:


autos['unrepaired_damage'] = autos['unrepaired_damage'].str.replace('nein', 'no')


# In[71]:


autos['unrepaired_damage'] = autos['unrepaired_damage'].str.replace('ja', 'yes')


# In[72]:


autos['unrepaired_damage'].value_counts(dropna=False)


# #### Calculating the avg price for both damaged and undamaged cars:

# In[73]:


mean_damaged = round(autos[autos['unrepaired_damage'] == 'yes'].loc[:,'price'].mean(),2)


# In[74]:


mean_undamaged = round(autos[autos['unrepaired_damage'] == 'no'].loc[:,'price'].mean(),2)


# In[75]:


print(abs(mean_damaged - mean_undamaged))


# In[76]:


print(abs(mean_damaged - mean_undamaged)/(mean_undamaged)*100)


# ### We can see a huge price gap between damaged and undamaged cars, ca. 4909€, or 68.4% more on the price for the undamaged ones!

# ### Let's try now to compute the avg price of all our ads taking into consideration their age!
# 
# #### First we need to define our intervals for the number of years that the cars have. And then calculate the average for each interval.

# #### Defining our intervals for the number of years of our advertised cars and the average price for each interval:

# In[77]:


# avg_price_0-5:
round(autos[(autos['n_years'] >= 0) & 
                      (autos['n_years'] < 5)].loc[:,'price'].mean(),2)


# In[78]:


# avg_price_5-10:
round(autos[(autos['n_years'] >= 5) & 
                       (autos['n_years'] < 10)].loc[:,'price'].mean(),2)


# In[79]:


# avg_price_10-15:
round(autos[(autos['n_years'] >= 10) & 
                       (autos['n_years'] < 15)].loc[:,'price'].mean(),2)


# In[80]:


# avg_price_15-20: 
round(autos[(autos['n_years'] >= 15) & 
                       (autos['n_years'] < 20)].loc[:,'price'].mean(),2)


# In[81]:


# avg_price_+20: 
round(autos[autos['n_years'] >= 20].loc[:,'price'].mean(),2)


# ### An interesting fact is that cars start to appreciate from age 20 onwards.
# ### The avg price for cars between age 0 and 5 is 15438.46€. That price tag drops approx 5000€ when our age range increases 5 years (5-10).
# ### The avg price for the cars aged between 10-15 is moreless 30% of the avg seen in the first range (0-5).
# ### And we can afirme that cars hit their residual avg value when they reach their interval age of 15-20.
