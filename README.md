# Data_Science_Portfolio

## Twitter Scraping Project

In this Portfolio you can find the code for the Twitter Scraping Project as ***Capstone_Project.py***

:star: **Project Title**: Twitter Scraping

:star: **Skills take away From This Project** : 
        :arrow_right: Python scripting
        :arrow_right: Data Collection
        :arrow_right: MongoDB
        :arrow_right: Streamlit
                                                

:star: **Domain** : Social Media

:star2:**Intro:**


  Today, data is scattered everywhere in the world. 
  Especially in social media, there may be a big quantity of data on Facebook, Instagram, Youtube, Twitter, etc. 
  This consists of pictures and films on Youtube and Instagram as compared to Facebook and Twitter. 
  To get the real facts on Twitter, here we have scraped the data from Twitter. 
  We have scraped the data like (date, id, url, tweet content, user,reply count, retweet count,language, source, like count etc) from twitter.
  

:star2:**Approach:**

:arrow_right:  By using the “snscrape” Library, Scraped the twitter data from Twitter. 
  *Reference:https://medium.com/dataseries/how-to-scrape-millions-of-tweets-using-snscrape-195ee3594721*
  
:arrow_right: Created a dataframe with date, id, url, tweet content, user,reply count, retweet count,language, source, like count.
  
:arrow_right:Stored each collection of data into a document into Mongodb along with the hashtag or key word we used to scrape from twitter. 
  
  *eg:({“Scraped Word”            : “Elon Musk”,
        “Scraped Date”             :15-02-2023,
        “Scraped Data”             : [{1000  Scraped data from past 100 days }]})*
        
:arrow_right:  Created a GUI using streamlit that contains the feature to enter the keyword or hashtag to be searched, select the date range and limit the tweet count need to be scraped. 

:arrow_right:  After scraping, the data is displayed on the page and button's are used to upload the data into the database and download the data into csv and json format.

:star2:**Conclusion:**


  This solution provides the user to scrape the twitter data in the database and allows the user to download the data with multiple data formats like csv and json.


