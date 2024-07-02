#!/usr/bin/env python
# coding: utf-8

# # College Majors_4º_Visualization_Plots
#     Basic earnings and labour force info of grads from 2010-2012

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')


# #### Reading the DataSet *recent-grads.csv*, and returning its first row:

# In[2]:


recent_grads = pd.read_csv('recent-grads.csv')
recent_grads.iloc[0]


# #### Top 5 Majors by median earnings:

# In[3]:


recent_grads.head()


# #### Bottom 5 Majors by median earnings:

# In[4]:


recent_grads.tail()


# ### We can immediately visualize 2 major trends:
#     - The Top 5 best paid Majors are in the Engineering Fields, while 
#     the Bottom 5 are in the areas of Social work;
#     - The Top 5 best paid Majors are populated mainly by working men, 
#     while the Bottom 5 is reserved almost entirely to women.

# #### A descriptive analysis of the DataSet: 

# In[5]:


recent_grads.describe(include='all')


# ### Women are the predominant sex in all the the job outcomes of students who graduated from college between 2010-2012, with and average (avg) of 22.646 per category Vs. 16.723 men.
# ### On avg only a very small sample of the grads are Unemployed, 2.416.
# ### The maximum Median wage is of 110.000 per year (*Major in PETROLEUM ENGINEERING*). While the minimum Median Wage is of 22.000 per year (*Major in LIBRARY SCIENCE*). 

# #### Cleaning our DataSet and removing the rows with NaN values in order to pass columns in Matplotlib with matching values so that no erros occur:

# In[6]:


raw_data_count = recent_grads.shape[0]
print(raw_data_count)


# In[7]:


recent_grads.dropna(axis=0, inplace=True)


# In[8]:


cleaned_data_count = recent_grads.shape[0]
print(cleaned_data_count)


# #### Only 1 row was dropped from the original DataSet. Meaning that only 1 row in the entire DataSet had missing values! We now have 172 rows instead of the original 173!

# #### Generating some Scatters plots: 

# In[9]:


recent_grads.plot(x='Sample_size', y='Median', kind='scatter', title='Sample_size Vs. Median', figsize=(8,5))


# In[10]:


recent_grads.plot(x='Sample_size', y='Unemployment_rate', kind='scatter', title='Sample_size Vs. Unemployment_rate', figsize=(8,5))


# In[11]:


recent_grads.plot(x='Full_time', y='Median', kind='scatter', title='Full_time Vs. Median', figsize=(8,5))


# In[12]:


recent_grads.plot(x='ShareWomen', y='Unemployment_rate', kind='scatter', title='ShareWomen Vs. Unemployment_rate', figsize=(8,5))


# In[13]:


recent_grads.plot(x='Men', y='Median', kind='scatter', title='Men Vs. Median', figsize=(8,5))


# In[14]:


recent_grads.plot(x='Women', y='Median', kind='scatter', title='Women Vs. Median', figsize=(8,5))


# ### There is no positive relation between the most popular majors and the amount of money students make! What we can observe is that the majority of the less popular majors grant the students a paycheck bellow 40k per year. Other not so popular majors, in a very less percentage, grant students an annual salary of 60k. 

# ### The majority of majors that are populated by women are situated bellow the 60k income per year, with a focus around the 40k per year.
# ### Observations in women above an income of 60k per year are very scarce and limited to very few examples! 
# ### The majors that are most popular among women all fall under 60k per year! 

# ### It seems there is no obvious link between the number of full-time employees and the median salary.
# ### Apart from that we can tell that the majors were the number of full-time employees is low is were the most obsvervations between a median salary of 20k-40k per year are observed.
# ### We should also pinpoint the lack of positive relation between the number of students in full-time jobs and their median salary per year. We should be led to think that way, but in reality that doesn't happen!

# #### Generating some Histogram plots:

# In[15]:


recent_grads['Sample_size'].hist(bins=25, range=(0,5000))


# In[16]:


recent_grads['Median'].hist(bins=12, range=(0,120000))


# In[17]:


recent_grads['Employed'].hist(bins=20, range=(0,310000))


# In[18]:


recent_grads['Full_time'].hist(bins=12, range=(0,252000))


# In[19]:


recent_grads['ShareWomen'].hist(bins=10, range=(0,1), color='red')


# In[20]:


recent_grads['Unemployment_rate'].hist(bins=20, range=(0,0.3), color='purple')


# In[21]:


recent_grads['Men'].hist(bins=20, range=(0,310000), color='yellow')


# In[22]:


recent_grads['Women'].hist(bins=20, range=(0,310000), color='pink')


# #### Another way of plotting all these histograms, but writing far less code, resorting to a for loop:

# In[23]:


cols = ['Sample_size', 'Median', 'Employed', 'Full_time', 'ShareWomen', 'Unemployment_rate', 'Men', 'Women']

fig, ax = plt.subplots(figsize=(12,30))
plt.xticks([])
plt.yticks([])
           
           
for i in range(8):
    ax = fig.add_subplot(8,1,i+1)
    ax = recent_grads[cols[i]].hist(bins=10)


# ### The most commom median salary is observed in the range between 30k and 40k per year!
# ### Its fair to say that more than half of all majors (96 Majors/56%) have a percentage of more than 50% of women based on the *ShareWomen* histogram. While men control the other 76 Majors, arround 44%.

# In[24]:


from pandas.plotting import scatter_matrix


# In[25]:


scatter_matrix(recent_grads[['Sample_size', 'Median']], figsize=(10,8))


# ### We can observe a relation between the median salary and the sample size. Low sample sized majors are more common in the median salary range of 20k-40k

# In[26]:


scatter_matrix(recent_grads[['Sample_size', 'Median', 'Unemployment_rate']], 
             figsize=(10,8))


# ### The frequency of ocurrences in the Unemployment_rate is higher between 5%-10%. This is also the interval were we see more cases of median salary bellow 40k per year!

# ####  Using some bar plots to compare the percentages of women and also of the Unemployment rate in all the Majors, from the top and bottom 10:

# In[27]:


recent_grads[:10].plot.bar(x='Major',y='ShareWomen' ,rot=90, color='pink')


# In[28]:


recent_grads.tail(10).plot.bar(x='Major', y='ShareWomen', rot=90, color='pink')


# ### Its interesting to see that the percentage of women is much higher in the Majors that return a lower median income per year than the ones that pay considerably better! The exception is seen only in one Major, *Astronomy and Astrophysics*. Being this the only Major that figures in the top 10 of the most well paid were women are predominante!
# ### Another interesting fact is that all the top 10 paying Majors are Engineerings or very technical ones, and the bottom 10 is composed by social/art/language sciences. In fact, this attests what we´ve already concluded in the first steps of this analysis. 
# ### Are men more pron to numbers/engineerings than women? Are women more pron to social/art/languages than men? Or is this a stigma/prejudice of a macho society thats pushing women to supposedly women orientated Majors that brings them a lower income compared to others dominated by men? 
# ### What the numbers do tell us is that women, although being predominants in the majority of all Majors (56%) are the ones integrating the majority of the lower income ones, and therefore receiving a far lower median income than men!

# In[29]:


recent_grads.head(10).plot.bar(x='Major', y='Unemployment_rate', color='grey')


# In[30]:


recent_grads[162:].plot.bar(x='Major', y='Unemployment_rate', color='grey')


# ### Unemployment rates are slightly higher in the bottom 10 Majors. Despite that, the biggest Unemployment rate is seen in 1 Major of the top 10, *Nuclear Engineering*, with approximetely 18% of Unemployment rate! 

# #### Exploring in a more depth the relation between *Men*, *Women* and their number in each category of Majors:

# In[31]:


recent_grads.groupby('Major_category')['Men', 'Women'].agg('sum').plot.barh(figsize=(10,10))


# ### As we previously concluded the disparity in *Engineering*, between women and men, is gigantic! This gap, although not in such proportion, can also be seen in the Major category *Computers & Mathematics* !
# ### The opposite is easily seen in areas like *Psychology & Social Work*, *Education*, *Arts* and *Humanities*!
# 

# #### Plotting 2 box plots to explore the distributions of median salaries and unemployment rate:

# In[32]:


recent_grads.boxplot(column=['Median'], figsize=(5,6))
plt.ylim(0,120000)


# ### Half of the values in the *Median* column (median salaries) are concentrated in a very small range, around 35k-45k. 
# ### The range of the top 25% of the distribution of values is much higher (45k-61k) than the bottom 25% (21k-32k). This means that the lower incomes are more concentrated in a smaller range!
# ### It's also visible the existence of some outliers in the very high side. That may have influenced positively our *Median* mean and might explain the rather slight difference towards its median value, 40k Vs. 37k. 

# In[33]:


recent_grads.boxplot(column='Unemployment_rate', figsize=(5,6))
plt.ylim(-0.03, 0.19)


# ### 50% of the values in the *Unemployment_rate* col are distributed around 5% and 8% rates! 
# ### The distribution of values in this indicator is pretty even. No quartile ranges significantly different from other!
# ### The median value of the *Unemployment_rate* is around 7%! 
