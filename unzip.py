import os
import zipfile

def twodig(x):
    if x >= 10:
        return(str(x))
    else:
        return("0" + str(x))

for day in range(11,20):
    
    print(day)

    zip_ref = zipfile.ZipFile("temp_data/all_data_2019-02-%s.zip"%twodig(day), 'r')
    zip_ref.extractall("temp_data/")
    zip_ref.close()

    files = os.listdir("temp_data/data/all_data_2019-02-%s"%twodig(day))
    for f in files:
        os.rename("temp_data/data/all_data_2019-02-%s/%s"%(twodig(day),f), "temp_data/%s"%f)

    os.remove("temp_data/all_data_2019-02-%s.zip"%twodig(day))
