#!/usr/bin/env python
# coding: utf-8

# # Analysing Hacker_News Dataset (2nd Project)

# ### In this Project we will be exploring a Dataset from the famous Hacker News site. We will be analyzing some data from their community, mainly the posts submited by their users that target the Ask HN and Show HN options

# In[1]:


from csv import reader

hn_n = open('hacker_news.csv')
hn = reader(hn_n)
hn = list(hn)

print(hn[0:5])


# ##### Extracting and 'deleting' the first row from our Dataset. That corresponds to the Header:

# In[2]:


headers = hn[0]
hn = hn[1:]
print(headers)
print('\n')
print(hn[0:5])
print('\n')
print(len(hn))


# ##### Disaggregating and separating our Dataset into 3 new different Dataset's: Ask_HN; Show_HN and Other posts

# In[3]:


ask_posts = []
show_posts = []
other_posts = []

for row in hn:
    title = row[1]
    if title.lower().startswith('ask hn'):
        ask_posts.append(row)
    elif title.lower().startswith('show hn'):
        show_posts.append(row)
    else:
        other_posts.append(row)

print(len(ask_posts))
print(len(show_posts))
print(len(other_posts))



# In[4]:


#first 5 rows from ask_posts:
print(ask_posts[:5])

#first 5 rows from show_posts:
print(show_posts[:5])


# In[5]:


#Calculating the average comments in the ask_comments section:
total_ask_comments = 0

for row in ask_posts:
    num_comments = int(row[4])   
    total_ask_comments += num_comments

avg_ask_comments = total_ask_comments/len(ask_posts)
print('Ask_Comments_Avg:', avg_ask_comments)


#Calculating the average comments in the show_comments section:
total_show_comments = 0

for row in show_posts:
    num_comments = int(row[4])
    total_show_comments += num_comments
    
avg_show_comments = total_show_comments/len(show_posts)
print('Show_Comments_Avg:', avg_show_comments)
    


# ##### On average, Ask_Posts receive 4 more comments per post than its counterpart Show_Posts! (14.03 Vs. 10.32)
# ##### This can be because a question thread makes more buzz than any other. Piling up different opinions from different users, and a kind of argumentative battle between all of them, boosting up comments. 

# ##### In the next step we will create two dictionaries. One for the frequency of ask_posts by hour, and another one for the frequency of comments by hour. This task is to be able to calculate the average of 

# In[6]:


import datetime as dt

#Looping through the ask_posts list, and creating a new
#list of lists, using the append method and inside the
#append method instead of using one object(a single list,
#or a sinle variable) we use 2 and wrap them up in a 
#single list ([]). So that when the append method works
#it will append that list inside another empty list
#(result_list), creating a list of lists:
result_list = []

for row in ask_posts:
    created_at = row[6]
    num_comments = row[4]
    result_list.append([created_at, num_comments])

#print(result_list)

#Another way of doing the same things as above, is by 
#using the List Comprehension method:

result_list_2 = [[row[6], row[4]] for row in ask_posts]
#print(result_list_2)

#The above method is a more elegant and Pythonic way of
#doing it! Here we consume less memory and write less 
#code, being less prone to mistakes! 

counts_by_hour = {}
comments_by_hour = {}

for row in result_list:
    hour_date = row[0]
    comments = int(row[1])
    hour_date_int = dt.datetime.strptime(hour_date, '%m/%d/%Y %H:%M')
    hour = hour_date_int.strftime('%H')
    if hour not in counts_by_hour:
        counts_by_hour[hour] = 1
        comments_by_hour[hour] = comments
    else:
        counts_by_hour[hour] += 1
        comments_by_hour[hour] += comments
        
print(counts_by_hour)
print('\n')
print('\n')
print(comments_by_hour)


# ##### Now its time to create a list of lists displaying the average number of comments per post in each hour! 
# ##### Our lists will have two elements each, being the first the hour, and the second the average between the number of comments and the number of posts. The first element(hour) will act as the key and the second(average) as its value, just like in a dictionary 

# In[7]:


avg_by_hour = []

for hour in comments_by_hour:
    avg_by_hour.append([hour, (int(comments_by_hour[hour])/counts_by_hour[hour])])

print(avg_by_hour)


# ##### Although a bit confusing at first glanse, we can already see from this analysis that the hour of the day that receives more Comments per Post (ask_post) is the 15th hour. With an average number of approximatly 39 comments per post, 3 o'clock ranks far ahead at number 1

# ##### We should work on our avg_by_hour list of lists, in order to make it more clean, and more user friendly. But also to present its results in a better readable way!
# ##### We are going to do this first by creating a new list were we swap the columns of our avg_by_hour list of lists, then we will sort its lists, and present the first five results:

# In[8]:


swap_avg_by_hour = []

# Using a for loop to iterate over the elements of the avg_by_hour variable
# and append those elemenst into a new list of lists, swap_avg_by_hour, but
# with the original columns swaped:
for row in avg_by_hour:
    swap_avg_by_hour.append([row[1], row[0]])
    
print(swap_avg_by_hour)
print('\n')

# Sorting through the swap_avg_by_hour, and doing it in descending order:
sorted_swap = sorted(swap_avg_by_hour, reverse=True)
#print(sorted_swap)

# Presenting the top 5 results of the sorted list, and presenting them using
# the str.format() method, were the first element is the hour, and the second
# the average of comments received per hour, presented in to 2 decimal places:
print("Top 5 Hours for Ask Posts Comments:")
for row in sorted_swap[:5]:
    avg_comments = row[0]
    h = row[1]
    h = dt.datetime.strptime(h, '%H')
    h_str = h.strftime('%H:%M')
    comments_h_str = '{}: {:.2f} average comments per post'. format(h_str, avg_comments)
    print(comments_h_str)
    
    


# ### After the analysis we can clearly tell that the best hour of the day to create an ask_post, in order to have a higher chance of receiving comments, would be around 3p.m. With an average of approximately 39 comments per post its by far the best time of the day. Followed by 02:00, with roughly 24 comments per post, and then 20:00 with 21 comments. 
# ### These hours all come in the timezone of the DataSet, that is EST USA (UTC/GMT -4). If we want to put it in our/mine timezone (GMT+1), we should had 5 more hours to it. So the results for us, sharing the same timezone, should be 20:00 @#1; 07:00 @#2; 01:00 @#3.
