import pandas as pd
import urllib.request
import re

df = pd.read_csv('/Users/jtim/Dropbox/DLSS/DLME/dlme-harvest/output/near-eastern-20181028.csv')

def get_image_url(df):
    try:
        irn = df['emuIRN']
        url = 'https://www.penn.museum/collections/object_images.php?irn={}'.format(irn)
        response = urllib.request.urlopen(url)
        html = response.read().decode('utf-8')
        image_url_pattern = re.compile(r'"https://upmaa-pennmuseum.netdna-ssl.com/collections/assets/.*?\"')
        image_url = re.findall(image_url_pattern, html)[0]
        df['image_url'] = image_url.replace('"', '')
    except:
        print('timeout')
    return df

df = df.apply(get_image_url, axis=1)
df.to_csv('/Users/jtim/Dropbox/DLSS/DLME/dlme-harvest/output/egyptian-20181028-cleaned.csv')
