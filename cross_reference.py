import json
import random
import re
import time
import pandas as pd
#import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

SOURCE = "C:/Users/mmatt/Desktop/all_data/all_csv"
options = Options()
options.headless = True
DRIVER = webdriver.Chrome(chrome_options=options)
DRIVER.implicitly_wait(5)


'''def find_all_banned(data):
    banned = []
    for screen_name in data['screen_name']:
        random_sleep()
        #user_info = scrape_shadowbaneu(screen_name)
        user_info = scrape_shadowbanio(screen_name)
        print('checking if {} is banned'.format(screen_name))
        if determine_ban(user_info):
            print('\t{} is banned'.format(screen_name))
            banned.append(screen_name)
    return banned'''

def cross_reference_users(data):
    approved = []
    banned = []
    try:
        for screen_name in data['screen_name']:
            random_sleep()
            if check_for_ban(screen_name):
                banned.append(screen_name)
            else:
                approved.append(screen_name)
    except KeyboardInterrupt:
        print('Writing to csv\'s and quitting...')
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
    user_info = scrape_shadowban_io(user)
    return user_info['data']['banned']

def scrape_shadowban_io(user):
    DRIVER.get('https://api.shadowban.io/api/v1/twitter/@{}'.format(user))
    return get_json_data(DRIVER.page_source)
    #res = requests.get('https://api.shadowban.io/api/v1/twitter/@{}'.format(user))
    #return json.loads(res.text)

def get_json_data(html):
    regex = '>({.*})<'
    match = re.search(regex, html)
    if match is None:
        return None
    return json.loads(match[1])

def check_shadowban_eu(user):
    user_info = scrape_shadowban_eu(user)
    return determine_ban_status(user_info)

def scrape_shadowban_eu(user):
    while True:
        DRIVER.get('https://shadowban.eu/.api/{0}'.format(user))
        user_data = get_json_data(DRIVER.page_source)
        if user_data is None or user_data['profile']['screen_name'].lower() != user.lower():
            print('\tcouldn\'t load user, sleeping for 3 seconds...')
            print(user_data)
            time.sleep(3)
        else:
            break
    return user_data

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
    approved.to_csv('{0}/approved.csv'.format(SOURCE), mode='a', header=False, index=False)
    banned.to_csv('{0}/banned.csv'.format(SOURCE), mode='a', header=False, index=False)

def drop_screen_names(data, names_list):
    print('Dropping known screen_names...')
    return data[~data['screen_name'].isin(names_list['screen_name'])]

if __name__ == "__main__":
    data = pd.read_csv("{0}/new_test_jan.csv".format(SOURCE))
    banned_list = pd.read_csv('{0}/banned.csv'.format(SOURCE))
    approved_list = pd.read_csv('{0}/approved.csv'.format(SOURCE))
    data = drop_screen_names(data, banned_list)
    data = drop_screen_names(data, approved_list)
    (approved_users, banned_users) = cross_reference_users(data.drop_duplicates(subset=['screen_name'],
                                                                                keep='first'))
    append_to_csvs(approved_users, banned_users)
