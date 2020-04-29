import glob
import json
import random
import re
import time
import sys
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

SOURCE = "C:/Users/mmatt/Desktop/all_data/all_csv"
OPTIONS = Options()
OPTIONS.headless = True
DRIVER = webdriver.Chrome(chrome_options=OPTIONS)
DRIVER.implicitly_wait(5)

def cross_reference_all_files():
    all_csv_files = glob.glob('{0}/*.csv'.format(SOURCE))
    for csv in all_csv_files:
        print('cross referencing {0}'.format(csv))
        cross_reference_file(csv)

def cross_reference_file(filepath):
    data, banned_names, approved_names = read_in_csvs(filepath)
    data = clean_data(data, approved_names, banned_names)
    (approved_users, banned_users) = cross_reference_users(data)
    append_to_csvs(approved_users, banned_users)

def read_in_csvs(filepath):
    data = pd.read_csv(filepath)
    banned_list = pd.read_csv('{0}/list_of_names/banned.csv'.format(SOURCE))
    approved_list = pd.read_csv('{0}/list_of_names/approved.csv'.format(SOURCE))
    return data, banned_list, approved_list

def clean_data(data, approved_list, banned_list):
    data = data.drop_duplicates(subset=['text'], keep='first')
    data = drop_screen_names(data, banned_list)
    data = drop_screen_names(data, approved_list)
    data = data.drop_duplicates(subset=['screen_name'], keep='first')
    print("{0} names to check...".format(data['screen_name'].size))
    return data

def drop_screen_names(data, names_list):
    print('Dropping known screen_names...')
    return data[~data['screen_name'].isin(names_list['screen_name'])]

def cross_reference_users(data):
    approved = []
    banned = []
    num_users_checked = 1
    try:
        for screen_name in data['screen_name']:
            random_sleep()
            if check_for_ban(screen_name):
                banned.append(screen_name)
            else:
                approved.append(screen_name)
            if num_users_checked % 500 == 0:
                append_to_csvs(approved, banned)
                print('\nappending 500 names to csvs...\n')
                approved = []
                banned = []
            num_users_checked += 1
    except KeyboardInterrupt:
        print('Writing to csv\'s and quitting...')
        append_to_csvs(approved, banned)
        sys.exit("Successfully quit")
    return (approved, banned)

def random_sleep():
    if random.random() < 0.05:
        print('sleeping for 3 seconds...')
        time.sleep(2)

def check_for_ban(user):
    is_banned = False
    print('checking if {} is banned'.format(user))
    if check_shadowban_io(user):
        print('\tmaking further tests for {}'.format(user))
        if check_shadowban_eu(user):
            print('\t{} is banned'.format(user))
            is_banned = True
    return is_banned

def check_shadowban_io(user):
    while True:
        try:
            user_info = scrape_shadowban_io(user)
            return user_info['data']['banned']
        except KeyError:
            if "error" in user_info:
                return False
            print('\tcouldn\'t check user, sleeping for 3 seconds...')
            time.sleep(3)

def scrape_shadowban_io(user):
    DRIVER.get('https://api.shadowban.io/api/v1/twitter/@{}'.format(user))
    return get_json_data(DRIVER.page_source)

def get_json_data(html):
    regex = '>({.*})<'
    match = re.search(regex, html)
    if match is None:
        return None
    return json.loads(match[1])

def check_shadowban_eu(user):
    while True:
        user_info = scrape_shadowban_eu(user)
        if user_info is None or user_info['profile']['screen_name'].lower() != user.lower():
            print('\tcouldn\'t check user, sleeping for 3 seconds...')
            time.sleep(3)
        else:
            return determine_ban_status(user_info)

def scrape_shadowban_eu(user):
    DRIVER.get('https://shadowban.eu/.api/{0}'.format(user))
    return get_json_data(DRIVER.page_source)

def determine_ban_status(user_info):
    ban = False
    try:
        if user_info['profile']['exists'] and not user_info['profile']['protected']:
            tests = user_info['tests']
            if ban_requirements(tests):
                ban = True
    except KeyError:
        ban = True
    return ban

def ban_requirements(tests):
    return tests['ghost'] is None or tests['ghost']['ban'] or (tests['more_replies'] == "ENOREPLIES"
                                                               and not tests['typeahead']
                                                               and tests['search'] == False
                                                               )

def append_to_csvs(approved_array, banned_array):
    approved = pd.DataFrame(approved_array)
    banned = pd.DataFrame(banned_array)
    approved.to_csv('{0}/list_of_names/approved.csv'.format(SOURCE), mode='a', header=False, index=False)
    banned.to_csv('{0}/list_of_names/banned.csv'.format(SOURCE), mode='a', header=False, index=False)

if __name__ == "__main__":
    cross_reference_all_files()
