# Data_Science_Portfolio

In this Portfolio you can find a Capstone_Project.py

Capstone_Project.py

:star: Project Title: Twitter Scraping

:star: Skills take away From This Project : Python scripting, Data Collection,MongoDB, Streamlit

Domain : Social Media

Intro:
  Today, data is scattered everywhere in the world. 
  Especially in social media, there may be a big quantity of data on Facebook, Instagram, Youtube, Twitter, etc. 
  This consists of pictures and films on Youtube and Instagram as compared to Facebook and Twitter. 
  To get the real facts on Twitter, here we have scraped the data from Twitter. 
  We can Scrape the data like (date, id, url, tweet content, user,reply count, retweet count,language, source, like count etc) from twitter.
  

Approach:
  By using the “snscrape” Library, Scrape the twitter data from Twitter. 
  Reference:https://medium.com/dataseries/how-to-scrape-millions-of-tweets-using-snscrape-195ee3594721
  
  Create a dataframe with date, id, url, tweet content, user,reply count, retweet count,language, source, like count.
  
  Store each collection of data into a document into Mongodb along with the hashtag or key word we use to  Scrape from twitter. 
  eg:({“Scraped Word”            : “Elon Musk”,
        “Scraped Date”             :15-02-2023,
        “Scraped Data”             : [{1000  Scraped data from past 100 days }]})
        
  Created a GUI using streamlit that contains the feature to enter the keyword or hashtag to be searched, select the date range and limit the tweet count need to be     scraped. 
  After scraping, the data needs to be displayed in the page and need a button to upload the data into Database and download the data into csv and json format.

Conclusion:
  This solution provides the user to scrape the twitter data in the database and allows the user to download the data with multiple data formats like csv and json.


