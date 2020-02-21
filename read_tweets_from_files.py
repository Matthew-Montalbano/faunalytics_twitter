import os
import re
import pickle as pkl
import pandas as pd

SOURCE = 'C:/Users/mmatt/Desktop/all_data/'

def read_all_tweets():
    for foldername in os.listdir('{0}/all_pkl'.format(SOURCE)):
        print('reading from', foldername)
        read_tweets_from_folder(foldername)

def read_tweets_from_folder(foldername):
    pkl_files = os.listdir('{0}/all_pkl/{1}'.format(SOURCE, foldername))
    data = {'screen_names': [],
            'txts': [],
            'favs': [],
            'rets': [],
            'times': [],
            'categories': []
            }

    for pkl_file in pkl_files:
        print("Processing", pkl_file)
        with open('{0}/all_pkl/{1}/{2}'.format(SOURCE, foldername, pkl_file), 'rb') as f:
            raw_data = pkl.load(f)
        populate_row_dictionary(raw_data, data, get_file_category(pkl_file))

    clean_data = pd.DataFrame({'screen_name': data['screen_names'],
                               'text': data['txts'],
                               'favorite_count': data['favs'],
                               'retweet_count': data['rets'],
                               'date_time': data['times'],
                               'category': data['categories']
                               })

    # print(clean_data)
    clean_data.to_csv("{0}/all_csv/{1}.csv".format(SOURCE, foldername), index=False, encoding='utf-8')

def populate_row_dictionary(data, row_dict, category):
    for info in data:
        row_dict['screen_names'] += [info['user']['screen_name']]
        row_dict['txts'] += [get_tweet_text(info)]
        row_dict['favs'] += [info['favorite_count']]
        row_dict['rets'] += [info['retweet_count']]
        row_dict['times'] += [shorten_time(info['created_at'])]
        row_dict['categories'] += [category]

def get_file_category(filename):
    match = re.search(r'tweets_(\w*-?\w*)_', filename)
    return match.group(1)


def get_tweet_text(data):
    try:
        text = 'RT @{0} {1}'.format(data['retweeted_status']['user']['screen_name'],
                                    data['retweeted_status']['full_text'])
    except KeyError:
        text = data['full_text']
    return text

def shorten_time(time):
    regex = r'(\w+ \w+ \d+ \d+:\d+):\d+ \+\d+ (\d+)'
    match = re.search(regex, time)
    return '{0} {1}'.format(match.group(1), match.group(2))


if __name__ == "__main__":
    read_all_tweets()
