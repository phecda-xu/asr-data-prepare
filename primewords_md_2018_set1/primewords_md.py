
# coding: utf-8

import os
import json
import pandas as pd
import soundfile as sf


BASE_PATH = os.getcwd()

data_path = os.path.join(BASE_PATH, 'primewords_md_2018_set1')

with open(os.path.join(data_path, 'set1_transcript.json'), 'r') as f:
    a = json.loads(f.readlines()[0])

data = pd.DataFrame(a)

new_data = data.drop_duplicates()
new_data = new_data.rename(columns={"file": "wav", "length":"durations", "text": "txt"})

new_data["wav_path"] = new_data.wav.apply(lambda x: "primewords_md_2018_set1/primewords_md_2018_set1/wav/{}".format(x))

total_hour = round(sum([float(i) for i in list(new_data.durations)])/3600.0, 3)
total_wav_num = len(new_data.wav)

print('total num of files is {} and total hours is {}h'.format(total_wav_num, total_hour))

new_data.to_csv(os.path.join(BASE_PATH, "primewords_md_2018_set1.csv"), index=False)