import configparser

import mysql
import tweepy
import pandas as pd
from mysql.connector import Error
import pip
package ='tweepy'
pip.main(['install',package])

config = configparser.ConfigParser()
config.read('venv/config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']



#Creating an empty dataframe to store the information
# tweets =pd.DataFrame(columns=["id","created_at","twitter_handle","text","media_url",location = 'India'])
# userdataFrame = pd.DataFrame(columns=["twitter_handle", "user_name", "description", "followers_count", "following_count", "profile_url"])
keywords=['Blood']
limits=2000

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

outtweets = [] #initialize master list to hold our ready tweets
user = [] #initialize user list to hold our user tweets
mentions = [] #initialize mentions list
url = [] #initialize mentions list
tags = [] #initialize mentions list

for tweet in tweepy.Cursor(api.search_tweets,q=keywords,count=100, #The q variable holds the hashtag
                           lang="en").items(limits):

    mentions = tweet.entities.get('user_mentions',[])
    for mentioned in mentions:
        mentioned_user = mentioned['screen_name']

    hastags = tweet.entities.get('hashtags', [])
    for hash in hastags:
        htag = hash['text']

    media = tweet.entities.get('media', [])

    if(tweet.entities.get('media',[])) : #This condition appends only those tweets to the list which have image URL's
        media = tweet.entities.get('media')
        outtweets.append([tweet.id_str,tweet.created_at,tweet.user.screen_name,tweet.text.encode("utf-8"),media[0]['media_url'],tweet.user.location])
        user.append([tweet.user.screen_name,tweet.user.name,tweet.user.description,tweet.user.followers_count, tweet.user.friends_count, tweet.user.profile_image_url_https, tweet.user.created_at])
        mentions.append([tweet.id_str, tweet.user.name, mentioned_user, tweet.source, tweet.favorite_count])
        url.append([tweet.id_str, media[0]['media_url']])
        tags.append([tweet.id_str, htag])
        print("hasttags print")
        print(htag)
        # print(media[0]['media_url'])

tweetdf = pd.DataFrame(outtweets,columns = ["Id","Created_at","twitter_handle","Text","URL","Location"])
tweetdf.to_csv('Tweets.csv',sep=",",encoding="utf-8")
data=pd.read_csv('Tweets.csv',encoding="utf-8", index_col=False , delimiter=",")
data.drop(columns = data.columns[0], axis = 1, inplace= True)
data.head()

userdataFrame = pd.DataFrame(user, columns=["twitter_handle", "user_name", "description", "followers_count", "following_count", "profile_url", "joined_on"])
userdataFrame.to_csv('UserData.csv', sep=",", encoding= "utf-8")
userdata = pd.read_csv('UserData.csv', encoding = "utf-8", index_col=False, delimiter=",")
userdata.drop(columns = userdata.columns[0], axis = 1, inplace= True)
userdata.head()

mentionsDataFrame = pd.DataFrame(mentions, columns=["tweet_id", "user_name", "user mentions", "source_of_tweet", "likes_count"])
mentionsDataFrame.to_csv('Mentions.csv', sep=",", encoding= "utf-8")
mentionsData = pd.read_csv('Mentions.csv', encoding = "utf-8", index_col=False, delimiter=",")
mentionsData.drop(columns = mentionsData.columns[0], axis = 1, inplace= True)
mentionsData.head()

urlDataFrame = pd.DataFrame(url, columns=["id", "url"])
urlDataFrame.to_csv('UrlData.csv', sep=",", encoding= "utf-8")
urlData = pd.read_csv('UrlData.csv', encoding = "utf-8", index_col=False, delimiter=",")
urlData.drop(columns = urlData.columns[0], axis = 1, inplace= True)
urlData.head()

tagsDataFrame = pd.DataFrame(tags, columns=["id", "hashtags"])
tagsDataFrame.to_csv('TagsData.csv', sep=",", encoding= "utf-8")
tagsData = pd.read_csv('TagsData.csv', encoding = "utf-8", index_col=False, delimiter=",")
tagsData.drop(columns = tagsData.columns[0], axis = 1, inplace= True)
tagsData.head()

def replace_empty_string(row):
    new_row = []
    for i in row:
        if i == None or str(i) == "nan":
            new_row.append("")
        else:
            new_row.append(i)
    return new_row

print(data.head())
# print(user)

try:
    conn = mysql.connector.connect(host='localhost', database='assignment2', user='root', password='root')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS twitterdata;')
        cursor.execute('DROP TABLE IF EXISTS twitterUser;')
        cursor.execute('DROP TABLE IF EXISTS userMentions;')
        cursor.execute('DROP TABLE IF EXISTS tweetUrl;')
        cursor.execute('DROP TABLE IF EXISTS hashtagsData;')
        print('Creating table..')

        if cursor.execute("CREATE TABLE twitterUser(twitter_handle varchar(255), user_name varchar(255), description varchar(500), followers_count int, following_count int, profile_url varchar(255), joined_on datetime)"):
            print("Table user is created ....")

        for a, row in userdata.iterrows():
            # here %S means string values
            sql = "INSERT INTO assignment2.twitterUser VALUES (%s, %s, %s, %s, %s, %s, %s)"
            row = replace_empty_string(row)
            cursor.execute(sql, tuple(row))
            print("Record inserted in twitterUser")

        # in the below line please pass the create table statement which you want #to create
        if cursor.execute("CREATE TABLE twitterdata(tweet_id varchar(30), tweet_time datetime, twitter_handle varchar(255), tweet varchar(500), profile_image_url varchar(200),location varchar(200))"):
            print("Table data is created....")

        # loop through the data frame
        for i, row in data.iterrows():
            # here %S means string values
            sql = "INSERT INTO assignment2.twitterdata VALUES (%s, %s, %s, %s,%s,%s)"
            row = replace_empty_string(row)
            cursor.execute(sql, tuple(row))
            print("Record inserted twitterdata")

        if cursor.execute("CREATE TABLE userMentions(tweet_id varchar(30), source_user varchar(255), target_user varchar(255), tweet_source varchar(255), tweet_likes varchar(30))"):
            print("userMentions table created..")
        for i, row in mentionsData.iterrows():
            sql = "INSERT INTO assignment2.userMentions VALUES (%s, %s, %s, %s, %s)"
            row = replace_empty_string(row)
            cursor.execute(sql, tuple(row))
            print("Record inserted userMentions")

        if cursor.execute("CREATE TABLE tweetUrl(tweet_id varchar(30), url varchar(250))"):
            print("Table tweetURL is created ....")
        for i, row in urlData.iterrows():
            sql = "INSERT INTO assignment2.tweetUrl VALUES(%s, %s)"
            row = replace_empty_string(row)
            cursor.execute(sql, tuple(row))
            print("Record inserted tweetUrl")

        if cursor.execute("CREATE TABLE hashtagsData(tweet_id varchar(30), hashtags varchar(250))"):
            print("Table hashtagsData is created ....")
        for i, row in tagsData.iterrows():
            sql = "INSERT INTO assignment2.hashtagsData VALUES(%s, %s)"
            row = replace_empty_string(row)
            cursor.execute(sql, tuple(row))
            print("Record inserted hashtagsData")
        # cursor.execute("Alter Table twitterdata add Constraint 'Tweets_Fk1'  Foreign Key (twitter_handle) References twitterUser(twitter_handle)")
        # the connection is not auto committed by default, so we must commit to save our changes
        conn.commit()
except Error as e:
    print("Error while connecting to MySQL", e)


