#Wrapper for twitter api
from twitter import *

def toListOfTweets(tweets):
    result = []
    rawTweets = tweets['statuses']
    for rawTweet in rawTweets:
        result.append(Tweet(rawTweet))
    return result

def toPlainTweet(rawTweet):
    return Tweet(rawTweet)

def boolToInt(bool_):
    if (bool_):
        return 1
    else:
        return 0

class ApiStreaming(object):
    def __init__(self,
                    consumer_key,
                    consumer_secret,
                    access_token_key,
                    access_token_secret):
        self.twitter = TwitterStream( auth = OAuth(access_token_key, 
                                             access_token_secret,
                                             consumer_key,
                                             consumer_secret))
    
    def GetStream(self, track = None):
        iterTweets = self.twitter.statuses.filter(track = track)
        return iterTweets

class ApiSearch(object):
    
    def __init__(self,
                    consumer_key,
                    consumer_secret,
                    access_token_key,
                    access_token_secret):
        self.twitter = Twitter( auth = OAuth(access_token_key, 
                                             access_token_secret,
                                             consumer_key,
                                             consumer_secret))

    def GetSearch(self,
                    q = None,
                    #geocode = None,
                    #lang = None,
                    #locale = None,
                    #result_type = None,
                    count = None,
                    #until = None,
                    #since_id = None,
                    max_id = None,
                    #include_entities = None,
                    #callback = None
                    ):
        tweets = self.twitter.search.tweets(q = q,
                            #geocode = geocode,
                            #lang = lang,
                            #locale = locale,
                            #result_type = result_type,
                            count = count,
                            #until = until,
                            #since_id = since_id,
                            max_id = max_id,
                            #include_entities = include_entities,
                            #callback = callback
                            )

        tweetsList = toListOfTweets(tweets)
        return tweetsList

    def GetSearchRateLimit(self):
        limits = self.twitter.application.rate_limit_status()
        remaining = limits['resources']['search']['/search/tweets']['remaining']
        reset = limits['resources']['search']['/search/tweets']['reset']
        limit = limits['resources']['search']['/search/tweets']['limit']
        return [remaining, reset, limit]

class ApiSearchFuture(object):
    
    def __init__(self,
                    consumer_key,
                    consumer_secret,
                    access_token_key,
                    access_token_secret):
        self.twitter = Twitter( auth = OAuth(access_token_key, 
                                             access_token_secret,
                                             consumer_key,
                                             consumer_secret))
        
    def GetSearch(self,
                    q = None,
                    #geocode = None,
                    #lang = None,
                    #locale = None,
                    #result_type = None,
                    count = None,
                    #until = None,
                    since_id = None,
                    #max_id = None,
                    #include_entities = None,
                    #callback = None
                    ):
        tweets = self.twitter.search.tweets(q = q,
                            #geocode = geocode,
                            #lang = lang,
                            #locale = locale,
                            #result_type = result_type,
                            count = count,
                            #until = until,
                            since_id = since_id,
                            #max_id = max_id,
                            #include_entities = include_entities,
                            #callback = callback
                            )

        tweetsList = toListOfTweets(tweets)
        return tweetsList

    def GetSearchRateLimit(self):
        limits = self.twitter.application.rate_limit_status()
        remaining = limits['resources']['search']['/search/tweets']['remaining']
        reset = limits['resources']['search']['/search/tweets']['reset']
        limit = limits['resources']['search']['/search/tweets']['limit']
        return [remaining, reset, limit]
