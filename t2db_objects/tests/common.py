#!/usr/bin/env python3
# Common functions

import random
import string

def randomInteger(maxSize):
    return random.randint(0, maxSize)

def randomIntegerRange(minSize, maxSize):
    return random.randint(minSize, maxSize)

def randomBoolean():
    if randomInteger(2) == 0:
        return False
    return True

def randomStringFixed(size = 10, chars = string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def randomStringVariable(maxSize, chars = string.ascii_uppercase + string.ascii_lowercase + string.digits):
    size = randomInteger(maxSize)
    return ''.join(random.choice(chars) for x in range(size))

def randomText(maxSizeText, maxSizeWord):
    text = ''
    size = randomIntegerRange(1, maxSizeText)
    while len(text) < size:
        word = randomStringVariable(maxSizeWord)
        text += word + ' '
    return text[0:size]

def randomUrl(base, extension):
    text = "http://"
    text += base
    text += "/"
    text += randomStringVariable(20)
    text += "."
    text += extension
    return text

def randomTweet(id_, created_at, user):
    randomTweet = {}
    randomTweet['id'] = id_
    randomTweet['created_at'] = created_at
    randomTweet['user'] = user
    # Non-mandatory
    randomTweet['retweet_count'] = randomInteger(100)
    randomTweet['text'] = randomText(200, 20)
    randomTweet['in_reply_to_screen_name'] = randomStringVariable(50)
    randomTweet['in_reply_to_user_id'] = randomInteger(100)
    randomTweet['in_reply_to_status_id'] = randomInteger(100)
    randomTweet['source'] = randomStringVariable(50)
    randomTweet['urls'] = randomUrl("twitter.com", "html")
    randomTweet['user_mentions'] = randomStringVariable(50)
    randomTweet['hashtags'] = randomText(100,10)
    randomTweet['geo'] = randomStringVariable(50)
    randomTweet['place'] = randomStringVariable(50)
    randomTweet['coordinates'] = randomStringFixed(10)
    randomTweet['contributors'] = randomStringVariable(50)
    randomTweet['favorited'] = randomBoolean()
    randomTweet['truncated'] = randomBoolean()
    randomTweet['retweeted'] = randomBoolean()
    return randomTweet

def randomUser(id_, created_at, name):
    randomUser = {}
    randomUser['id'] = id_
    randomUser['created_at'] = created_at
    randomUser['name'] = name
    # Non-mandatory
    randomUser['screen_name'] = randomStringVariable(200)
    randomUser['location'] = randomStringVariable(200)
    randomUser['description'] = randomText(200, 15)
    randomUser['profile_image_url'] = randomUrl("twitter.com", "jpg")
    randomUser['profile_image_url_https'] = randomUrl("twitter.com", "jpg")
    randomUser['profile_background_tile'] = randomBoolean()
    randomUser['profile_background_image_url'] = randomUrl("twitter.com", "jpg")
    randomUser['profile_background_color'] = randomStringFixed(6)
    randomUser['profile_sidebar_fill_color'] = randomStringFixed(6)
    randomUser['profile_sidebar_border_color'] = randomStringFixed(6)
    randomUser['profile_link_color'] = randomStringFixed(6)
    randomUser['profile_text_color'] = randomStringFixed(6)
    randomUser['protected'] = randomBoolean()
    randomUser['utc_offset'] = randomInteger(100)
    randomUser['time_zone'] = randomStringFixed(3)
    randomUser['followers_count'] = randomInteger(100)
    randomUser['friends_count'] = randomInteger(100)
    randomUser['statuses_count'] = randomInteger(100)
    randomUser['favourites_count'] = randomInteger(100)
    randomUser['url'] = randomUrl("usersite.com", ".html")
    randomUser['geo_enabled'] = randomBoolean()
    randomUser['verified'] = randomBoolean()
    randomUser['lang'] = randomStringFixed(2)
    randomUser['notifications'] = randomBoolean()
    randomUser['contributors_enabled'] = randomBoolean()
    randomUser['listed_count'] = randomInteger(100)
    return randomUser

def randomJob(command, process_id):
    randomJob = {}
    randomJob['command'] = command
    randomJob['process_id'] = process_id
    # Non-mandatory
    randomJob['consumer'] = randomStringFixed(100)
    randomJob['consumer_sec'] = randomStringFixed(100)
    randomJob['access'] = randomStringFixed(100)
    randomJob['access_sec'] = randomStringFixed(100)
    randomJob['query'] = randomText(100, 10)
    randomJob['kind'] = randomStringFixed(5)
    return randomJob

def randomTweetStreaming(tweet, streaming):
    randomTweetStreaming = {}
    randomTweetStreaming['tweet'] = tweet
    randomTweetStreaming['streaming'] = streaming
    return randomTweetStreaming

def randomTweetSearch(tweet, search):
    randomTweetSearch = {}
    randomTweetSearch['tweet'] = tweet
    randomTweetSearch['search'] = search
    return randomTweetSearch

def randomStreaming(id_):
    randomStreaming = {}
    randomStreaming["id"] = id_
    randomStreaming["query"] = randomText(100, 10)
    randomStreaming['consumer'] = randomStringFixed(100)
    randomStreaming['consumer_secret'] = randomStringFixed(100)
    randomStreaming['access'] = randomStringFixed(100)
    randomStreaming['access_secret'] = randomStringFixed(100)
    return randomStreaming

def randomSearch(id_):
    randomSearch = {}
    randomSearch["id"] = id_
    randomSearch["query"] = randomText(100, 10)
    randomSearch['consumer'] = randomStringFixed(100)
    randomSearch['consumer_secret'] = randomStringFixed(100)
    randomSearch['access'] = randomStringFixed(100)
    randomSearch['access_secret'] = randomStringFixed(100)
    return randomSearch
