# to do:
# Automatically search for terms without spaces as well!

# import numpy as np
# pip install python-twitter
# import twitter
import tweepy
# import csv
import datetime
# import jsonpickle
import pickle
import re
import sys

consumer_key = "PDZPPLGUu5ySTrR5viqi2l9mN"
consumer_secret = "9VOIBWCGl7Y7sJ6hXaP5QY9j7wKYBMo9NzK8Fun29IIpRc1Xbo"
access_token = "796525448301780992-ef1dlKykooXAaiD9RWQS87FdqK8cMnF"
access_token_secret = "tXT82ibd014C9xfUk7kBaIcZdBzm8D7cf999rD2gISl3L"

max_tweets = 1000000


def download_twitter_search(search_terms, search_group, offset):

    # https://gist.github.com/vickyqian/f70e9ab3910c7c290d9d715491cde44c
    #  Good info!:
    # http://www.dealingdata.net/2016/07/23/PoGo-Series-Tweepy/

    # auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)

    # api = tweepy.API(auth,wait_on_rate_limit=True)

    # Switching to application authentication
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

    # Setting up new api wrapper, using authentication only
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # Error handling
    if (not api):
        print("Problem Connecting to API")

    start_date = (datetime.datetime.today() + datetime.timedelta(days=-offset)).strftime('%Y-%m-%d')
    end_date = (datetime.datetime.today() + datetime.timedelta(days=(-offset + 1))).strftime('%Y-%m-%d')

    # Open/Create a file to append data
    # csvFile = open('test_vegan.csv', 'a')
    # Use csv Writer
    # csvWriter = csv.writer(csvFile)
    # json_file = open('test_vegan_%s.json'%start_date, 'w')

    print(start_date)
    print(end_date)

    print(api.rate_limit_status()['resources']['search'])

    search_query = ""
    for term in search_terms:
        if len(search_query) > 0:
            search_query += ' OR '
        # search_query += '"' + term + '"'
        search_query += '"{0}"'.format(term)
        if re.search(' ', term):
            # search_query += ' OR "' + re.sub(' ', '', term) + '"'
            search_query += ' OR "{0}"'.format(re.sub(' ', '', term))

    print(search_query)

    # cursor version
    # tweets = tweepy.Cursor(api.search,q=search_query,count=100,
    #                                                   lang="en",
    #                                                   since=start_date,
    #                           until=end_date,tweet_mode = "extended").items(max_tweets)

    output_dict = []

    max_id = -1
    tweet_count = 0
    # page = 1
    while tweet_count < max_tweets:
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
                # print (tweet._json['created_at'])
                output_dict += [tweet._json]
                tweet_count += 1
                # csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])

                if tweet_count > 0 and tweet_count % 10000 == 0:
                    with open('../data/tweets_%s_%s_%d.pkl' % (search_group, start_date, tweet_count), 'wb') as handle:
                        pickle.dump(output_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    print('Written %d tweets.' % tweet_count)
                    print(tweet._json['created_at'])
                    print(tweets[-1].id)
                    output_dict = []

            max_id = tweets[-1].id
        else:
            break

    with open('../data/tweets_%s_%s_%d.pkl' % (search_group, start_date,tweet_count), 'wb') as handle:
            pickle.dump(output_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print('Written %d tweets.' % tweet_count)

    print("Downloaded {0} tweets".format(tweet_count))


search_terms_lists = {
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


if len(sys.argv) == 1:
    offset = 2
else:
    offset = int(sys.argv[1])

# Pick list of terms to search.
for group in search_terms_lists.keys():
# for group in ['other']:
    print(group)
    download_twitter_search(search_terms_lists[group], group, offset)
