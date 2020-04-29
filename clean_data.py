import glob
import pandas as pd
import re

SOURCE = "F:/Users/mmatt_000/Faunalytics/all_data/all_csv"
OTHER_SUBCATEGORIES = ['animal testing', 'cruelty free', 'humane']


def clean_all_files():
    all_csv_files = glob.glob('{0}/*.csv'.format(SOURCE))
    for csv in all_csv_files:
        clean_file(csv)

def clean_file(file):
    filename = re.findall(r'all_data_\d+-\d+-\d+\.csv', file)[0]
    print('cleaning {0}'.format(filename))
    data = pd.read_csv(file)
    cleaned_data = clean_data(data)
    cleaned_data.to_csv("{0}/cleaned_csv/{1}".format(SOURCE, filename), index=False)
    print('\twrote cleaned data to csv')


def clean_data(data):
    data = drop_subcategories_from_other(data)
    data = data.drop_duplicates(subset=['text'], keep='first')
    return data

def drop_subcategories_from_other(data):
    data_to_drop = get_data_to_drop(data)
    return data.drop(data_to_drop.index)

def get_data_to_drop(data):
    keep_data = pd.DataFrame()
    data_other = data[data['category'] == 'other']
    for category in OTHER_SUBCATEGORIES:
        found_data = data_other[data_other['text'].str.contains(category, regex=False)]
        keep_data = keep_data.append(found_data)
    return data_other[~data_other.index.isin(keep_data.index)]

if __name__ == "__main__":
    clean_all_files()
