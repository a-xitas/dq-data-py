#!/usr/bin/env python
# coding: utf-8

# # Star Wars Surveys Analysis

# ## === Exordium ===
# #### - In the following analysis we will be working with a Dataset about some questions compiled by the team at FiveThirtyEight, and address to the American Star Wars fan base.
# #### - The purpose of the team with this surveys was to answer some questions such as: was the Episode V - The Empire Strikes Back, the favourite movie from the fans? If not which was? What were their favourite characters? Does Education levels from the side of the fans, present themselves as a differentiator in the rating of the 6 Star Wars movies from the saga?  Do we see differences in the fan base tastes when we segment the data in terms of Gender.  And what was the most seen movie of all?
# #### - Because the Dataset had some dirty datapoints and some of the data was inserted in a columns dependency level we will need, prior to do the analysis, to do some cleaning. So first we will put our hands in the dough by cleaning what needs to be cleaned from the Dataset, and then we will do our analysis by resorting to some plots in order to better grasp the full potential of the data and to try to unlock some of its questions.

# ## Cleaning the Dataset - Episode 1

# In[1]:


import pandas as pd
import numpy as np

# Reading into a Dataframe the Star Wars Dataset:
star_wars = pd.read_csv('star_wars.csv', encoding='ISO-8859-1')
star_wars.head()


# In[2]:


# Extracting and checking the Dataset columns:
star_wars.columns


# In[3]:


# Removing all the NaN rows in the RespondentID col of our Dataset, using
# the notna() method:
star_wars = star_wars[star_wars['RespondentID'].notna()].copy()
# Validating the operation:
star_wars['RespondentID'].isnull().value_counts()


# In[4]:


# Converting the Yes's and No's in the 'Have you seen any of the 6 films 
# in the Star Wars franchise?' col, to True's and False's. Transforming that
# way the entire col from a string type to a Boolean type:
star_wars[
    'Have you seen any of the 6 films in the Star Wars franchise?'
        ] = star_wars[
    'Have you seen any of the 6 films in the Star Wars franchise?'
        ].map({'Yes': True, 'No': False}).copy()

# Checking the results:
star_wars['Have you seen any of the 6 films in the Star Wars franchise?'].value_counts(
dropna=False)


# In[36]:


# Converting the Yes's and No's in the 'Do you consider yourself to be a 
# fan of the Star Wars film franchise?' col, to True's and False's. 
# Transforming that way the entire col from a string type to a Boolean type:

star_wars[
    'Do you consider yourself to be a fan of the Star Wars film franchise?'
        ] = star_wars[
    'Do you consider yourself to be a fan of the Star Wars film franchise?'
        ].map({'Yes': True, 'No': False})
# Veifying the changes:
star_wars[
    'Do you consider yourself to be a fan of the Star Wars film franchise?'
].value_counts(dropna=False)


# In[6]:


# Renaming all the cols that correspond to the movies seen by the Star Wars
# fans from Unnamed to seen, adding to it a numeric value that corresponds
# to each of the 6 Episodes from the saga. E.g., seen_Ep.1 == seen Episode I,
# seen_Ep.4 == seen Episode IV, seen_Ep.6 == seen Episode VI, etc:
star_wars = star_wars.rename(columns={
                'Which of the following Star Wars films have you seen? Please select all that apply.': 'seen_Ep.1',
                'Unnamed: 4': 'seen_Ep.2',
                'Unnamed: 5': 'seen_Ep.3',
                'Unnamed: 6': 'seen_Ep.4',
                'Unnamed: 7': 'seen_Ep.5',
                'Unnamed: 8': 'seen_Ep.6'
                                    }).copy()
# Changing the content of the cols. Passing from a str to a boolean type.
# First we will creat a list of all the names of the movies that populate
# our seen cols. Than, resorting to a for loop, we will change the format 
# of that very same columns. Attributing the ones with the name of the movie
# a True boolean and assuming that the ones that have null values correspond
# to False answers related to whether or not the fans have seen that 
# particular movie: 
movies = [
    'Star Wars: Episode I  The Phantom Menace', 
    'Star Wars: Episode II  Attack of the Clones',
    'Star Wars: Episode III  Revenge of the Sith',
    'Star Wars: Episode IV  A New Hope',
    'Star Wars: Episode V The Empire Strikes Back',
    'Star Wars: Episode VI Return of the Jedi'    
]
for n in np.arange(6):
    col = 'seen_Ep.{}'.format(n+1)
    star_wars[col] = star_wars[col].map({
    movies[n]: True, np.NaN: False})
    
# Checking and validating the previous changes in the Dataset:
for n in np.arange(6):
    col = 'seen_Ep.{}'.format(n+1)
    print(star_wars[col].value_counts().sum() == star_wars.shape[0])
    print(star_wars[col].value_counts())


# In[7]:


# Converting the Star Wars movies rating on preference cols from str-float:
star_wars[star_wars.columns[3:15]] = star_wars[
                            star_wars.columns[3:15]].astype(float).copy()
# Checking the outcome of the operation:
print(star_wars[star_wars.columns[9:15]].dtypes)


# In[8]:


# Renaming those very same cols to a more descriptive name,
# resorting to the rename() method from pandas:
star_wars = star_wars.rename(columns={
    'Please rank the Star Wars films in order of preference with 1 being your favorite film in the franchise and 6 being your least favorite film.': 'ranking_Ep.1',
    'Unnamed: 10': 'ranking_Ep.2',
    'Unnamed: 11': 'ranking_Ep.3',
    'Unnamed: 12': 'ranking_Ep.4',
    'Unnamed: 13': 'ranking_Ep.5',
    'Unnamed: 14': 'ranking_Ep.6'}).copy()

# Verifying the changes:
print(star_wars.columns[9:15])


# ## Analyzing the Dataset Episode 1

# In[9]:


import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')

# Calculating the mean of all the 5 ranking cols.
# The values range from 1-6. Being 1 the most favorite and 
# 6 the least favorite movie. So the ones that have a higher 
# ranking value are the least favorite movies from the
# Star Wars saga, and vice-versa:
ranking_means = star_wars[
    star_wars.columns[9:15]].mean().sort_values(
ascending=False)

ranking_means.head()

# Plotting those means in a bar graph:
rank_graph = ranking_means.plot.barh(
    edgecolor='none',
color= [(255/255,188/255,121/255),
       (162/255,200/255, 236/255),
       (207/255,207/255,207/255),
       (200/255,82/255,0/255),
       (255/255,194/255,10/255),
       (212/255,17/255,89/255)])

# ENHANCING PLOT AESTHETICS: 

# Removing all the 4 spines with a for loop from our graph figure:
for key, spine in rank_graph.spines.items():
    spine.set_visible(False)
# Removing the ticks:    
rank_graph.tick_params(
    bottom='off', top='off', left='off', right='off')
# Setting a graph title:
rank_graph.set_title('Average Star Wars Movies Ranking')
# Setting an average graph line:
rank_graph.axvline(ranking_means.mean(), 
                   alpha=.8, linestyle='--', color='grey')
# Displaying the graph:
plt.show()


# In[10]:


# Analysing the Age column from our Dataset:
star_wars['Age'].value_counts().sort_values()


# ### Findings:
# 
# #### - Interestingly enough the 3 movies from the saga that enter the top 3 rank for the Star Wars fans are the very first 3 ones to be realeased: Star Wars Episode V - The Empire Srikes Back; Star Wars Episode VI - Return of the Jedi; Star Wars Episode IV, in order of choice.
# #### - Another funny fact is that these very same 3 Episodes rank, in the Internet Movie Database website (IMDb), much higher than the other 3 ones, the 'new' movies from the saga: 8,7;  8,3 and 8,6 out of 10. Against 6,5; 6,5 and 7,5, for the Episodes I; II and III, respectively. 
# #### - We can conclude that the choices from the fans on this survey are vey much aligned with the ranking of the Star Wars saga in biggest movies database over the Internet.
# #### - Last but not least, when we dig a little bit deeper, we find that the age range from the biggest portion of the respondents of the survey is from around 30's onwards. This might explain the lean to the oldest movies from the Star Wars saga. Being these movies the ones from their teen age or young adult age, the ones that most influence and impact caused on them and their future lifes. 

# In[11]:


# Indexing, calculating and sorting the data that corresponds to the six
# different movies seen by the fans:
star_wars_seen_total = star_wars[star_wars.columns[3:9]].sum().copy().sort_values(
ascending=False)

# Plotting a bar graph of the total of movies seen per Episode of the Star
# Wars saga:
star_wars_seen_total_graph = star_wars_seen_total.plot.bar(
    edgecolor='none',
    color=[(12/255,123/255,220/255),
           (93/255,58/255,155/255),
           (254/255,254/255,98/255),
           (211/255,95/255,183/255),
           (212/255,17/255,89/255),
           (64/255,176/255,166/255)])
# Setting an average graph line:
star_wars_seen_total_graph.axhline(
    star_wars_seen_total.mean(),
color='grey', alpha=.8, linestyle=':')


# ENHANCING PLOT AESTHETICS: 

# Removing the ticks:
star_wars_seen_total_graph.tick_params(
bottom='off', top='off', left='off', right='off')
# Removing all the 4 spines with a for loop from our graph figure:
for key, spine in star_wars_seen_total_graph.spines.items():
    spine.set_visible(False)
    
# Setting a graph title:    
star_wars_seen_total_graph.set_title('Most seen Episode movie')
# Rotating the xtick labels:
plt.xticks(rotation='horizontal')
# Displaying the graph:  
plt.show()


# ### Findings:
# 
# #### - The result is in line with the previous conclusions. Two out of the three most voted movies from the Star Wars fans, are also the most seen ones: Episode V and Episode VI with more than 700 respondents having seen them. In between these 2 and the other most favorite movie from the saga, the Episode IV, stands Episode I with views that puts it above the average, roughly around 680. 
# #### - The explanations for this meddling might be two: marketing and time. On one hand, beeing the movie Star Wars Episode IV the very first one to be realeased the expectations from 20th Century Fox weren't that high, so they didn't back the movie enough prior to their release. Not betting that much in marketing and even in theatrical run, being it initialy only released to a limited number. The success of the movie was far more due to it's screenplay/innovative special effects/actors/producer quality - its core content, than to the support of its Studio. The other explanations that placed the Episode I -  The Phantom Menace as the third most seen movie from all the saga were time, and marketing. Marketing that, for example the first movie didn't have, this had in double or more. Now being highly backed both from Lucas Arts and 20th Century Fox. 20th Century Fox knew now the kind of cash cow this was. And the time it took them to release this movie from their last one, Star Wars Episode VI - Return of the Jedi, more than 15 years, led all the fans to such an impatious level, that only grew more and more as years were passing. Creating the perfect momentum for the launch of the movie, and therefore a massive influx to the theaters. 

# ### Analyzing the Dataset in a Gender perspective 

# In[12]:


# Dividing our Dataset into two new ones. One for Female respondents and 
# another one for Male ones:

female = star_wars[star_wars['Gender'] == 'Female'].copy()
male = star_wars[star_wars['Gender'] == 'Male'].copy()
# Displaying the first 5 rows of the female Dataset:
female.head()


# In[13]:


# Redoing the same two previous analyses, and plotting two graph bars for
# the most ranked Star Wars movies and the most seen ones from all the saga.
# Ladies first.

# Indexing, calculating and sorting the data that corresponds to the 
# Female gender:
ranking_means_female = female[
    female.columns[9:15]].mean().sort_values(
ascending=False)

ranking_means_female.head()

# Plotting those means in a bar graph:
rank_graph_female = ranking_means_female.plot.barh(
    edgecolor='none',
    color= [(255/255,188/255,121/255),
           (162/255,200/255, 236/255),
           (207/255,207/255,207/255),
           (200/255,82/255,0/255),
           (255/255,194/255,10/255),
           (212/255,17/255,89/255)])

# ENHANCING PLOT AESTHETICS:

# Removing all the 4 spines with a for loop from our graph figure:
for key, spine in rank_graph_female.spines.items():
    spine.set_visible(False)
# Removing the ticks:    
rank_graph_female.tick_params(
    bottom='off', top='off', left='off', right='off')
# Setting a graph title:
rank_graph_female.set_title('Average Star Wars Movies Ranking (Female_Respondents)')
# Setting an average graph line:
rank_graph_female.axvline(ranking_means_female.mean(), 
                   alpha=.8, linestyle='--', color='grey')
# Displaying the graph:
plt.show()


# In[14]:


# Doing the same process as previous only this time for the male Gender.

# Indexing, calculating and sorting the data that corresponds to the 
# Male Gender:
ranking_means_male = male[
    male.columns[9:15]].mean().sort_values(
ascending=False)

ranking_means_male.head()

# Plotting those means in a bar graph:
rank_graph_male = ranking_means_male.plot.barh(
    edgecolor='none',
    color= [(255/255,188/255,121/255),
            (162/255,200/255, 236/255),
            (207/255,207/255,207/255),
            (200/255,82/255,0/255),
            (255/255,193/255,7/255),
            (216/255,27/255,96/255)])

# ENHANCING PLOT AESTHETICS:

# Removing all the 4 spines with a for loop from our graph figure:
for key, spine in rank_graph_male.spines.items():
    spine.set_visible(False)
# Removing the ticks:    
rank_graph_male.tick_params(
    bottom='off', top='off', left='off', right='off')
# Setting a graph title:
rank_graph_male.set_title('Average Star Wars Movies Ranking (Male_Respondents)')
# Setting an average graph line:
rank_graph_male.axvline(ranking_means_male.mean(), 
                   alpha=.8, linestyle='--', color='grey')
# Displaying the graph:
plt.show()


# In[15]:


# Now lets deal with the number of views per movie, for all the six Episodes
# of the Star Wars saga that the Female Gender as seen.
# As usual, ladies first.

# Indexing, calculating and sorting the data that corresponds to the 
# Female Gender:
female_seen_total = female[female.columns[3:9]].sum().copy().sort_values(
ascending=False)
# Plotting a bar graph of the Female_seen_total Dataset: 
female_seen_total_graph = female_seen_total.plot.bar(
    edgecolor='none',
    color=[(12/255,123/255,220/255),
           (93/255,58/255,155/255),
           (254/255,254/255,98/255),
           (211/255,95/255,183/255),
           (212/255,17/255,89/255),
           (64/255,176/255,166/255)])

# ENHANCING PLOT AESTHETICS: 

# Setting an average graph line:
female_seen_total_graph.axhline(
    female_seen_total.mean(),
color='grey', alpha=.8, linestyle=':')
# Turning off all the ticks:
female_seen_total_graph.tick_params(
bottom='off', top='off', left='off', right='off')
# Cleaning out all the spines from our graph figure:
for key, spine in female_seen_total_graph.spines.items():
    spine.set_visible(False)    
# Setting a graph title:    
female_seen_total_graph.set_title('Star Wars most seen Episodes (Female_Respondents)')
# Rotating the xtick labels:
plt.xticks(rotation='horizontal')
# Displaying the graph:    
plt.show()


# In[16]:


# Doing the same process as previous only this time for the male Gender.

# Indexing, calculating and sorting the data that corresponds to the 
# Male Gender:
male_seen_total = male[male.columns[3:9]].sum().copy().sort_values(
ascending=False)
# Plotting a bar graph of the male_seen_total Dataset:
male_seen_total_graph = male_seen_total.plot.bar(
    edgecolor='none',
    color=[(12/255,123/255,220/255),
           (93/255,58/255,155/255),
           (254/255,254/255,98/255),
           (211/255,95/255,183/255),
           (212/255,17/255,89/255),
           (64/255,176/255,166/255)])

# ENHANCING PLOT AESTHETICS:

# Setting an average graph line:
male_seen_total_graph.axhline(
    male_seen_total.mean(),
color='grey', alpha=.8, linestyle=':')
# Turning off all the ticks:
male_seen_total_graph.tick_params(
bottom='off', top='off', left='off', right='off')
# Cleaning out all the spines from our graph figure:
for key, spine in male_seen_total_graph.spines.items():
    spine.set_visible(False)
# Setting a graph title:    
male_seen_total_graph.set_title('Star Wars most seen Episodes (Male_Respondents)')
# Rotating the xtick labels:
plt.xticks(rotation='horizontal')
# Displaying the graph:    
plt.show()


# ### Findings:
# 
# #### - Interesting discoveries. If on the Total number of Movies seen both genders present similar results over all the six movies from the saga, the same can't be said on the way the two genders ranked the movies.
# #### - The ranking gap between the 'old' three movies and the 'new' ones is much more pronounced in the Male respondents rather than in the Female ones. The Female fans even ranked the the Star Wars Episode I -  The Phantom Menace at number 3, relegating to fourth the Episode IV. For the Male fans this Episode was their second choice for best Star Wars movie from all the six.
# #### - Does this means that men are more into sci-fi movies per own initative rather than women that need a 'push' from all the marketing machine, or does it means that women were awakening late to the uniqueness of the Star Wars saga? 

# ### Analyzing the Dataset and the respondents ranking answers related to their degree of Education

# In[17]:


# Figuring out how many Education levels there are in the Dataset:
star_wars['Education'].value_counts(dropna=False)


# In[18]:


# Creating our pivot table based on those 5 levels of Education:
education_pivot = star_wars.pivot_table(
    index='Education',
    values=['ranking_Ep.1', 
            'ranking_Ep.2', 
            'ranking_Ep.3', 
            'ranking_Ep.4', 
            'ranking_Ep.5',
            'ranking_Ep.6'],
    aggfunc='mean',
    dropna=True
    )

# Reseting the Dataframe (DF) index and turning Education as a label:
education_pivot = education_pivot.reset_index().copy()
# Displaying the first five rows of our newly created education_pivot DF:
education_pivot.head()


# In[29]:


# Plotting 6 pie charts, one for each movie,of the rankings segmented by the 
# Star Wars fans Education levels.These levels are divided into 5 categories:
# Bachelor degree (B); Graduate degree (G); High school degree (HS);
# Less than high school degree (<HS); Some College or Associate degree (CAD):

# Plotting 6 pie graphs of the education_pivot Dataset:
edu = education_pivot[[
                      'ranking_Ep.1',
                      'ranking_Ep.2',
                      'ranking_Ep.3',
                      'ranking_Ep.4',
                      'ranking_Ep.5',
                      'ranking_Ep.6']].plot.pie(subplots=True,
                                            figsize=(18, 3),
                                            legend=False,
                                            labels=[
                                            'B',
                                            'G',
                                            'HS',
                                            '<HS',
                                            'CAD'
                                            ],
                                            colors=[(100/255,143/255,255/255),
                                                  (120/255,95/255,240/255),
                                                   (220/255,38/255,127/255),
                                                   (254/255,97/255,0/255),
                                                   (255/255,176/255,0/255)])
# ENHANCING PLOT AESTHETICS: 

# Removing the edgecolor black from all the pie charts:
plt.rcParams['patch.edgecolor'] = 'white'
# Displaying the graph:
plt.show()


# ### Findings:
# 
# #### - There isn't, at a first glance, a very strong evidence that respondents belonging to one certain level of Education tend to choose some certain Episodes over others, from all the six movies of the Star Wars saga in analysis, ranking some group of movies much higher in detriment of others. 
# #### - The sample tends do be moreless homogeneous. If from one side we see fans with less than a High School degree giving a high ranking to The Star Wars Episode V. They than cut that score in the next movie of the saga, the Episode VI, and give a better ranking to the third movie, Star Wars Episode III - Revenge of the Sith. Moreless the same applies to the High School Degree fans. They tend to rank all the six movies moreless the same.
# #### - A slight trend is observable though for the Bachelor and Graduate groups. These two groups seem to give a slightly better rank to the 'old' movies (Episodes IV-VI) from the saga, compared to 'new' ones ((Episodes I-III).

# ## Cleaning the Dataset Episode 2
# #### The most and the least loved, and the more controversial characters from all the 6 Episodes

# In[20]:


# Returning the necessary cols for this specific analysis:
print(star_wars.columns[15:29])


# In[21]:


# Renaming all our cols that rate, according to the fans preferences, the
# characters from the first six Episodes of the Star Wars saga.
# Each column is being renamed after the correspondent character:
star_wars = star_wars.rename(columns={
'Please state whether you view the following characters favorably, unfavorably, or are unfamiliar with him/her.': 'Han Solo',
'Unnamed: 16': 'Luke Skywalker',
'Unnamed: 17': 'Princess Leia Organa',
'Unnamed: 18': 'Anakin Skywalker',
'Unnamed: 19': 'Obi Wan Kenobi',
'Unnamed: 20': 'Emperor Palpatine',
'Unnamed: 21': 'Darth Vader',
'Unnamed: 22': 'Lando Calrissian',
'Unnamed: 23': 'Boba Fett',
'Unnamed: 24': 'C-3P0',
'Unnamed: 25': 'R2 D2',
'Unnamed: 26': 'Jar Jar Binks',
'Unnamed: 27': 'Padme Amidala',
'Unnamed: 28': 'Yoda'}).copy()
                            
# Validating the previous changes:
star_wars.columns[15:29]


# In[22]:


# Checking, resorting to the value_counts() method, how many rating types
# there are to rank our characters:

star_wars['Luke Skywalker'].value_counts(dropna=False).sort_values()


# In[23]:


star_wars['Darth Vader'].value_counts(dropna=False).sort_values()


# In[24]:


star_wars['Yoda'].value_counts(dropna=False).sort_values()


# In[25]:


# In the few samples we previous analyzed we already check that the number 
# of Null values is very material in all of them.
# Let's check in all of our characters cols with the isna() method:
star_wars[star_wars.columns[15:29]].isna().sum()


# ### Findings:
# 
# #### - The number of Null values although being very significant, its very similar in terms of frequency, across all the characters. Ranging from 355-374. This might be to some shared missing values across all the Dataset or some shared errors in inputing the data. Either way, being the numbers very similiar across all the Dataset, opting for excluding all these Nulls for our analysis becomes much less violent per se. 

# In[26]:


# Droping all the nulls from our characters rating using the dropna method,
# and assigning the values to a new variable:
star_wars_characters_rating = star_wars[star_wars.columns[
    15:29]].dropna(axis=0).copy()
# Verifying the previous method:
star_wars_characters_rating.isna().sum()


# In[31]:


# Now thats combine the several types of answers that the respondents gave 
# into 4 major groups: Favorably; Unfavorably; Neutral; Unknown. we do this
# in order to facilitate and structure our analysis in biggers groups:
star_wars_characters_rating = star_wars_characters_rating.replace([
    'Somewhat unfavorably', 
    'Very unfavorably',
    'Somewhat favorably',
    'Very favorably',
    'Unfamiliar (N/A)', 
    'Neither favorably nor unfavorably (neutral)'], 
    ['Unfavorably',
     'Unfavorably',
     'Favorably',
     'Favorably',
     'Unknown',
     'Neutral']).copy()

# Shortening some cols names, thus improving their readability:
star_wars_characters_rating = star_wars_characters_rating.rename(columns={
    'Princess Leia Organa': 'Princess Leia',
    'Anakin Skywalker': 'Anakin'}).copy()
# Displaying the first five rows
star_wars_characters_rating.head()


# ## Analyzing the Dataset Episode 2
# #### The most and the least loved, and the more controversial characters from all the 6 Episodes
# 

# In[37]:


# Creating all our 4 Bars, based on the 4 major ratings each respondent
# gave to the main Star Wars characters, stacking them up accordingly to 
# that very same rating group, and distributing them along each of the main
# characters:
fig, ax = plt.subplots(figsize=(22,10))
characters = star_wars_characters_rating.columns.values
r = np.arange(len(characters))
bar_w = .85

# Calculating the percentages of the 4 major character rating groups:
Favorably = ((star_wars_characters_rating == 
    'Favorably').sum()/star_wars_characters_rating.shape[0]) * 100
Unfavorably = ((star_wars_characters_rating == 
        'Unfavorably').sum()/star_wars_characters_rating.shape[0]) * 100
Neutral = (star_wars_characters_rating ==
          'Neutral').sum()/star_wars_characters_rating.shape[0] * 100
Unknown = (star_wars_characters_rating == 
           'Unknown').sum()/star_wars_characters_rating.shape[0] * 100

# Plotting a stacked bar graph for each of the previous variables:
plt.bar(r, Favorably[r], color=(26/255,255/255,26/255), edgecolor='white', width = bar_w)
plt.bar(r, Neutral[r], bottom=Favorably[r], color=(254/255,254/255,98/255), edgecolor='white', width = bar_w)
plt.bar(r, Unknown[r], bottom=(Favorably[r]+ Neutral[r]), color=(195/255,186/255,164/255), edgecolor='white', width = bar_w)
plt.bar(r, Unfavorably[r], bottom=(Favorably[r]+ Neutral[r] + Unknown[r]), color=(254/255,58/255,0/255), edgecolor='white', width=bar_w)
plt.xticks(r+.35, characters)
plt.yticks(np.arange(20, 120, 20))

# ENHANCING PLOT AESTHETICS:

# Removing the ticks from the graph:
ax.tick_params(bottom='off',
              top='off',
              left='off',
              right='off')
# Removing the spines from our graph:
for key, spine in ax.spines.items():
    spine.set_visible(False)

# Setting up a legend box for our bar graph:    
plt.legend(
    loc='upper right', 
    labels=('Favorably', 'Neutral', 'Unknown', 'Unfavorably'), 
    ncol=1, fancybox=True, framealpha=.6)

# Displaying the graph:
plt.show()


# ### Findings:
# 
# #### - Not surprisingly the villain characters are seen as the least favourable of them all. In the opposite spectrum we have the so called heroes of the Star Wars saga. 
# #### - Characters like Luke Skywalker; Obi Wan Kenobi; Han Solo; Yoda and R2 D2 all top the first 5 choices of the fans. And Luke will forever remain in all of the fans hearts as the one and only number 1. 
# #### - The most unfavorable character of them all is, for surprise of many, or maybe not, Jar Jar Binks. I don' t think this is perceived as he beeing a villain, but rahter an empty shallow character. Very weak lines, forced appearances in the plot, like he would suddenly fall from the sky directly in the movie set. The only reasoning for me for him to have been in the movies was purely economics. Someone wanted to push their merchandising sales figures.
# #### - No surprises on the other most unfavorable characters of the saga. Maybe I would expect, and this is my personal opinion, the most unfavorable one, apart from Jar Jar Binks, to be Emperor Palpatine, and not Darth Vader. I would even rate him as one of the Good ones. Not only because of his master played role and his amazing and iconic character, but also because of his contribute to the light side of the force, especially in the last episode of the saga. 
# #### - Darth Vader, appart of being one of the least favourite characters, is also the most controversial one. If we take out of the equation the Unknown and the Neutral answers we end up with only the Favorably and the Unfavorably opinions of the fans. And taking these two antagonistic opinions no one beats Darth Vader in the bipolarization of the fans opinions. Hence my previous statement. You hate him or you love him, and fans opinions relatively to the character of Darth Vader are among the most divided ones. 
# #### - On the side of the Unknowns I have to confess, WHO IS BOBA FETT? I have to say that I had to do an herculean effort to go to my very far far away corners of my brain only to, after googling for it, find out I was wrong :D. Anyway, I think this choice from the survey promotors - FiveThirtyEight was not the happiest one. Why not, for example, Chewbacca or Jabba the Hutt?
# #### - The other mysterious personage, for the Star Wars fans surveyed, Lando Calrissian, I can only explain by a mix of old generation and lack of screenplay time?!
# 

# ## === Bottom Line ===
# #### After our analysis we can wrap and conclude the following:
#     1. Star Wars fans are well aware of the importance of the Episode 5 - The Empire Strikes Back movie. Not only was this the most seen 
#     movie as it was the one they ranked at number one from all the 6
#     Episodes of the saga;
#     
#     2. There's a collage of the most ranked movies of the saga by the 
#     fans, and their respective rating at IMDb. The opposite is also seen on the other side of the force;
#     
#     3. Bad boys will go to hell, and Good boys will top the preference
#     choices of the fans;
#     
#     4. Better to be a bad boy than a bad actor or a bad role. And Jar 
#     Jar Binks is a very good example of those two;
#     
#     5. Marketing expenditures with a pinch of growing anxiety creates 
#     the ideal recipe to bring massive flows of fans to the movie 
#     theaters. Well done 20th Century Fox, better late than never;
#     
#     6. The previous does not mean that you can apply the same recipe 
#     over and over to boost movie theaters ticket sales. A schmuck will
#     remain a schmuck no matter how well portrayed he is. Better luck 
#     next time 20th Century Fox. Maybe channelling more money into the 
#     movies per se, and improving their quality, instead of masking them with tons of marketing woudn't be such a bad idea;
#     
#     7. The IQ levels of the Star Wars fans doesn't play a significant 
#     role in their opinions and how they perceive the quality of the 
#     movies;
#     
#     8. What unease most of the trully Star Wars fans, now that all of 
#     the Star Wars sagas and future productions have been sold to the 
#     Mickey Mouse, Mulan or Maleficent: Mistress of Evil orchestrator, 
#     is: Will we ever again in our lifetime have another opportunity 
#     to contemplate a movie such as The Empire Strikes Back? 
#     
