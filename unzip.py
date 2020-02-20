import os
import zipfile

NUM_MONTHS = 12
NUM_DAYS = 31
SOURCE = "C:/Users/mmatt/Desktop/all_data"

def extract_every_month():
    for month in range(1, NUM_MONTHS + 1):
        extract_every_day(twodig(month))

def extract_every_day(month):
    for day in range(1, NUM_DAYS + 1):
        day = twodig(day)
        try:
            extract_zip(month, day)

        except FileNotFoundError:
            print("couldn't find all_data_2019-{0}-{1}.zip".format(month, day))

def extract_zip(month, day):
    zip_ref = zipfile.ZipFile("{0}/all_data_2019-{1}-{2}.zip".format(SOURCE, month, day), 'r')
    zip_ref.extractall("{0}/all_pkl/".format(SOURCE))
    print("extracted all_data_2019-{0}-{1}.zip".format(month, day))
    zip_ref.close()

    os.rename("{0}/all_pkl/data/all_data_2019-{1}-{2}".format(SOURCE, month, day),
              "{0}/all_pkl/all_data_2019-{1}-{2}".format(SOURCE, month, day))

    os.remove("{0}/all_data_2019-{1}-{2}.zip".format(SOURCE, month, day))
    print("     removed all_data_2019-{0}-{1}.zip".format(month, day))
    # os.remove("C:/Users/mmatt/Desktop/all_data/all_pkl/data")

def twodig(x):
    if x >= 10:
        return str(x)

    return "0" + str(x)

if __name__ == "__main__":
    extract_every_month()
