import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
import json



# Defining the code on functional blocks

# Scraping the data from twitter for a max tweets of 1000 between a specified date range

def scraped_tweets(SearchTerm, sincedate, untildate, maxTweets):    

# Creating list to append tweet data to
  tweets_list = []
  if(maxTweets<=1000):
# Using TwitterSearchScraper to scrape data and append tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{SearchTerm} since:{sincedate}  until:{untildate}').get_items()):
        if i>maxTweets:
          break
        #Scrape the data like (date, id, url, tweet content, user,reply count, retweet count,language, source, like count etc) from twitter 
        tweets_list.append([tweet.date, tweet.id, tweet.url,tweet.content, tweet.user.username, tweet.replyCount, tweet.retweetCount, tweet.lang, tweet.source, tweet.likeCount])
        print(tweets_list)
# Creating a dataframe from the tweets list above
# Create a dataframe with date, id, url, tweet content, user,reply count, retweet count,language, source, like count.
    tweets_df = pd.DataFrame(tweets_list, columns=['Datetime', 'TweetId', 'URL', 'TweetContent', 'Username', 'ReplyCount', 'RetweetCount', 'Language', 'Source', 'Like Count'])
    return tweets_df


# Uploading the data to mongodb database

#Your local Streamlit app will read secrets from a file .streamlit/secrets.toml in your app's root directory.
# Initialize connection.
# Uses st.cache_resource to only run once.
# @st.cache_resource is a decorator that tells Streamlit to cache the results of the init_connection() function. 
# This means that if the function is called again with the same arguments, Streamlit will return the cached result instead of recomputing the function. 
# This can save a lot of time if the function is expensive to compute.
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])
#return pymongo.MongoClient(**st.secrets["mongo"]) returns a new MongoClient object, which is used to connect to a MongoDB database. 
#The ** syntax is used to pass a dictionary of parameters to the MongoClient() constructor, and the st.secrets["mongo"] dictionary is likely used to store the connection string and other parameters needed to connect to the database.


client = pymongo.MongoClient("mongodb://localhost:27017")

# Use st.cache_data to only rerun when the query changes or after 10 min.
# If your database updates more frequently, you should adapt time-to-live[ttl] or remove caching so viewers always see the latest data
# The cache has a TTL of 600 seconds, which means that the cached result will be stored for up to 10 minutes before it is invalidated and the function is re-run.
@st.cache_data(ttl=600)
def upload_data_mongodb(tweets_df):
  
    db = client.Capstone #Database name
    collection_name = db.CapstoneProject  #Collection name
    data = {
      "Scraped Word":SearchTerm,
      "Scraped date": pd.to_datetime('today'),
      "Scraped Data": pd.DataFrame(tweets_df).to_dict('records') #'records' : list like [{column -> value}, … , {column -> value}]
    }
    return collection_name.insert_one(data)


# Downloading the file as csv and json

#st.cache_data is a decorator to cache functions that return data (e.g. dataframe transforms, database queries, ML inference).
#Cached objects are stored in "pickled" form, which means that the return value of a cached function must be pickleable. Each caller of the cached function gets its own copy of the cached data.
#You can clear a function's cache with func.clear() or clear the entire cache with st.cache_data.clear().
@st.cache_data
def download_csv(tweets_df):
  # ignore index while writing/exporting DataFrame to CSV file.
  return pd.DataFrame(tweets_df).to_csv(index=False).encode()
#The above code takes the dataframe and converts it to a a CSV formatted string.
#.encode(): Encodes the Python string as bytes, using the default UTF-8 encoding. 
# This is necessary if you want to transmit the CSV data over a network, as bytes are the format used for transmitting data over the internet.
# By default, the index is set true,to not to include the index in the csv file we are setting the index=False

def download_json(tweets_df): 
  return json.dumps(pd.DataFrame(tweets_df).to_json(orient = 'records')).encode()
#json.dumps(): Converts the JSON string to a Python string. 
# The dumps() function is part of Python's built-in json module, and is used to encode a Python object as a JSON-formatted string.
#The above code takes the dataframe and converts it to a a json formatted string using a record orientation which creates a JSON array of records.
#.encode(): Encodes the Python string as bytes, using the default UTF-8 encoding. 
# This is necessary if you want to transmit the JSON data over a network, as bytes are the format used for transmitting data over the internet.

# Creating a GUI using the streamlit 

st.set_page_config(
    page_title="Hello Folks",
    page_icon="👋",
)

st.title("**:blue[Twitter Scraping Capstone]**")


st.markdown("**:blue[_Welcome to the Twitter Scraping Capstone Page_]** :speech_balloon:")

SearchTerm = st.text_input('**:red[Enter your keyword]**')
sincedate = st.date_input('**:red[Since]**', min_value = pd.to_datetime('1990,01,01'), max_value = pd.to_datetime('2099,01,12'), value=pd.to_datetime('today') - pd.Timedelta(days=7) )
untildate = st.date_input('**:red[Until]**', min_value=pd.to_datetime('1990,01,01'), max_value = pd.to_datetime('2099,31,12'), value=pd.to_datetime('today'))
maxTweets = st.slider('**:blue[Tweets to be scraped]**',min_value=1,max_value=1000)

try:
  scraped_keyword = st.button('Scraping Keyword')

# Scrape the data
  if scraped_keyword:
    scraped_data = scraped_tweets(SearchTerm, sincedate, untildate, maxTweets-1)
    st.write('Scraped tweets', len(scraped_data))
    
    # Show the data in the page
    st.write('Scraped data:')
    st.dataframe(scraped_data)
except Exception as e:
  st.write(e)    

try:
  uploading_to_mongoDb = st.button('Upload to MongoDB')
  if uploading_to_mongoDb:
          st.write('Uploading data to MongoDB...')
          scraped_data1 = scraped_tweets(SearchTerm, sincedate, untildate, maxTweets-1)
          init_connection()
          upload_data_mongodb(scraped_data1)
          
          st.write('Data uploaded to MongoDB :white_check_mark:')
except Exception as e:
  st.write(e)    
  
try:       
  downloading_csv = st.button('Download as CSV')   
  if downloading_csv:
        scraped_data2 = scraped_tweets(SearchTerm, sincedate, untildate, maxTweets-1)
        csv = download_csv(scraped_data2)
        st.download_button('Confirm Download CSV', csv, 'Scraped_Tweets.csv' ,'text/csv')
        #csv contains the contents of the csv file 
        #text/csv indicates the nature of file to be downloaded which is of mime(Multipurpose Internet Mail Extensions or MIME type) type of data and tells the browser that the file is a csv file
except Exception as e:
  st.write(e)    

try:    
  downloading_json = st.button('Download as JSON')
  if downloading_json:
        scraped_data3 = scraped_tweets(SearchTerm, sincedate, untildate, maxTweets-1)
        json_data = download_json(scraped_data3)
        st.download_button('Confirm Download JSON',  json_data, 'Scraped_Tweets.json', 'application/json')
        #json_data contains the contents of the json file 
        #'application/json' indicates the nature of file to be downloaded which is of mime(Multipurpose Internet Mail Extensions or MIME type) type of data and tells the browser that the file is a json file
except Exception as e:
  st.write(e)    

