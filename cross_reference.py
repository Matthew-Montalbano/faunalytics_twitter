import json
import pandas as pd
import re
from selenium import webdriver

SOURCE = "C:/Users/mmatt/Desktop/all_data/all_csv"
DRIVER = webdriver.PhantomJS()

def find_all_banned(data):
    banned = []
    for screen_name in data['screen_name']:
        user_info = scrape_shadowban(screen_name)
        print('checking if {} is banned'.format(screen_name))
        if determine_ban(user_info):
            print('         {} is banned'.format(screen_name))
            banned.append(screen_name)
    return banned

def scrape_shadowban(user):
    DRIVER.get('https://shadowban.eu/.api/{0}'.format(user))
    return get_json_data(DRIVER.page_source)


def get_json_data(html):
    regex = '>({.*})<'
    match = re.search(regex, html)
    return json.loads(match[1])

def determine_ban(user_info):
    ban = False
    try:
        if user_info['profile']['exists']:
            if not user_info['profile']['protected']:
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

def create_new_csv(array):
    series = pd.Series(array)
    series.to_csv('new_test_jan_ban.csv')

if __name__ == "__main__":
    data = pd.read_csv("{0}/new_test_jan.csv".format(SOURCE))
    banned_users = find_all_banned(data)
    create_new_csv(banned_users)
