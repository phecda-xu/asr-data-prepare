
# coding: utf-8

import os
import pandas as pd
import soundfile as sf


BASE_PATH = os.getcwd()

data_path = os.path.join(BASE_PATH, 'data_aishell')

def read_text(file_path):
    with open(file_path, 'r') as f:
        text = f.readlines()
    return text

wav_list = []
set_list = []
path_list = []
duration_list = []
for data_set in os.listdir(os.path.join(data_path, 'wav')):
    for person in os.listdir(os.path.join(data_path, 'wav/{}'.format(data_set))):
        for wav in os.listdir(os.path.join(data_path, 'wav/{}/{}'.format(data_set, person))):
            wav_list.append(wav)
            set_list.append(data_set)
            path_list.append('{}/wav/{}/{}/{}'.format('aishell_1/data_aishell',data_set, person, wav))
            sig,sr = sf.read(os.path.join(data_path, 'wav/{}/{}/{}'.format(data_set,person, wav)))
            duration_list.append(round(float(len(sig))/float(sr), 3))

data = pd.DataFrame()

data["wav"] = wav_list
data["wav_path"] = path_list
data["durations"] = duration_list
data["data_set"] = set_list

data = data.sort_values(by='wav')

text = read_text(os.path.join(data_path, "transcript/aishell_transcript_v0.8.txt"))

wav_name_list = []
text_list = []
for i in sorted(text):
    wav_name = i[:16]
    wav_name_list.append(wav_name)
    txt = i[16:].strip('\n').replace(" ", '')
    text_list.append(txt)

data['txt'] = text_list[:len(data.wav)]

print('total num of wav is {}'.format(len(data.wav)))
print('total durations is {}h'.format(round(sum(data.durations)/3600.0, 3)))

data.to_csv('{}/aishell_1.csv'.format(BASE_PATH), index=False)
