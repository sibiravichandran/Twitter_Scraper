import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
import json
import streamlit_option_menu as streamlit_option
import time
import webbrowser
from PIL import Image


my_pic = Image.open("Sibi.jpg")
logo_twitter = Image.open("TwitterLogo.png")

# Defining the code on functional blocks

# Scraping the data from twitter for a max tweets of 1000 between a specified date range
@st.cache_data
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
    time.sleep(2)
    return tweets_df


# Uploading the data to mongodb database

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
    page_title="Twitter Scraper",
    page_icon=logo_twitter,
    layout="wide"
)

page_bg_img = '''
<style>
[data-testid="stAppViewContainer"]{
    background-image: url("https://wallpaperaccess.com/full/1884898.jpg");
    
    background-size: cover;
}



[data-testid="stHeader"]{
    background-color: rgba(0,0,0,0);
}


</style>
'''


st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("**:blue[Twitter Scraping Capstone]**")



selected1 = streamlit_option.option_menu(
    menu_title = "",  
    options = ["Home","About","Scrape Twitter Data","Contact"],
    icons =["house","bar-chart","search", 'at'],
    orientation="horizontal",
    default_index=0,
    styles={
        
        "nav-link": {"--hover-color": "#1DA1F2"},
        "nav-link-selected": {"background-color": "#1DA1F2"}
    })

if selected1 == "About":
    st.header("*:green[Twitter Scrapper]*")
    st.subheader('Twitter Scraper is a tool or program used to extract data from Twitter in an automated and efficient manner. Twitter Scraper allows users to collect data from Twitter, such as tweets, hashtags, user profiles, and more, and store that data in a structured format, such as a CSV file or a database.There are many different Twitter scraping tools available, ranging from simple Python libraries like Tweepy and Snscrape to more complex commercial solutions. The choice of tool will depend on the specific needs of the user and the amount of data they wish to collect.')

    # Info about Snscraper
    st.header("*:orange[Snscraper]*")
    st.subheader('Snscrape is a Python package used for scraping data from social media platforms, with a focus on Twitter. It allows you to scrape data such as tweets, users, and hashtags by using various search queries. Snscrape provides a more flexible and robust way of scraping Twitter data compared to the Twitter API, as it is not subject to API limits or restrictions. Snscrape can be used to collect data for research, analysis, and other purposes.')

    # Info about MongoDB database
    st.header("*:violet[Mongo DB]*")
    st.subheader('MongoDB is a popular open-source document-oriented NoSQL database. It is designed to handle large volumes of unstructured and semi-structured data, making it a good choice for modern applications that require flexible data models. MongoDB stores data as JSON-like documents, which can be nested and have dynamic schemas. It provides a rich query language and supports indexing for fast and efficient querying of data. MongoDB can be used for a variety of use cases, including web applications, mobile applications, content management systems, and more.')

    # Info about Streamlit framework
    st.header("*:red[Streamlit]*")
    st.subheader('Streamlit is a Python library used for building web applications for data science and machine learning projects. It allows data scientists and developers to easily create interactive and customizable web interfaces for their models, data visualizations, and other projects without having to write extensive HTML, CSS, or JavaScript code. Streamlit simplifies the process of creating web applications by providing pre-built widgets and components that can be used to create interactive and responsive user interfaces with minimal coding. It also integrates well with popular data science libraries like Pandas and Matplotlib, making it a popular choice for building data science and machine learning applications.')

elif selected1 == "Scrape Twitter Data":
    SearchTerm = st.text_input('**:blue[Enter your keyword]**')
    sincedate = st.date_input('**:blue[Since]**', min_value = pd.to_datetime('1990,01,01'), max_value = pd.to_datetime('2099,01,12'), value=pd.to_datetime('today') - pd.Timedelta(days=7) )
    untildate = st.date_input('**:blue[Until]**', min_value=pd.to_datetime('1990,01,01'), max_value = pd.to_datetime('2099,31,12'), value=pd.to_datetime('today'))
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
            
            scraped_data1 = scraped_tweets(SearchTerm, sincedate, untildate, maxTweets-1)
            #init_connection()
            upload_data_mongodb(scraped_data1)
            
            st.success('Data uploaded to MongoDB Successfully!!! :white_check_mark:')
    except Exception as e:
        st.write(e)    
  
    try:       
        
        scraped_data2 = scraped_tweets(SearchTerm, sincedate, untildate, maxTweets-1)
        csv = download_csv(scraped_data2)
        downloading_csv = st.download_button('Download CSV', csv, 'Scraped_Tweets.csv' ,'text/csv')
        if downloading_csv:
            st.success('CSV File Downloaded Successfully!!!')
            
            #csv contains the contents of the csv file 
            #text/csv indicates the nature of file to be downloaded which is of mime(Multipurpose Internet Mail Extensions or MIME type) type of data and tells the browser that the file is a csv file
    except Exception as e:
        st.write(e)    

    try:
        scraped_data3 = scraped_tweets(SearchTerm, sincedate, untildate, maxTweets-1)
        json_data = download_json(scraped_data3)
        downloading_json = st.download_button('Download JSON',  json_data, 'Scraped_Tweets.json', 'application/json')    
        
        if downloading_json:
                st.success("JSON File Downloaded Successfully!!!")
                #json_data contains the contents of the json file 
                #'application/json' indicates the nature of file to be downloaded which is of mime(Multipurpose Internet Mail Extensions or MIME type) type of data and tells the browser that the file is a json file
    except Exception as e:
        st.write(e)    
        

elif selected1 == "Contact":
    
    name = " *:red[SIBI RAVICHANDRAN]* "
    mail = (f'{"*ravisibi16@gmail.com*"}')
    
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(my_pic)
        if st.button('Github'):
            webbrowser.open_new_tab("https://github.com/sibiravichandran")
        if st.button('LinkedIn'):
            webbrowser.open_new_tab("https://www.linkedin.com/in/sibi-ravichandran-817ab021b/")
        
    with col2:
        st.title(name)
        st.subheader(mail)
        st.subheader("Aspiring Data Scientist with a passion for turning data into insights and using those insights to drive business decisions.I bring a wealth of knowledge and expertise to any organization looking to streamline their operations and drive growth through effective use of technology.") 
        st.subheader("With a passion for continuous learning and professional as well as personal development, I am dedicated to staying on the cutting edge of industry trends and best practices, and am always seeking out new challenges and opportunities to expand my skillset.") 
        st.subheader("Whether it's through formal education, online courses, or simply exploring new ideas and perspectives, I am passionate about staying curious and engaged with the world around me.")
        st.subheader("With a commitment to continuous growth and development, I am constantly pushing myself to reach new heights and take on new challenges and I am committed to sharing my knowledge and insights with others, and am always eager to collaborate and exchange ideas with fellow professionals in the field.. If you share my love of learning and are looking for a dynamic and enthusiastic team member to help drive innovation and success in your organization, I would love to hear from you!")
        st.write("---")
        
    # st.write("#")

            
elif selected1 == "Home":
    st.header("**:blue[_Welcome to the Twitter Scraping Project!_]** :speech_balloon:")


    st.subheader('Twitter is a powerful platform that offers a wealth of information on a wide range of topics. From news updates to customer feedback, Twitter is a treasure trove of valuable insights that businesses and individuals can leverage to enhance their operations and decision-making processes. However, with billions of tweets being sent every day, it can be overwhelming to manually sift through this information.')
    
    st.subheader("Thats where our Twitter scraping project comes in. By using cutting-edge web scraping techniques, we collect and analyze Twitter data to help you gain a deeper understanding of your target audience, industry trends, and more. Our scraping methods are ethical, transparent, and comply with Twitter's terms of service, ensuring that you receive reliable and accurate data.")
    
    
    st.subheader("Here, we aim to provide you with valuable insights and data analysis of Twitter content by utilizing advanced web scraping techniques. The main goal is to help you make informed decisions by leveraging the vast amount of data available on Twitter.")
    
    st.subheader('This Twitter Scraping web app is created using Streamlit.')
    st.subheader("The tweets once scraped can then be uploaded into the MongoDB database and can be downloaded as CSV or a JSON file.")
    
    st.subheader("Whether you're a business looking to improve your marketing strategy or an individual looking to stay up-to-date on the latest trends, our Twitter scraping project has got you covered. We are committed to providing you with the best possible service and look forward to helping you achieve your goals.")