
# coding: utf-8

import os
import json
import pandas as pd
import soundfile as sf


BASE_PATH = os.getcwd()
data_path = os.path.join(BASE_PATH, 'primewords_md_2018_set1')


with open(os.path.join(data_path, 'set1_transcript.json'),'r') as f:
    a = json.loads(f.readlines()[0])

data = pd.DataFrame(a)

new_data = data.drop_duplicates()

new_data.to_csv(os.path.join(BASE_PATH, "primewords_md_2018_set1.csv"))
