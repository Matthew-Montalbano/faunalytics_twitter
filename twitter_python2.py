import twitter_python
import sys

SEARCH_TERMS_LISTS = {
    'diet':
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
    'advocacy':
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
    'covid':
    [
        "covid",
        "covid-19",
        "covid19",
        "cov19",
        "sarscov2",
        "sars-cov-2",
        "coronavirus",
        "pandemic",
        "epidemic",
        "wet market",
        "open market",
        "live market"
    ]
}

if __name__ == "__main__":
    if len(sys.argv) == 1:
        OFFSET = 2
    else:
        OFFSET = int(sys.argv[1])

    # Pick list of terms to search.
    for group in SEARCH_TERMS_LISTS:
        print(group)
        twitter_python.download_twitter_search(SEARCH_TERMS_LISTS[group], group, OFFSET)
