import os
import re
import pickle as pkl
import pandas as pd

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
    #PKL_FILES = os.listdir("temp_data/all_data_2019-05-16")
    PKL_FILES = os.listdir("C:/Users/mmatt/Desktop/data/all_data_2020-01-20")

    screen_names = []
    # ids = []
    txts = []
    # uids = []
    favs = []
    rets = []
    times = []
    categories = []

    for pf in PKL_FILES:
        print("Processing", pf)
        category = get_file_category(pf)
        #with open('temp_data/all_data_2019-05-16/%s' % pf, 'rb') as f:
        #with open('temp_data/all_data_2019-05-16/tweets_clean_meat_2019-05-16_128.pkl', 'rb') as f:
        with open("C:/Users/mmatt/Desktop/data/all_data_2020-01-20/%s" % pf, 'rb') as f:
            raw_data = pkl.load(f)

        for x in raw_data:
            screen_names += [x['user']['screen_name']]
            # ids += [x['id']]
            txts += [get_tweet_text(x)]
            # uids += [x['user']['id']]
            favs += [x['favorite_count']]
            rets += [x['retweet_count']]
            times += [shorten_time(x['created_at'])]
            categories += [category]

    clean_data = pd.DataFrame({'screen_name': screen_names,
                                # 'id': ids,
                               'text': txts,
                               # 'user_id': uids,
                               'favorite_count': favs,
                               'retweet_count': rets,
                               'date_time': times,
                               'category': categories
                               })

    # print(clean_data)
    clean_data.to_csv("new_test_jan.csv", index=False, encoding='utf-8')
