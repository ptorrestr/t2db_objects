#TODO Get automatically data model from webservice

#List to store TweetSearch or TweetStreaming objects
class TweetElementList(object):
    def __init__(self):
        self.list = []

    def append(self, element):
        self.list.append(element)

    def toHash():
        hashList = []
        for element in self.list:
            hashList.append(element.toHash())
        return hashList

class Tweet(object):
    def __init__(self, rawTweet): 
        self.id = rawTweet['id']
        self.created_at = rawTweet['created_at']
        self.favorited = boolToInt(rawTweet['favorited'])
        self.text = rawTweet['text']
        self.in_reply_to_screen_name = rawTweet['in_reply_to_screen_name']
        self.in_reply_to_user_id = rawTweet['in_reply_to_user_id']
        self.in_reply_to_status_id = rawTweet['in_reply_to_status_id']
        self.truncated = boolToInt(rawTweet['truncated'])
        self.source = rawTweet['source']
        self.urls = rawTweet['entities']['urls']
        self.user_mentions = rawTweet['entities']['user_mentions']
        self.hashtags = rawTweet['entities']['hashtags']
        self.geo = rawTweet['geo']
        self.place = rawTweet['place']
        self.coordinates = rawTweet['coordinates']
        self.contributors = rawTweet['contributors']
        self.retweeted = boolToInt(rawTweet['retweeted'])
        self.retweet_count = rawTweet['retweet_count']
        self.user = User(rawTweet['user'])
        self.tweetSearch = searchList
        self.tweetStreaming = streamingList

    def toHash(self):
        args = {}
        args['id'] = self.id 
        args['created_at'] = self.created_at
        args['favorited'] = self.favorited
        args['text'] = self.text
        args['in_reply_to_screen_name'] = self.in_reply_to_screen_name
        args['in_reply_to_user_id'] = self.in_reply_to_user_id
        args['in_reply_to_status_id'] = self.in_reply_to_status_id
        args['truncated'] = self.truncated
        args['source'] = self.source
        args['urls'] = self.urls
        args['user_mentions'] = self.user_mentions 
        args['hashtags'] = self.hashtags
        args['geo'] = self.geo
        args['place'] = self.place
        args['coordinates'] = self.coordinates
        args['contributors'] = self.contributors
        args['retweeted'] = self.retweeted
        args['retweet_count'] = self.retweet_count
        args['user'] = self.user.id
        return args

class Entities(object):
    def __init__(self, rawEntities):
        self.urls = rawEntities['urls']
        self.hashtags = rawEntities['hashtags']
        self.user_mentions = rawEntities['user_mentions']

class Metadata(object):
    def __init__(self, rawMetadata):
        self.iso_language_code = rawMetadata['iso_language_code']
        self.result_type = rawMetadata['result_type']

class User(object):
    def __init__(self, rawUser):
        self.id = rawUser['id']
        self.created_at = rawUser['created_at']
        self.name = rawUser['name']
        self.screen_name = rawUser['screen_name']
        self.location = rawUser['location']
        self.description = rawUser['description']
        self.profile_image_url = rawUser['profile_image_url']
        self.profile_image_url_https = rawUser['profile_image_url_https']
        self.profile_background_tile = rawUser['profile_background_tile']
        self.profile_background_image_url = rawUser['profile_background_image_url']
        self.profile_background_color = rawUser['profile_background_color']
        self.profile_sidebar_fill_color = rawUser['profile_sidebar_fill_color']
        self.profile_sidebar_border_color = rawUser['profile_sidebar_border_color']
        self.profile_link_color = rawUser['profile_link_color']
        self.profile_text_color = rawUser['profile_text_color']
        self.protected = rawUser['protected']
        self.utc_offset = rawUser['utc_offset']
        self.time_zone = rawUser['time_zone']
        self.followers_count = rawUser['followers_count']
        self.friends_count = rawUser['friends_count']
        self.statuses_count = rawUser['statuses_count']
        self.favourites_count = rawUser['favourites_count']
        self.url = rawUser['url']
        self.geo_enabled = rawUser['geo_enabled']
        self.verified = rawUser['verified']
        self.lang = rawUser['lang']
        self.notifications = rawUser['notifications']
        self.contributors_enabled = rawUser['contributors_enabled']
        self.listed_count = rawUser['listed_count']

    def toHash(self):
        args = {}
        args['id'] = self.id
        args['created_at'] = self.created_at
        args['name'] = self.name
        args['screen_name'] = self.screen_name
        args['location'] = self.location
        args['description'] = self.description
        args['profile_image_url'] = self.profile_image_url
        args['profile_image_url_https'] = self.profile_image_url_https
        args['profile_background_tile'] = boolToInt(self.profile_background_tile)
        args['profile_background_image_url'] = self.profile_background_image_url
        args['profile_background_color'] = self.profile_background_color
        args['profile_sidebar_fill_color'] = self.profile_sidebar_fill_color
        args['profile_sidebar_border_color'] = self.profile_sidebar_border_color
        args['profile_link_color'] = self.profile_link_color
        args['profile_text_color'] = self.profile_text_color
        args['protected'] = boolToInt(self.protected)
        args['utc_offset'] = self.utc_offset
        args['time_zone'] = self.time_zone
        args['followers_count'] = self.followers_count
        args['friends_count'] = self.friends_count
        args['statuses_count'] = self.statuses_count
        args['favourites_count'] = self.favourites_count
        args['url'] = self.url
        args['geo_enabled'] = boolToInt(self.geo_enabled)
        args['verified'] = boolToInt(self.verified)
        args['lang'] = self.lang
        args['notifications'] = boolToInt(self.notifications)
        args['contributors_enabled'] = boolToInt(self.contributors_enabled)
        args['listed_count'] = self.listed_count
        return args
