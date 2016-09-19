import configparser
import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import urllib.request, urllib.error, urllib.parse, time, os, re, getopt, sys

from nltk.chat import eliza

from random import randint

config = configparser.ConfigParser()
config.read('.twitter')

consumer_key = config.get('apikey', 'key')
consumer_secret = config.get('apikey', 'secret')
access_token = config.get('token', 'token')
access_token_secret = config.get('token', 'secret')
stream_rule = config.get('app', 'rule')
account_screen_name = config.get('app', 'account_screen_name').lower()
account_user_id = config.get('app', 'account_user_id')

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitterApi = API(auth)

chatbot = eliza.Chat(eliza.pairs)

responseOptions =['Hey There! ', 'Lookin\' good, gorgeous! ','It\'s hot up here...and lonely ', 'If a FSU student falls and no one hears it, does its team still suck? ','HEYY ']

#for the scraper
axisip='10.179.2.87'
basename='umiami'


class ReplyToTweet(StreamListener):

    def on_data(self, data):
        #print(data)
        tweet = json.loads(data.strip())

        retweeted = tweet.get('retweeted')
        from_self = tweet.get('user',{}).get('id_str','') == account_user_id

        if retweeted is not None and not retweeted and not from_self:
            #just get some info...this is useful for debugging
            tweetId = tweet.get('id_str')
            screenName = tweet.get('user',{}).get('screen_name')
            tweetText = tweet.get('text')

            #scrape the image
            auth_handler = urllib.request.HTTPBasicAuthHandler()
            opener = urllib.request.build_opener(auth_handler)
            urllib.request.install_opener(opener)
            axis_jpg=urllib.request.urlopen('http://10.179.2.87/axis-cgi/jpg/image.cgi')
            filename='%s_%s_%s.jpg' % ( basename, time.strftime('%Y%m%d'), time.strftime('%H%M%S') )
            local_jpg=open(filename,'wb')
            local_jpg.write(axis_jpg.read())
            local_jpg.close()

            #choose the tweet
            tweetchoice = randint(0,4)
            chatResponse = responseOptions[tweetchoice]

            #make the reply text
            replyText = '@' + screenName + ' ' + chatResponse

            #check if repsonse is over 140 char
            if len(replyText) > 140:
                replyText = replyText[0:139] + '…'

            print('Tweet ID: ' + tweetId)
            print('From: ' + screenName)
            print('Tweet Text: ' + tweetText)
            print('Reply Text: ' + replyText)

            # If rate limited, the status posts should be queued up and sent on an interval
            #twitterApi.update_status(status=replyText, in_reply_to_status_id=tweetId)
            twitterApi.update_with_media(filename,status=replyText,in_reply_to_status_id=tweetId)

#pleasedontbreak...
    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    streamListener = ReplyToTweet()
    twitterStream = Stream(auth, streamListener)
    twitterStream.userstream(_with='user')
