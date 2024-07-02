#!/usr/bin/env python
# coding: utf-8

# # My first DQ project (on most used free apps)
# 
# **with this project I will try to gain a view on which free apps are most sought after in order to monetize the possibility to introduce adds on a free app we are trying to develop**

# - opening the Apple Dataset [link](https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps/home):

# In[1]:


from csv import reader
opened_file_A = open('AppleStore.csv', encoding="utf8")
read_file_A = reader(opened_file_A)
Apps_Ds = list(read_file_A)


# - opening the Google Play Dataset [link](https://www.kaggle.com/lava18/google-play-store-apps/home):

# In[2]:


opened_file_G =  open('googleplaystore.csv', encoding="utf8")
read_file_G = reader(opened_file_G)
Google_Ds = list(read_file_G)


# - creating a function to xplore the data:

# In[3]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]
    for row in dataset_slice:
        print(row)
        print('\n') #adds a new (empty) line
        
    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# In[4]:


print(Apps_Ds[0]) #printing the header of the Apple Dataset


# In[5]:


print(Google_Ds[0]) #printing the header of the Google Dataset


# **Now we will, before the analysis, have to do some data cleaning to our 2 Datasets. And remove duplicates or typos in the info, or info that really doesnt matter, like apps in other language other than English!**

# In[6]:


print(Google_Ds[10473])


# - the Google Dataset has an error in row 10473. Were the Category of the app doesnt appear, instead in its place we have the rating. We will have to delete this row:

# In[7]:


del Google_Ds[10473]


# - Scraping for Duplicate entries in our Dataset. Because As read in the Kaggle Discussion area, for the Google Play store Dataset, this Dataset as a number os duplicate entries on it. 
# - As example I will show some duplicates for the Instagram app:

# In[8]:


for column in Google_Ds:
    header = Google_Ds[0]
    name = column[0]
    if name == 'Instagram':
        print(header)
        print(column)
        print("\n")


# - Now we should and ought to count how many duplicate entries we have in this Dataset of Google Play Store. By Looping trough the entire Dataset and verifying if the variable *name*, that should correspond to the name of an app is already in the empty list we created for the unique_apps, and if it isn't to be part of that list, and once that very same app is encountered again, and is part of the unique_apps list, should then be part of the duplicate_apps list. We then simply return the total number of those duplicate entries, and also print some examples of them:

# In[9]:


duplicate_apps = []
unique_apps = []

for column in Google_Ds:
    name = column[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)
        
print('Nº of Duplicate Apps:', len(duplicate_apps))
print('\n')
print('Some examples of Duplicate Entries:', duplicate_apps[:10])


# - This Duplicate Entries won't be, obsviously, randomly deleted! I will use the info that's differentiating them from one another, the column *Reviews*, and assume that the ones that have the more *Reviews* are the ones that are more updated. Being therefore the ones that should stay in our Dataset and all the other duplicates deleted! 

# - We will start by first sorting and saving the apps that have the highst number of reviews.
# - First we will creat an empty dict with the name of *reviews_max*, where we will save the name of the app as a key, and the total number of reviews as the value of that unique key
# - Then we will loop through the Google_Ds and isolate the variable *name* which corresponds to the name of the app, and the variable *n_reviews* which corresponds to the nº of the reviews a certain app has.
# 
#     - Using an if Statement we will assess if the app already exists in the dict we created and if the key:value is inferior to the the biggest review it will have the biggest review as the new value for the key name app. If the app is not in the reviews_max dict it will had it to the dict under the form key(name):value(n_reviews)

# In[10]:


reviews_max  = {}

for column in Google_Ds[1:]:
    name = column[0]
    n_reviews = float(column[3])
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    elif name not in reviews_max:
        reviews_max[name] = n_reviews


#print(reviews_max)

print(len(reviews_max))
print(len(Google_Ds[1:]) - 1181)


# - We can check above that now we have the same number of unique apps in our *reviews_max* dict as we should have in our Google_Ds: 9659

# ## Now lets incorporate our unique entries into our Google_Ds and delete the Duplicates:
# - first lets creat 2 empty lists and assign them to the variables *Google_Ds_clean* and *already_added*. The first one will store our newly cleaned and unique rows, and the second will save the name of the apps we add to the list *Google_Ds_clean*
# 
# - Afterwards we will loop through our *Google_Ds* and isolate the variables *name* and *n_reviews*
#     - For each iteration we will append the rows/columns to our *Google_Ds_clean* list, if the variable *n_reviews* is equal to the value we had in our dict *reviews_max*, that should have the **key**(name of the app)**:value**(max review of that very app. And we also have to check if that app isnt already in the *already_added* list! We have to validate this condition because we have apps that have duplicate entries and that cannot be sorte through the nº of their reviews, because they simple have the same nº of reviews for all the duplicated entries! So one way to not include the duplicate entries is by when in each iteration we had that app in our *Google_Ds_clean* we also include its name in the list *already_added* and once its in this list even if it validates the first condition: **if n_reviews == reviews_max[name]** it will not be included because the name is already in the *already_added* list, therefore solving this issue!

# In[11]:


Google_Ds_clean = []
already_added = []

for column in Google_Ds[1:]:
    name = column[0]
    n_reviews = float(column[3])
    if n_reviews == reviews_max[name] and name not in already_added:
        Google_Ds_clean.append(column)
        already_added.append(name)

print(Google_Ds_clean[:10])
print('\n')
print(len(Google_Ds_clean))

explore_data(Google_Ds_clean, 0, 3, True) 
    


# #### Perfect! We can validate that our new and cleaned *Google_Ds_clean* has all the rows it should have: 9659

# ### Scouring through the Data of both Datasets one can check that there are several apps that are for non-english users!
# 

# In[12]:


print(Google_Ds_clean[4412][0])
print(Google_Ds_clean[7940][0])
print('\n')
print(Apps_Ds[814][1])


#   - Bellow we will try to creat a function that uses the ASCII counting system (0-127) to count each character of an inputed string and sort which ones bellong to the English common set of characters, and which ones dont:

# In[13]:


def check_str_Eng(a_string):
    
    for character in a_string:
        if ord(character) > 127:
            return False
    else: 
        return True
    '''esta linha do else tem que estar fora da 1º condição if. Isto vai fzr 1
           validação da 1º condição em cada loop e, se encontra dentro d cada
           iteração, seja ela a 1º iteração p ex, 1 caracter q seja verdadeiro 
           ele pára a iteração e da a string como verdadeira e correndo os 
           outros caracteres da string. Dai que temos que os correr todos 1º,
           para avaliar se não pertencem, e só dp de os corrermos tds é que 
           podemos validar a string como True, sim, pertence ao sistema ASCII'''
        


# In[14]:


print(check_str_Eng('Instagram'))


# In[15]:


print(check_str_Eng('爱奇艺PPS -《欢乐颂2》电视剧热播'))


# In[16]:


print(check_str_Eng('Docs To Go™ Free Office Suite'))


# In[17]:


print(check_str_Eng('Instachat 😜'))


# ### Some of the *"English_Apps"*  are being tagged as not bellonging to the Dataset of English language market target. This happens due to special characters embedded on their names, such as ™ or emojis
#     - We will have to create a different function, one that takes into account this special characters, and we will do so by first defining a cutoff. 
#     - Our new function should accept up to a max of 3 special characters per string in order to catalogue it as an *"English_Apps"*. Anything more than this and the app should fall into the category of non-english!

# In[18]:


def check_str_Eng_1(a_string):
    n_Falses = 0
    for character in a_string:
        if ord(character) > 127:
            n_Falses += 1
            if n_Falses > 3:
                return False
    else:
        return True


# In[19]:


print(check_str_Eng_1('Docs To Go™ Free Office Suite'))


# In[20]:


print(check_str_Eng_1('Instachat 😜'))


# In[21]:


print(check_str_Eng_1('爱奇艺PPS -《欢乐颂2》电视剧热播'))


# ## PERFECT, VALIDATED! 

# - Applying our function to both Datasets:

# In[22]:


Google_Ds_clean_1 = []
Apps_Ds_clean_1 = []


for app in Google_Ds_clean:
        name = app[0]
        if check_str_Eng_1(name):
            Google_Ds_clean_1.append(app)
            
for app in Apps_Ds:
    name = app[1]
    if check_str_Eng_1(name):
        Apps_Ds_clean_1.append(app)

explore_data(Google_Ds_clean_1, 0, 4, True)
print('\n')
print('\n')
explore_data(Apps_Ds_clean_1, 0, 4, True)

        


# ### Now we are moving to our last stage of the data cleaning process! We already:
#     - Removed inncurate data;
#     - Removed duplicate app entries;
#     - Removed non-English apps.
# ### Now its time to remove all the apps from both Datasets that arent for free:

# In[23]:


Google_Ds_clean_2 = []
Apps_Ds_clean_2 = []


for column in Google_Ds_clean_1[1:]:
    type_price = column[6]
    price = column[7]
    if type_price == 'Free' and price == '0':
        Google_Ds_clean_2.append(column)
        
for column in Apps_Ds_clean_1[1:]:
    price = column[4]
    if price == '0.0':
        Apps_Ds_clean_2.append(column)

explore_data(Google_Ds_clean_2, 0, 4, True)
print('\n')
print('\n')
explore_data(Apps_Ds_clean_2, 0, 4, True)
       


# #### We were left with **3222 rows in the Apps_Ds_clean_2** and **8862 in the Google_Ds_clean_2**

# ## In this phase we will need to evaluate which of the free apps from both Datasets are most common their own markets! We will do so by first constructing 2 frequency tables for each of the 2 Datasets and their respective genres 

# In[24]:


frequency_table_Google_Ds = {}
frequency_table_Apps_Ds = {}

for column in Google_Ds_clean_2[1:]:
    app_genre = column[1]
    
    if app_genre in frequency_table_Google_Ds:
        frequency_table_Google_Ds[app_genre] += 1
    else:
        frequency_table_Google_Ds[app_genre] = 1
     
    
for column in Apps_Ds_clean_2[1:]:
    app_genre = column[11]
    
    if app_genre in frequency_table_Apps_Ds:
        frequency_table_Apps_Ds[app_genre] += 1   
    else:
        frequency_table_Apps_Ds[app_genre] = 1

print('Google:',  frequency_table_Google_Ds)
print('\n')
print('Apps:', frequency_table_Apps_Ds)



# - ##### Now that we know that one of the most common free apps both in Apps and Google are of the genre *Games*:
# 
#     - Our goal will be to develop one *Game* app and provide it in the *Google App Store*. 
#     - We will do so by undertaken the minimun resources as this should be a sample pilot test that, if results in a good response from the market ougth to be further developed.
#         - If it reaches profitability in 6 months we should direct it to the *App Store* market as well! 

# - We can now creat a generic function, that we can use to extract a frequency table, expressed in percentages, out of any Dataset and of any feature of it! 
# 
# - That's what we will try to do bellow:

# In[25]:


def freq_table(dataset, index):
    feature_percentages = {}
    n_apps = len(dataset)
    features = {}
    for row in dataset:
        feature = row[index]
        if feature not in features:
            features[feature] = 1
        else:
            features[feature] += 1
      
    for key in features:
        value = features[key]
        feature_percentages[key] = 100 * value/n_apps
    
    return feature_percentages  


#    - Above we created a function that accpets 2 inputs (a dataset and an index. 
#     - Created 2 empty dicts (feature_percentages + features)
#     - Looped through each row of our choosen dataset, and for each loop we assigned our index row choosen to a variable named feature
#         - In each loop we check if the feature we've choosen is not in the empty dict we created named features, if it isn't we need to assigned that feature there as a *Key*. If in the next loop it finds there that feature as a *Key* it should add a value to it
#         
#     - After this we created another for Loop to iterate through the new and fully filled *features* dict. 
#         - for each iteration our loop will extract the *Value* out of each *Key* and asign it to a variable named **value**
#         - and also for each iteration it will fill our other empty dict **feature_percentages** with each *Key* and it corresponding *Value* but express as the percentage that it represents in the full length of our Dataset

# - Now let's see if it's working:

# In[26]:


freq_table(Google_Ds_clean_2, 1)


# ##### PERFECT!

# #### Aplying our *freq_table* function to another function (display_table()), in order to see/sort our frequency table in a particular order...:

# In[27]:


def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# In[28]:


print(display_table(Google_Ds_clean_2, 1))
print('\n')
print(display_table(Google_Ds_clean_2, 9))
print('\n')
print(display_table(Apps_Ds_clean_2, 11))


# #### Some first impressions on the FT (frequency table) of the DataSet Apps_Ds_clean_2 (Apple App Store_free_english_apps):
# 
#    - Analyzing the DataSet one can conclude that the most common genre in this sample is *Games* representing more than half (58%) of all the apps in our DataSet. Followed, far behind, by the genre *Entertainment* with approximately 8% (7.88%);
#    - Another interesting pattern in the DataSet is that there are almost no English free apps in the genre *Navigation*! Due to intensive competition from the free Google App *Google Maps* (?). Probably won't be either much market, I would risk almost none, for the paid ones in this genre! 
#     *Medical* is also a genre were developers do not offer much of free English Apps, maybe because this is more of a market that first has to "pass through" a middle man (doctor?) or an institution (hospital?) in order to monitize their products. Therefore, making it difficult for this market to profit and to rev up sales targeting directly their consumers, who first are not the most suitable ones to choose on their own this array of products, and second, in a legal matter, couldn't even do it all by themselfs without proper medical advice;
#    - Generally we can see that most of the free English apps are designed and developed towards entertainment rather than pratical purposes. With the top 6 being occupied by app genres such as *Games*, *Entertainment*, *Photo & Video*, *Education*, *Social Networking* and *Shoping* and the bottom 6 *Reference*, *Business*, *Book*, *Navigation*, *Medical*, *Catalogs*;
#    - One, based only in this FT, could not blindly recommend an app profile for this market. The info, I think, its insufficient to take any final conclusion. We could make a wrong conclusion by saying that if there's a lot of apps developed in the *Games* genre then maybe thats were there are more users or more market share. This could be right, but it could also be profoundly wrong! This could mean, for example, that Game apps are easier to develop, therefore being available for a big array of developers to jump in and flood the market, trying their luck. It could also mean that developing Games is cheaper, making this genre appealing for a pilot app for future development! **To better grasp this matter I think we should cross this info with others (rating_count_tot(?)**
# 

# #### Some first impressions on the FT of the DataSet Google_Ds_clean_2 (Google Play Store_free_english_apps):

#    - The most common **Genre** of apps here is *Tools* with 8,4% followed by *Entertainment* with aprox 6,07%, and in the third position comes Education counting ca. 5,35% of all free english apps developed; 
#    - In the **Category** designation *Tools* has also a prime position, coming in third with approximately 8,5%, in second is *Games* with 9,7% of all developed apps, and in the first position highlighted with almost 19% (18,9%) is the **Category** *Family*;
#    - Education and Productivity orientated Apps, play in Google Play Store a major role. With *Tools*, *Family*, and *Education* being in the top 3 of both **Genres** and **Category**;
#    - Comparing this patterns with the ones discovered in the **Apps_Ds_clean_2** DataSet we can conclude that although the **Genre** *Games* play an important role in both DataSet's, it is far less important in Google Play Store than in Apple Store (9,7% Vs. 58%). We can also assume that Apple Store is more Entertainment orientated compared to the Google one.
#    - Once more, for a better understandment and a more useful recommendation of which app to develop, we should cross this info with other such has *Installs* and *Reviews*. With this 3 sections we should get a pretty accurate view of whats the most popular genre of Apps, or which kind of App should we be targeting our efforts into.  

# In[29]:


genres = freq_table(Apps_Ds_clean_2, 11)
print(genres)


# In[30]:


for genre in genres:
    total = 0 #this variable will store the total nº of ratings for each genre
    len_genre = 0 #this variable will store the total nº of apps of each genre
    
    for row in Apps_Ds_clean_2:
        genre_app = row[11]
        if genre_app == genre:
            user_ratings_app = float(row[5])
            total += user_ratings_app
            len_genre += 1
            
    avg_user_ratings = total/len_genre
    
    print(genre, ':', avg_user_ratings)



    


# #### After doing this analysis, we can see that the most "popular" **Genre** is the *Navigation*. With an average of 86090 ratings per app developed. This is a very interesting result, since this one of the least developed apps_genre, coming in the top 3 of the last ones, followed by *Medical* and *Catalogs*.
# #### But I would no recommend a *Navigation* app, I would instead choose a *Social Networking* orientated one. It comes in 3rd has one of the most rated genres in average (71548) and on the other side is also one of the most popular genres in terms of number of apps developed, rating 5h (3.3%)

# In[31]:


Categories = freq_table(Google_Ds_clean_2, 1)
print(Categories)


# In[32]:


for category in Categories:
    total = 0
    len_category = 0
    
    for row in Google_Ds_clean_2:
        category_app = row[1]
        if category_app == category:
            n_installs = row[5]
            # Remove any + or , character, and then convert the string to a float.
            n_installs = n_installs.replace('+', '')
            n_installs = n_installs.replace(',', '')
            n_installs = float(n_installs)
            total += n_installs
            len_category += 1
            
    avg_category_installs = total/len_category
    print(category, ':', (round(avg_category_installs, 2)))

        
            
    


# ### After these results in both analysis (Apple Store + Google Play Store), I would recommend, as a free english-app our company should develop, an app orientated towards the *Social Network* ecosystem! Since in both DataSet's this genre/category is well positioned as beeing one of them that most buzz creats around users. Positioning itself at number 3 in Google Play Store, as one of the genres/categories with more installs in average per user (23253652.13). And if we take into consideration that the other first two genres/categories (*Communication* and *Video_Players*) may share apps with the *Social* genre and vice-versa, due to their similarity apps may have leaked and leaped from one of these 3 genres to another, we can attest the true value of the genre/category *Social Network/Social*
# 
# ### I would recommend the development of an app that could be used as a video-recording/Vlog and that could creat a social network around it and its users, sharing and commenting their content. Giving it also the ability to be shared in the more mainstream Social-Networks. Monetizing it in the first stage with adds, and in a second stage with fees, unlocking new abilities like for example UHD recording, following up to 100.000 friends or new recording filters. Taking full advantage of the 3 areas, *Communication*, *Video* and *Social* and also flowing with this new wave of a more narcissistic and influencers hostage society! 
