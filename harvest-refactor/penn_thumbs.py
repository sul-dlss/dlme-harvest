import pandas as pd

def get_thumb(df):
    id = df['emuIRN']
    df['thumbnail'] = "https://upmaa-pennmuseum.netdna-ssl.com/collections/assets/center/{}.jpg".format(id)
    return df

# Read Egyptian data in incoming format and add thumbnail column
df = pd.read_csv('https://raw.githubusercontent.com/sul-dlss/dlme-metadata/master/penn/egyptian-museum/data/egyptian-20181028.csv', header=0)
df = df.apply(get_thumb, axis=1)
df.to_csv('../output/egyptian-20181028.csv')

# Read Near Eastern data in incoming format and add thumbnail column
df = pd.read_csv('https://raw.githubusercontent.com/sul-dlss/dlme-metadata/master/penn/near-eastern/data/near%20eastern-20181028.csv', header=0)
df = df.apply(get_thumb, axis=1)
df.to_csv('../output/near-eastern-20181028.csv')
