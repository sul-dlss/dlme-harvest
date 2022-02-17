import yaml
import pandas as pd
import numpy as np

df = pd.read_csv('periodo-dataset.csv')

values = {}

for i in df['label'].unique():
    values.update({i: []})
    # if label matches i, get periods and append to values dictionary
    values[i].extend(df.loc[df['label'] == i, 'period'].to_list())

with open ('output/periodo.yaml', 'w') as out:
    out.write(yaml.dump(values))
