# to do:
# Automatically search for terms without spaces as well!

# import numpy as np
import datetime
import pickle
import re
import sys
import tweepy
# import csv
# import jsonpickle

'''
Paul's keys:
CONSUMER_KEY = "PDZPPLGUu5ySTrR5viqi2l9mN"
CONSUMER_SECRET = "9VOIBWCGl7Y7sJ6hXaP5QY9j7wKYBMo9NzK8Fun29IIpRc1Xbo"
ACCESS_TOKEN = "796525448301780992-ef1dlKykooXAaiD9RWQS87FdqK8cMnF"
ACCESS_TOKEN_SECRET = "tXT82ibd014C9xfUk7kBaIcZdBzm8D7cf999rD2gISl3L"
'''

SEARCH_TERMS_LISTS = {
    'vegan':
    [
        "vegan",
        "vegetarian",
        "reducetarian",
        "flexitarian",
        "pescatarian",
        "meatless monday",
        "veganuary",
        "plant-based",
        "plant based"
    ],
    'clean_meat':
    [
        "clean mean",
        "cultured meat",
        "cell-based meat",
        "cell based meat"
        "in vitro meat",
        "slaughter-free meat",
        "slaughter free meat"
        "artificial meat",
        "lab meat",
        "lab grown meat"
    ],
    'cage-free':
    [
        "cage free",
        "cage-free",
        "free range",
        "gestation crate",
        "animal welfare",
        "factory farm",
        "intensive agriculture",
        "live export"
    ],
    'eaa':
    [
        "effective animal advocacy",
        "animal advocacy",
        "animal rights",
        "animal welfare",
        "animal activism",
        "animal liberation",
        "effective altruism",
        "effective advocacy",
        "animal protection"
    ],
    'other':
    [
        "animal testing",
        "clean eating",
        "cruelty free",
        "dash diet",
        "fitness",
        "humane",
        "keto",
        "kosher",
        "gluten free",
        "gmo",
        "macros",
        "mediterranean diet",
        "non gmo",
        "organic",
        "paleo",
        "weight loss",
        "whole 30",
        "whole thirty"
    ]
}

CONSUMER_KEY = "4L3PcDJIZR1TTD9J6TRnlqFxH"
CONSUMER_SECRET = "39GEwYjAcGdcfJqM3S64Jqh5iHfnM1MEuwS7fWOS9zNzYesFmk"
ACCESS_TOKEN = "1201957817424457728-i8E1w5cHa1QhiWuYX1qgWzF6Glhrwa"
ACCESS_TOKEN_SECRET = "aTZhJwgxLwQvz6200WW63KAaKiucuOJOEcQU1w4MBLKrN"

MAX_TWEETS = 1000000

def download_twitter_search(search_terms, search_group, offset):
    api = get_twitter_api()
    start_date, end_date = get_start_and_end_dates(offset)
    print(api.rate_limit_status()['resources']['search'])
    search_query = build_search_query(search_terms)
    output_dict = []
    max_id = -1
    tweet_count = 0
    # page = 1
    while tweet_count < MAX_TWEETS:
        if max_id <= 0:
            tweets = api.search(q=search_query,
                                count=100,
                                lang="en",
                                since=start_date,
                                until=end_date,
                                tweet_mode="extended")
        else:
            tweets = api.search(q=search_query,
                                count=100,
                                lang="en",
                                since=start_date,
                                until=end_date,
                                tweet_mode="extended",
                                max_id=str(max_id - 1))

        if tweets:
            for tweet in tweets:
                output_dict += [tweet._json]
                tweet_count += 1
                if tweet_count > 0 and tweet_count % 10000 == 0:
                    create_pkl_file(search_group, start_date, tweet_count, output_dict)
                    print(tweet._json['created_at'])
                    print(tweets[-1].id)
                    output_dict = []

            max_id = tweets[-1].id
        else:
            break

    create_pkl_file(search_group, start_date, tweet_count, output_dict)
    print("Downloaded {0} tweets".format(tweet_count))


def get_twitter_api():
    # https://gist.github.com/vickyqian/f70e9ab3910c7c290d9d715491cde44c
    #  Good info!:
    # http://www.dealingdata.net/2016/07/23/PoGo-Series-Tweepy/

    # auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    # auth.set_ACCESS_TOKEN(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # api = tweepy.API(auth,wait_on_rate_limit=True)

    auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    if not api:
        print("Problem Connecting to API")
    return api


def get_start_and_end_dates(offset):
    start_date = (datetime.datetime.today() + datetime.timedelta(days=-offset)).strftime('%Y-%m-%d')
    end_date = (datetime.datetime.today() + datetime.timedelta(days=(-offset + 1))).strftime('%Y-%m-%d')
    print(start_date)
    print(end_date)
    return start_date, end_date


def build_search_query(search_terms):
    search_query = ""
    for term in search_terms:
        if len(search_query) > 0:
            search_query += ' OR '
        search_query += '"{0}"'.format(term)
        if re.search(' ', term):
            search_query += ' OR "{0}"'.format(re.sub(' ', '', term))
    print(search_query)
    return search_query


def create_pkl_file(search_group, start_date, tweet_count, output):
    file_name = "../data/tweets_{0}_{1}_{2}.pkl".format(search_group, start_date, tweet_count)
    with open(file_name, 'wb') as handle:
        pickle.dump(output, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print('Written %d tweets.' % tweet_count)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        OFFSET = 2
    else:
        OFFSET = int(sys.argv[1])

    # Pick list of terms to search.
    for group in SEARCH_TERMS_LISTS:
    # for group in ['other']:
        print(group)
        download_twitter_search(SEARCH_TERMS_LISTS[group], group, OFFSET)
