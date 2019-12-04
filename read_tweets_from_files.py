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


if __name__ == "__main__":
    #PKL_FILES = os.listdir("temp_data/all_data_2019-05-16")
    PKL_FILES = os.listdir("../data")

    ids = []
    txts = []
    uids = []
    favs = []
    rets = []
    times = []
    categories = []

    for pf in PKL_FILES:
        print("Processing", pf)
        category = get_file_category(pf)
        #with open('temp_data/all_data_2019-05-16/%s' % pf, 'rb') as f:
        #with open('temp_data/all_data_2019-05-16/tweets_clean_meat_2019-05-16_128.pkl', 'rb') as f:
        with open("../data/%s" % pf, 'rb') as f:
            raw_data = pkl.load(f)

        for x in raw_data:
            ids += [x['id']]
            txts += [get_tweet_text(x)]
            uids += [x['user']['id']]
            favs += [x['favorite_count']]
            rets += [x['retweet_count']]
            times += [x['created_at']]
            categories += [category]

    clean_data = pd.DataFrame({'id': ids,
                               'text': txts,
                               'user_id': uids,
                               'favorite_count': favs,
                               'retweet_count': rets,
                               'date_time': times,
                               'category': categories
                               })

    print(clean_data)
    clean_data.to_csv("test123.csv", index=False, encoding='utf-8')
