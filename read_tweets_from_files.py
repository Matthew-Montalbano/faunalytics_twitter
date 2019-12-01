import os
import pandas as pd
import pickle as pkl

pkl_files = os.listdir("temp_data/all_data_2019-05-16")

ids = []
txts = []
uids = []
favs = []
rets = []
times = []

for pf in pkl_files:
    print("Processing", pf)
    with open('temp_data/all_data_2019-05-16/%s' % pf, 'rb') as f:
    #with open('temp_data/all_data_2019-05-16/tweets_clean_meat_2019-05-16_128.pkl', 'rb') as f:
        raw_data = pkl.load(f)

    for x in raw_data:
        # print(x)
        ids += [x['id']]
        txts += [x['full_text']]
        uids += [x['user']['id']]
        favs += [x['favorite_count']]
        rets += [x['retweet_count']]
        times += [x['created_at']]

clean_data = pd.DataFrame({'id': ids,
                           'text': txts,
                           'user_id': uids,
                           'favorite_count': favs,
                           'retweet_count': rets,
                           'date_time': times
                           })

print(clean_data)

clean_data.to_csv("test123.csv", index=False, encoding='utf-8')
