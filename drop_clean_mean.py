import glob
import pandas as pd
import re

SOURCE = "F:/Users/mmatt_000/Faunalytics/all_data/all_csv/cleaned_csv"

def clean_all_files():
    all_csv_files = glob.glob('{0}/*.csv'.format(SOURCE))
    for csv in all_csv_files:
        clean_file(csv)


def clean_file(file):
    filename = re.findall(r'all_data_\d+-\d+-\d+\.csv', file)[0]
    print('cleaning {0}'.format(filename))
    data = pd.read_csv(file)
    cleaned_data = clean_data(data)
    cleaned_data.to_csv("{0}/{1}".format(SOURCE, filename), index=False)
    print('\twrote cleaned data to csv')


def clean_data(data):
    clean_meat_data = data[data['category'] == 'clean_meat']
    data_contains_clean_mean = clean_meat_data['text'].str.contains('clean mean', regex=False)
    clean_mean_indexes = clean_meat_data[data_contains_clean_mean].index
    return data.drop(clean_mean_indexes)

clean_all_files()