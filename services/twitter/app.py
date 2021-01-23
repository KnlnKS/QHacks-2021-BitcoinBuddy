import tweepy
import os
from google.cloud import language_v1
import pandas as pd 

consumer_key = 'qVpsb29zjvsxrKVBRSsReTH5N'
consumer_secret = '9jUcw1nyqcFtMePt98zPkDUPrH6TTu80KmkOeoDAfALeEWNVtp'
access_token = '4901508948-bU4lSJOGL0QED2KZQR2tbfhtLWDF1jxgFJFPzTi'
access_token_secret = 'IKqUMpgF1flHztV4qzi39QLrsicBXW1TrmElSI6hXF4P9'

tweetsPerQry = 2
maxTweets = 100
hashtag = "#bitcoins OR #bitcoin OR #BTC"

authentication = tweepy.OAuthHandler(consumer_key, consumer_secret)
authentication.set_access_token(access_token, access_token_secret)

api = tweepy.API(authentication, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

tweet_count = 0
list_posts = []
newTweets = tweepy.Cursor(api.search, q=hashtag, lang="en", result_type="recent", tweet_mode="extended").items(500)
#newTweets = api.search(q=hashtag, result_type="recent").items(5)#, tweet_mode="extended")
for tweet in newTweets:
    #print(f"{tweet.user.name}:{tweet.text}")
    try:
        #print(tweet.retweeted_status.full_text)
        list_posts.append(tweet.retweeted_status.full_text.encode('utf-8'))
        tweet_count += 1
    except AttributeError:  # Not a Retweet 
        #print(tweet.full_text)
        list_posts.append(tweet.full_text.encode('utf-8'))
        tweet_count += 1
    print("NEXT!!")
list_posts = pd.DataFrame(list_posts, columns = ['tweet'])
#list_posts.to_csv('test.csv')
print(tweet_count)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "InfluxElectric-f281b5ae4c8a.json"
client = language_v1.LanguageServiceClient()
new_file = []


for x in range (len(list_posts)):
    type_ = language_v1.Document.Type.PLAIN_TEXT
    print("test")
    
    document = {"content": list_posts['tweet'][x], "type_": type_}
    
    #document = language_v1.Document(content=list_posts[x], type_=language_v1.Document.Type.PLAIN_TEXT)
    encoding_type = language_v1.EncodingType.UTF8
    
    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})
    
    sscore = round(response.document_sentiment.score,4)
    smag = round(response.document_sentiment.magnitude,4)
    

    new_file.append([list_posts['tweet'][x], sscore, smag])
    '''
    try:
        print("tried")
        document = language_v1.Document(content=list_posts[x], type_=language_v1.Document.Type.PLAIN_TEXT)
        sentiment = client.analyze_sentiment(document=document).document_sentiment
        sscore = round(sentiment.score,4)
        smag = round(sentiment.magnitude,4)

        print("SSCORE: " + sscore)
 
        list_posts[x]["score"] = sscore
        list_posts[x]["magnitude"] = smag
         
    except Exception as e:
        print("and failed")
        print(e)
        list_posts[x]["score"] = 0
        list_posts[x]["magnitude"] = 0
    '''
new_file = pd.DataFrame(new_file, columns = ['text', 'score', 'magnitude'])
new_file.to_csv('tweet_data.csv', header=True, index=False)

#print (listposts)