#!/usr/bin/env python
# coding: utf-8

# # Exit Surveys - DETE & TAFE

# ### Analysing the Department of Education, Training and Employment (DETE) and the Technical and Further Education (TAFE) exit surveys, and trying to answer questions such as: 
#     - Are employees who only worked for the institutes for a short period of time resigning due to some kind of dissatisfaction? What about employees who have been there longer?
#     - Are younger employees resigning due to some kind of dissatisfaction? What about older employees?
# ### The aim of the project is to try to grasp the reasons for the non retention of employees in order to better counter this trend.
# 
# ### For that we will rely in 2 very similar DataSet's, one from DETE and the other one from TAFE.

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')


# In[2]:


dete_survey = pd.read_csv('dete_survey.csv')
tafe_survey = pd.read_csv('tafe_survey.csv')


# In[3]:


dete_survey.info()
dete_survey.head()


# In[4]:


tafe_survey.info()
tafe_survey.head()


# In[5]:


dete_survey.isnull().sum().sort_values()


# In[6]:


dete_survey['Aboriginal'].value_counts(dropna=False)


# In[7]:


tafe_survey.isnull().sum()


# In[8]:


tafe_survey['Gender. What is your Gender?'].value_counts(dropna=False)


# In[9]:


tafe_survey['Workplace. Topic:Does your workplace promote a work culture free from all forms of unlawful discrimination?'].value_counts(dropna=False)


# #### In the DETE Dataset (DS) we have innumerable missing values (NaN's). Mainly in categorizing columns such as *Aboriginal; Torres Strait; South Sea; Disability; NESB*. Should we eleminate such cols? Are they really necessary to answer our questions? Or should we maintain them and assume that all the missing values are No's?
# #### Also the *Business Unit* and the *Classification* cols have a relevant number of NaN's.
# #### Regarding the TAFE Dataset we see a less number of NAN's, but some messy and rather complex column names.
# #### In the TAFE DS, more particularly in the *InductionInfo* cols, we see a pattern in the number of NAN's. Standing bettween 147-149.
# #### Both DS's contains plenty of cols that we probable won't need to answer our questions. And they both contain shared info but with slightly different names.
# #### Some cols in the DETE DS contain the designation *Not Stated* and they are not beeing treated as NaN's.

# In[10]:


dete_survey = pd.read_csv('dete_survey.csv', na_values=['Not Stated'])
dete_survey_updated = dete_survey.drop(dete_survey.columns[28:49], axis=1)


# In[11]:


dete_survey_updated.head()


# In[12]:


tafe_survey_updated  = tafe_survey.drop(tafe_survey.columns[17:66], axis=1)
tafe_survey_updated.head()


# #### Above we droped some cols in both DS's that were not important for our analysis, nor to answer our questions.
# #### We've also treated the *Not Stated* info that the DETE DS had in some rows as a NaN value. Since that's exactly what it is, so it should be labeled as such. 

# ### Standardizing the columns names in both DataSet's.

# In[13]:


dete_survey_updated.columns


# In[14]:


dete_survey_updated.columns = dete_survey_updated.columns.str.lower().str.strip().str.replace(" ", "_")
dete_survey_updated.columns


# In[15]:


tafe_survey_updated.columns


# In[16]:


tafe_survey_updated = tafe_survey_updated.rename(columns={'Record ID': 'id', 
                                         'CESSATION YEAR': 'cease_date',
                                         'Reason for ceasing employment': 'separationtype',
                                         'Gender. What is your Gender?': 'gender',
                                         'CurrentAge. Current Age': 'age',
                                         'Employment Type. Employment Type': 'employment_status',
                                         'Classification. Classification': 'position',
                                         'LengthofServiceOverall. Overall Length of Service at Institute (in years)': 'institute_service',
                                         'LengthofServiceCurrent. Length of Service at current workplace (in years)': 'role_service'})
tafe_survey_updated.columns


# In[17]:


dete_survey_updated.head()


# In[18]:


tafe_survey_updated.head()


# #### We renamed some cols from the TAFE dataset, in order to make them more  simple and easy to refer to.
# #### We also standardized the cols names/format from the DETE DS. Making the info easier to understand and cleaner.

# ### Further cleaning both our DataSet's and eliminating unnecessary info.

# In[19]:


dete_survey_updated['separationtype'].value_counts()


# In[20]:


tafe_survey_updated['separationtype'].value_counts()


# In[21]:


dete_resignation = dete_survey_updated[(dete_survey_updated['separationtype']==
                    'Resignation-Other reasons') | 
                   (dete_survey_updated['separationtype']==
                    'Resignation-Other employer') |
                   (dete_survey_updated['separationtype']==
                    'Resignation-Move overseas/interstate')]
dete_resignation.head()


# In[22]:


dete_survey_updated = dete_resignation.copy()
dete_survey_updated.head()


# In[23]:


tafe_resignation = tafe_survey_updated[tafe_survey_updated['separationtype']
                                       =='Resignation']
tafe_resignation.head()


# In[24]:


tafe_survey_updated = tafe_resignation.copy()
tafe_survey_updated.head()


# #### Since our question is focused only on the employees who quited due to *Resignation* theres no need for us to have our Dataset's populated with datapoints referring to other separation types. Therefore, we only selected in both DS's the info that matched this criteria, and eliminated all the other that was unnecessary. 

# ### Further investigating our core cols for our analysis (*cease_date* and *dete_start_date*). Formating and cleaning them. 

# In[25]:


dete_survey_updated['cease_date'].value_counts()


# In[26]:


dete_survey_updated['cease_date'] = dete_survey_updated['cease_date'].str.replace('/', ' ').str.split(' ').str[-1]


# In[27]:


dete_survey_updated['cease_date']=dete_survey_updated['cease_date'].astype('float64', inplace=True)


# In[28]:


dete_survey_updated['cease_date'].value_counts(dropna=False).sort_index(
ascending=True)


# In[29]:


dete_survey_updated['cease_date'].dtype


# In[30]:


dete_survey_updated['dete_start_date'].dtype


# In[31]:


dete_survey_updated['dete_start_date'].value_counts()


# In[32]:


tafe_survey_updated['cease_date'].value_counts(dropna=False).sort_index(ascending=True)


# In[33]:


tafe_survey_updated['cease_date'].dtype


# In[34]:


tafe_survey_updated['institute_service'].value_counts(dropna=False).sort_index(ascending=True)


# In[35]:


boxplot_dete = dete_survey_updated.boxplot(column=['cease_date'], grid=False)
boxplot_dete.set_ylim(2009,2014)
boxplot_dete.tick_params(bottom='off', top='off', left='off', right='off')

for key, spine in boxplot_dete.spines.items():
    spine.set_visible(False)



# In[36]:


boxplot_tafe = tafe_survey_updated.boxplot(column=['cease_date'], grid=False)
boxplot_tafe.set_ylim(2008, 2014)
boxplot_tafe.tick_params(top='off', bottom='off', left='off', right='off')

for key, spine in boxplot_tafe.spines.items():
    spine.set_visible(False)


# #### We were further cleaning and analyzing our core cols in both our Dataset's (*cease_date*) and other cols in the DETE DS such as *dete_start_date*.
# #### We cleaned the data and extracted only the year, and also converted the data to a numeric type(float), in order to better work with it.
# #### We concluded that apart from this, there were no need to futher modify the Data. The datapoints seem to be correct and rather realistic. The *cease_date* in the DETE Dataset evolves around the years 2006-2014. While in the TAFE is between 2009-2013

# ### Standardizing the time spent in both institutes.

# In[37]:


dete_survey_updated['institute_service'] = dete_survey_updated['cease_date']-dete_survey_updated['dete_start_date']


# In[38]:


dete_survey_updated.head()


# In[39]:


dete_survey_updated['institute_service'].value_counts(dropna=False).sort_index(ascending=True)


# #### Created a new col in the DETE Dataset, *institute_service*, in order to standardize the information related to the time, in years, spent in the institute. This piece of information was in the TAFE DS so we needed to add it also to the DETE

# ### Trying to aggregate the info in the different Dissatisfaction cols in both Dataset's into one columns only.

# In[40]:


tafe_survey_updated['Contributing Factors. Dissatisfaction'].value_counts(
dropna=False)


# In[41]:


tafe_survey_updated['Contributing Factors. Job Dissatisfaction'].value_counts(
dropna=False)


# In[42]:


def update_vals(element):
    if element == '-':
        return False
    elif pd.isnull(element):
        return np.nan
    else:
        return True
    
    
tafe_survey_updated[['Contributing Factors. Job Dissatisfaction', 
                     'Contributing Factors. Dissatisfaction']] = tafe_survey_updated[['Contributing Factors. Job Dissatisfaction', 
                     'Contributing Factors. Dissatisfaction']].applymap(
    update_vals)


# In[43]:


# Checking if the function update_vals and the process ran smoothly:
tafe_survey_updated['Contributing Factors. Job Dissatisfaction'].value_counts(
    dropna=False)


# In[44]:


# Checking if the function update_vals and the process ran smoothly:
tafe_survey_updated['Contributing Factors. Dissatisfaction'].value_counts(
dropna=False)


# In[45]:


# creating a new col, dissatisfied, in TAFE dataset:
tafe_survey_updated['dissatisfied'] = tafe_survey_updated[['Contributing Factors. Job Dissatisfaction', 
                     'Contributing Factors. Dissatisfaction']].any(
axis=1, skipna=False)


# In[46]:


# copying and creating a new DF, tafe_resignations_up, from tafe_survey_updated:
tafe_resignations_up = tafe_survey_updated.copy()


# In[47]:


tafe_resignations_up.head()


# In[48]:


dete_dissatisfaction_cols = ['job_dissatisfaction', 'dissatisfaction_with_the_department',
                            'physical_work_environment', 'lack_of_recognition',
                            'lack_of_job_security', 'work_location',
                            'employment_conditions', 'work_life_balance',
                            'workload']
dete_survey_updated['dissatisfied'] =  dete_survey_updated[dete_dissatisfaction_cols].any(
axis=1, skipna=False)


# In[49]:


# copying and creating a new DF, dete_resignations_up, from dete_survey_updated: 
dete_resignations_up = dete_survey_updated.copy()


# In[50]:


dete_resignations_up.head()


# #### We just compiled all the info that was related to the dissatisfaction motives into one single column, *dissatisfied*. And sorted it by True of False. So if an employee had any of the innumerous dissatisfaction reasons pinned as True it felt into the True category of the newly created col *dissatisfied*

# ### Now its time to combine both Dataset's into one.

# In[51]:


# creating a new col to identify the rows that belong to the DETE DS:
dete_resignations_up['institute'] = 'DETE'
dete_resignations_up.head()


# In[52]:


# creating a new col to identify the rows that belong to the TAFE DS:
tafe_resignations_up['institute'] = 'TAFE'
tafe_resignations_up.head()


# In[53]:


# combining both Dataset's into a major one, combined, using the concat method:
combined = pd.concat([dete_resignations_up, tafe_resignations_up],
                     ignore_index=True, axis=0)


# In[54]:


combined.columns.value_counts()


# In[55]:


# dropping cols with a number of less than 500 non null values:
combined_updated = combined.dropna(thresh=500, axis=1).copy()


# In[56]:


combined_updated.shape


# In[57]:


combined_updated.head()


# In[58]:


combined_updated['institute_service'].value_counts(dropna=False)


# #### We just changed our 2 Dataset's (DETE and TAFE) and merged it into a single one, *combined*. 
# #### We did so recurring to the concat method in a row level (axis=0), in order to preserve and combine the shared cols between the 2 DS's. We also did it because our focus is on the col *institute_service* and we wanted all the values from both DS's to be 'under' this col.
# #### Some more cleaning was made in the *combined* Dataset arriving to the *combined_updated* DS. This was achieved by dropping the columns that didn't had at least 500 non noll values.

# ### Categorizing and 'bin' the range of values in the *institute_service* column. And adding an extra col - *service_cat* with that info to the *combined_updated* Dataset.

# In[59]:


# checking if the data type of the institute_service col
# is in a str/object type in order to work on it with
# vectorized str methods:
combined_updated['institute_service'].dtype


# In[60]:


# cleaning and modifying some tricky datapoints in the Series
# the purpose is to then change the dtype of the col to a
# float type:
combined_updated['institute_service'] = combined_updated['institute_service'
                                                        ].str.replace(
    'Less than 1 year', '0').copy()


# In[61]:


combined_updated['institute_service'] = combined_updated['institute_service'
                                                        ].str.replace(
    'More than 20 years', '21').copy()


# In[62]:


combined_updated['institute_service'
                ] = combined_updated[
    'institute_service'].str.split('-').str.get(-1).copy()


# In[63]:


combined_updated['institute_service'].value_counts(dropna=False)


# In[64]:


# changing again the data type of the col to a float:
combined_updated['institute_service'] = combined_updated[
    'institute_service'].astype('float').copy()


# In[65]:


combined_updated['institute_service'].dtype


# In[66]:


# creating our own function - map_service_years - that 
# will let us categorized into 4 main categories - New;
# Experienced; Established; Veteran - the several number 
# of years spent in the company that ranges from 0 to 21:
def map_service_years(element):
    if element < 3:
        return 'New'
    elif element >= 3 and element <= 6:
        return 'Experienced'
    elif element >= 7 and element <= 10:
        return 'Established'
    elif pd.isnull(element):
        return np.nan
    else:
        return 'Veteran'

# applying our function to a element-wise method - 
# Series.apply() and copying the changes back to a new
# col named service_cat:
combined_updated['service_cat'] = combined_updated[
    'institute_service'].apply(map_service_years).copy()


# In[67]:


# validating the values/categories and checkin the new col:
combined_updated['service_cat'].value_counts(dropna=False)


# #### We ended up with adding a new column, *service_cat*, with 4 categories to our Dataset. 
# #### This is a *sine qua non* operation to tackle our questions. Without it, how could we answer the dissatisfaction on a time-spent-working level? 

# ### Doing our first piece of analysis - working on the *dissatisfied* col in order to answer questions such as: How many workers, in terms of percentage, fall into the category dissatisfied and how many don't.

# In[68]:


#checking how many and what kind of values populate our Series:
combined_updated['dissatisfied'].value_counts(
dropna=False)


# In[69]:


# filling the 8 missing values in the dissatisfied column
# with the most common value that populates the Series, 
# recurring to the fillna() method:
combined_updated['dissatisfied'] = combined_updated[
    'dissatisfied'
].fillna(combined_updated['dissatisfied'
                         ].value_counts().idxmax()).copy()

combined_updated['dissatisfied'].value_counts(
dropna=False)


# In[70]:


#creating a pivot table from the aggregated col service_cat
#and with the values - mean - of the dissatisfied:
pivot_service_dissatisfied = combined_updated.pivot_table(
index=['service_cat'], values='dissatisfied')

#plotting that pivot table into a bar chart:
bar_chart = pivot_service_dissatisfied.plot(
kind='barh', 
    title='Dissatisfied percentage by Service Category',
legend=False, xlim=(0,.7))

for key,spine in bar_chart.spines.items():
    spine.set_visible(False)
    
bar_chart.tick_params(top='off', bottom='off', right='off')

bar_chart.axvline(x=combined_updated[
    'dissatisfied'].mean(),color='grey', alpha=.3)

plt.show()


# #### The two main categories were there are more dissatisfied employees are among the ones with more years spent in the company: *Established* and *Veteran*.
# #### These two categories present mean values far more off than the overall mean. With huge gaps to the other two categories, *New* and *Experienced*.
# #### The *New* category stands out itself as the one with a less dissatisfied level, well bellow the overall avg. 
