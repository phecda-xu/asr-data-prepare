
# coding: utf-8


import os
import pandas as pd
import soundfile as sf
from pypinyin import lazy_pinyin

BASE_PATH = os.getcwd()

data_path = os.path.join(BASE_PATH, 'data_aishell')


def read_text(file_path):
    with open(file_path, 'r') as f:
        text = f.readlines()
    return text


def pinyin_cover(char):
    if 'zh' in char:
        char = char.replace("zh", "z")
    char = char.replace("z", "z-zh")
    if 'ch' in char:
        char = char.replace("ch", "c")
    char = char.replace("c", "c-ch")
    if 'sh' in char:
        char = char.replace("sh", "s")
    char = char.replace("s", "s-sh")
    if 'l' in char:
        char = char.replace("l", "n")
    if 'ing' in char:
        char = char.replace("ing", "in")
    char = char.replace("in", "in-ing")
    return char

text = read_text(os.path.join(data_path, "transcript/aishell_transcript_v0.8.txt"))

wav_name_list = []
text_list = []
pinyin_list = []
for i in sorted(text):
    wav_name = i[:16]
    wav_name_list.append(wav_name)
    txt = i[16:].strip('\n').replace(" ", '')
    text_list.append(txt)
    text_pinyin = ' '.join([pinyin_cover(i) for i in lazy_pinyin(txt, errors='ignore')])
    pinyin_list.append(text_pinyin)

wav_list = []
set_list = []
path_list = []
duration_list = []
for data_set in os.listdir(os.path.join(data_path, 'wav')):
    for person in os.listdir(os.path.join(data_path, 'wav/{}'.format(data_set))):
        for wav in os.listdir(os.path.join(data_path, 'wav/{}/{}'.format(data_set, person))):
            if wav[:-4] in wav_name_list:
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

data['txt'] = text_list[:len(data.wav)]
data['pinyin'] = pinyin_list[:len(data.wav)]

print('total num of wav is {}'.format(len(data.wav)))
print('total durations is {}h'.format(round(sum(data.durations)/3600.0, 3)))

data.to_csv('{}/aishell_1.csv'.format(BASE_PATH), index=False)
