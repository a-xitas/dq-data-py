#!/usr/bin/env python
# coding: utf-8

# # Analyzing the Gender Gap across several college degrees

# In[1]:


get_ipython().magic('matplotlib inline')
import pandas as pd
import matplotlib.pyplot as plt

women_degrees = pd.read_csv('percent-bachelors-degrees-women-usa.csv')
cb_dark_blue = (0/255,107/255,164/255)
cb_orange = (255/255, 128/255, 14/255)

stem_cats = ['Engineering', 'Computer Science', 'Psychology', 'Biology', 
             'Physical Sciences', 'Math and Statistics']

fig = plt.figure(figsize=(18, 3))

for sp in range(0,6):
    ax = fig.add_subplot(1,6,sp+1)
    ax.plot(women_degrees['Year'], women_degrees[stem_cats[sp]], c=cb_dark_blue, label='Women', linewidth=3)
    ax.plot(women_degrees['Year'], 100-women_degrees[stem_cats[sp]], c=cb_orange, label='Men', linewidth=3)
    for key,spine in ax.spines.items():
        spine.set_visible(False)
    ax.set_xlim(1968, 2011)
    ax.set_ylim(0,100)
    ax.set_title(stem_cats[sp])
    ax.tick_params(bottom="off", top="off", left="off", right="off")
    if sp == 0:
        ax.text(2005, 87, 'Men')
        ax.text(2002, 8, 'Women')
    elif sp== 5:
        ax.text(2005, 62, 'Men')
        ax.text(2001, 35, 'Women')
    
   


# In[15]:


cb_dark_blue = (0/255,107/255,164/255)
cb_orange = (255/255, 128/255, 14/255)

stem_cats = ['Psychology', 'Biology', 'Math and Statistics', 
             'Physical Sciences', 'Computer Science', 'Engineering']

lib_arts_cats = ['Foreign Languages', 'English', 'Communications and Journalism', 
                 'Art and Performance', 'Social Sciences and History']

other_cats = ['Health Professions', 'Public Administration', 'Education', 
              'Agriculture','Business', 'Architecture']

fig = plt.figure(figsize=(15, 17))

for i in range(0,17, 3):
    ax = fig.add_subplot(6,3,i+1)
    index_stem = int(i/3)
    ax.plot(women_degrees['Year'], women_degrees[stem_cats[index_stem]], 
            c=cb_dark_blue, label='Women', linewidth=3)
    ax.plot(women_degrees['Year'], 100-women_degrees[stem_cats[index_stem]], 
            c=cb_orange, label='Men', linewidth=3)
    for key,spine in ax.spines.items():
        spine.set_visible(False)
    ax.set_xlim(1968, 2011)
    ax.set_ylim(0,100)    
    ax.set_title(stem_cats[index_stem])
    ax.tick_params(bottom="off", top="off", left="off", right="off",
                  )
    if i == 0:
        ax.text(2005, 80, 'Men')
        ax.text(2002, 8, 'Women')        
    elif i == 15:
        ax.text(2005, 62, 'Men')
        ax.text(2001, 35, 'Women')
        

for i in range (1,16, 3):
    ax = fig.add_subplot(6,3,i+1)
    lib_arts_index = int((i-1)/3)
    ax.plot(women_degrees['Year'], women_degrees[lib_arts_cats[lib_arts_index]], 
            c=cb_dark_blue, linewidth=3, label='Women')
    ax.plot(women_degrees['Year'], 100-women_degrees[lib_arts_cats[lib_arts_index]],
           c=cb_orange, linewidth=3, label='Men')
    ax.set_xlim(1968,2011)
    ax.set_ylim(0,100)    
    ax.set_title(lib_arts_cats[lib_arts_index])
    ax.tick_params(right='off', left='off', bottom='off', top='off',
                  )
    if i == 1:
        ax.text(2005, 75, 'Women')
        ax.text(2002, 20, 'Men')
    elif i == 13:
        ax.text(2005, 60, 'Men')
        ax.text(2002, 35, 'Women')        
    for key,spine in ax.spines.items():
        spine.set_visible(False)

for i in range(3, 19, 3):
    ax = fig.add_subplot(6,3,i)
    other_cats_index = int(((i)/3)-1)
    ax.plot(women_degrees['Year'], women_degrees[other_cats[other_cats_index]],
           c=cb_dark_blue, linewidth=3, label='Women')
    ax.plot(women_degrees['Year'], 100-women_degrees[other_cats[other_cats_index]],
           c=cb_orange, linewidth=3, label='Men')
    ax.set_xlim(1968,2011)
    ax.set_ylim(0,100)    
    ax.set_title(other_cats[other_cats_index])
    ax.tick_params(bottom='off', top='off', right='off', left='off',
                  )
    if i == 3:
        ax.text(2005, 90, 'Women')
        ax.text(2002, 5, 'Men')
    elif i == 18:
        ax.text(2005, 60, 'Men')
        ax.text(2002, 30, 'Women')        
    for key,spine in ax.spines.items():
        spine.set_visible(False)


# #### Removing the x-axis labels from all the plots except for the bottommost ones, resorting to the labelbottom parameter in the ax.tick_params() method, avoiding overlaps between them and the titles of the different plots:

# In[13]:


cb_dark_blue = (0/255,107/255,164/255)
cb_orange = (255/255, 128/255, 14/255)

stem_cats = ['Psychology', 'Biology', 'Math and Statistics', 
             'Physical Sciences', 'Computer Science', 'Engineering']

lib_arts_cats = ['Foreign Languages', 'English', 'Communications and Journalism', 
                 'Art and Performance', 'Social Sciences and History']

other_cats = ['Health Professions', 'Public Administration', 'Education', 
              'Agriculture','Business', 'Architecture']

fig = plt.figure(figsize=(15, 17))

for i in range(0,17, 3):
    ax = fig.add_subplot(6,3,i+1)
    index_stem = int(i/3)
    ax.plot(women_degrees['Year'], women_degrees[stem_cats[index_stem]], 
            c=cb_dark_blue, label='Women', linewidth=3)
    ax.plot(women_degrees['Year'], 100-women_degrees[stem_cats[index_stem]], 
            c=cb_orange, label='Men', linewidth=3)
    for key,spine in ax.spines.items():
        spine.set_visible(False)
    ax.set_xlim(1968, 2011)
    ax.set_ylim(0,100)    
    ax.set_title(stem_cats[index_stem])
    ax.tick_params(bottom="off", top="off", left="off", right="off",
                  labelbottom='off')
    if i == 0:
        ax.text(2005, 80, 'Men')
        ax.text(2002, 8, 'Women')        
    elif i == 15:
        ax.text(2005, 62, 'Men')
        ax.text(2001, 35, 'Women')
        ax.tick_params(labelbottom='on')

for i in range (1,16, 3):
    ax = fig.add_subplot(6,3,i+1)
    lib_arts_index = int((i-1)/3)
    ax.plot(women_degrees['Year'], women_degrees[lib_arts_cats[lib_arts_index]], 
            c=cb_dark_blue, linewidth=3, label='Women')
    ax.plot(women_degrees['Year'], 100-women_degrees[lib_arts_cats[lib_arts_index]],
           c=cb_orange, linewidth=3, label='Men')
    ax.set_xlim(1968,2011)
    ax.set_ylim(0,100)    
    ax.set_title(lib_arts_cats[lib_arts_index])
    ax.tick_params(right='off', left='off', bottom='off', top='off',
                  labelbottom='off')
    if i == 1:
        ax.text(2005, 75, 'Women')
        ax.text(2002, 20, 'Men')
    elif i == 13:
        ax.text(2005, 60, 'Men')
        ax.text(2002, 35, 'Women')
        ax.tick_params(labelbottom='on')
    for key,spine in ax.spines.items():
        spine.set_visible(False)

for i in range(3, 19, 3):
    ax = fig.add_subplot(6,3,i)
    other_cats_index = int(((i)/3)-1)
    ax.plot(women_degrees['Year'], women_degrees[other_cats[other_cats_index]],
           c=cb_dark_blue, linewidth=3, label='Women')
    ax.plot(women_degrees['Year'], 100-women_degrees[other_cats[other_cats_index]],
           c=cb_orange, linewidth=3, label='Men')
    ax.set_xlim(1968,2011)
    ax.set_ylim(0,100)    
    ax.set_title(other_cats[other_cats_index])
    ax.tick_params(bottom='off', top='off', right='off', left='off',
                  labelbottom='off')
    if i == 3:
        ax.text(2005, 90, 'Women')
        ax.text(2002, 5, 'Men')
    elif i == 18:
        ax.text(2005, 60, 'Men')
        ax.text(2002, 30, 'Women')
        ax.tick_params(labelbottom='on')
    for key,spine in ax.spines.items():
        spine.set_visible(False)


# #### In order do reduce even more the cluttering we will simplify the y-axis labels and reduce them to two, 0 and 100. Using the method ax.set_yticks().

# In[6]:


cb_dark_blue = (0/255,107/255,164/255)
cb_orange = (255/255, 128/255, 14/255)

stem_cats = ['Psychology', 'Biology', 'Math and Statistics', 
             'Physical Sciences', 'Computer Science', 'Engineering']

lib_arts_cats = ['Foreign Languages', 'English', 'Communications and Journalism', 
                 'Art and Performance', 'Social Sciences and History']

other_cats = ['Health Professions', 'Public Administration', 'Education', 
              'Agriculture','Business', 'Architecture']

fig = plt.figure(figsize=(15, 17))

for i in range(0,17, 3):
    ax = fig.add_subplot(6,3,i+1)
    index_stem = int(i/3)
    ax.plot(women_degrees['Year'], women_degrees[stem_cats[index_stem]], 
            c=cb_dark_blue, label='Women', linewidth=3)
    ax.plot(women_degrees['Year'], 100-women_degrees[stem_cats[index_stem]], 
            c=cb_orange, label='Men', linewidth=3)
    for key,spine in ax.spines.items():
        spine.set_visible(False)
    ax.set_xlim(1968, 2011)
    ax.set_ylim(0,100)
    ax.set_yticks([0,100])
    ax.set_title(stem_cats[index_stem])
    ax.tick_params(bottom="off", top="off", left="off", right="off",
                  labelbottom='off')
    if i == 0:
        ax.text(2005, 80, 'Men')
        ax.text(2002, 8, 'Women')        
    elif i == 15:
        ax.text(2005, 62, 'Men')
        ax.text(2001, 35, 'Women')
        ax.tick_params(labelbottom='on')

for i in range (1,16, 3):
    ax = fig.add_subplot(6,3,i+1)
    lib_arts_index = int((i-1)/3)
    ax.plot(women_degrees['Year'], women_degrees[lib_arts_cats[lib_arts_index]], 
            c=cb_dark_blue, linewidth=3, label='Women')
    ax.plot(women_degrees['Year'], 100-women_degrees[lib_arts_cats[lib_arts_index]],
           c=cb_orange, linewidth=3, label='Men')
    ax.set_xlim(1968,2011)
    ax.set_ylim(0,100)
    ax.set_yticks([0,100])
    ax.set_title(lib_arts_cats[lib_arts_index])
    ax.tick_params(right='off', left='off', bottom='off', top='off',
                  labelbottom='off')
    if i == 1:
        ax.text(2005, 75, 'Women')
        ax.text(2002, 20, 'Men')
    elif i == 13:
        ax.text(2005, 60, 'Men')
        ax.text(2002, 35, 'Women')
        ax.tick_params(labelbottom='on')
    for key,spine in ax.spines.items():
        spine.set_visible(False)

for i in range(3, 19, 3):
    ax = fig.add_subplot(6,3,i)
    other_cats_index = int(((i)/3)-1)
    ax.plot(women_degrees['Year'], women_degrees[other_cats[other_cats_index]],
           c=cb_dark_blue, linewidth=3, label='Women')
    ax.plot(women_degrees['Year'], 100-women_degrees[other_cats[other_cats_index]],
           c=cb_orange, linewidth=3, label='Men')
    ax.set_xlim(1968,2011)
    ax.set_ylim(0,100)
    ax.set_yticks([0,100])
    ax.set_title(other_cats[other_cats_index])
    ax.tick_params(bottom='off', top='off', right='off', left='off',
                  labelbottom='off')
    if i == 3:
        ax.text(2005, 90, 'Women')
        ax.text(2002, 5, 'Men')
    elif i == 18:
        ax.text(2005, 60, 'Men')
        ax.text(2002, 30, 'Women')
        ax.tick_params(labelbottom='on')
    for key,spine in ax.spines.items():
        spine.set_visible(False)
    
    


# #### While the clutter was significantly reduced, we now have a problem: knowing which degrees have close to 50-50 gender breakdown!
# #### We will resort to the ax.axhline() method to draw an horizontal line in all our plots to 'cut' them in half (50). Using another color blind, grey, and giving it some transparancy level, using the alpha method!

# In[19]:


cb_dark_blue = (0/255,107/255,164/255)
cb_orange = (255/255, 128/255, 14/255)
cb_grey = (171/255, 171/255, 171/255)

stem_cats = ['Psychology', 'Biology', 'Math and Statistics', 
             'Physical Sciences', 'Computer Science', 'Engineering']

lib_arts_cats = ['Foreign Languages', 'English', 'Communications and Journalism', 
                 'Art and Performance', 'Social Sciences and History']

other_cats = ['Health Professions', 'Public Administration', 'Education', 
              'Agriculture','Business', 'Architecture']

fig = plt.figure(figsize=(15, 17))

for i in range(0,17, 3):
    ax = fig.add_subplot(6,3,i+1)
    index_stem = int(i/3)
    ax.plot(women_degrees['Year'], women_degrees[stem_cats[index_stem]], 
            c=cb_dark_blue, label='Women', linewidth=3)
    ax.plot(women_degrees['Year'], 100-women_degrees[stem_cats[index_stem]], 
            c=cb_orange, label='Men', linewidth=3)
    for key,spine in ax.spines.items():
        spine.set_visible(False)
    ax.set_xlim(1968, 2011)
    ax.set_ylim(0,100)
    ax.set_yticks([0,100])
    ax.set_title(stem_cats[index_stem])
    ax.tick_params(bottom="off", top="off", left="off", right="off",
                  labelbottom='off')
    ax.axhline(y=50, color=cb_grey, alpha=0.3)
    if i == 0:
        ax.text(2005, 80, 'Men')
        ax.text(2002, 8, 'Women')        
    elif i == 15:
        ax.text(2005, 62, 'Men')
        ax.text(2001, 35, 'Women')
        ax.tick_params(labelbottom='on')

for i in range (1,16, 3):
    ax = fig.add_subplot(6,3,i+1)
    lib_arts_index = int((i-1)/3)
    ax.plot(women_degrees['Year'], women_degrees[lib_arts_cats[lib_arts_index]], 
            c=cb_dark_blue, linewidth=3, label='Women')
    ax.plot(women_degrees['Year'], 100-women_degrees[lib_arts_cats[lib_arts_index]],
           c=cb_orange, linewidth=3, label='Men')
    ax.set_xlim(1968,2011)
    ax.set_ylim(0,100)
    ax.set_yticks([0,100])
    ax.set_title(lib_arts_cats[lib_arts_index])
    ax.tick_params(right='off', left='off', bottom='off', top='off',
                  labelbottom='off')
    ax.axhline(y=50, color=cb_grey, alpha=0.3)
    if i == 1:
        ax.text(2005, 75, 'Women')
        ax.text(2002, 20, 'Men')
    elif i == 13:
        ax.text(2005, 60, 'Men')
        ax.text(2002, 35, 'Women')
        ax.tick_params(labelbottom='on')
    for key,spine in ax.spines.items():
        spine.set_visible(False)

for i in range(3, 19, 3):
    ax = fig.add_subplot(6,3,i)
    other_cats_index = int(((i)/3)-1)
    ax.plot(women_degrees['Year'], women_degrees[other_cats[other_cats_index]],
           c=cb_dark_blue, linewidth=3, label='Women')
    ax.plot(women_degrees['Year'], 100-women_degrees[other_cats[other_cats_index]],
           c=cb_orange, linewidth=3, label='Men')
    ax.set_xlim(1968,2011)
    ax.set_ylim(0,100)
    ax.set_yticks([0,100])
    ax.set_title(other_cats[other_cats_index])
    ax.tick_params(bottom='off', top='off', right='off', left='off',
                  labelbottom='off')
    ax.axhline(y=50, color=cb_grey, alpha=0.3)
    if i == 3:
        ax.text(2005, 90, 'Women')
        ax.text(2002, 5, 'Men')
    elif i == 18:
        ax.text(2005, 60, 'Men')
        ax.text(2002, 30, 'Women')
        ax.tick_params(labelbottom='on')
    for key,spine in ax.spines.items():
        spine.set_visible(False)

plt.savefig('gender_degrees.png')


# In[ ]:




