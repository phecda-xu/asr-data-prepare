
# coding: utf-8

import os
import pandas as pd
import soundfile as sf
from pypinyin import lazy_pinyin

BASE_PATH = os.getcwd()

data_path = os.path.join(BASE_PATH, 'aidatatang_200zh/corpus')


def read_text(path):
    with open(path, 'r') as f:
        a = f.readlines()[0].strip('\n')
    return a


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


wav_list = []
path_list = []
duration_list = []
data_set_list = []
text_list = []
pinyin_list = []
for data_set in os.listdir(data_path):
    for person in os.listdir(os.path.join(data_path, data_set)):
        for wav_file in os.listdir(os.path.join(data_path, '{}/{}'.format(data_set, person))):
            if wav_file.endswith('.wav'):
                data_set_list.append(data_set)
                wav_list.append(wav_file)
                path_list.append("aidatatang_200zh/corpus/{}/{}/{}".format(data_set, person, wav_file))
                sig, sr = sf.read(os.path.join(data_path, '{}/{}/{}'.format(data_set, person, wav_file)))
                duration = round(float(len(sig))/float(sr), 3)
                duration_list.append(duration)
                text_path = os.path.join(data_path, '{}/{}/{}'.format(data_set, person, wav_file.replace('wav', 'txt')))
                txt = read_text(text_path)
                text_list.append(txt)
                text_pinyin = ' '.join([pinyin_cover(i) for i in lazy_pinyin(txt)])
                pinyin_list.append(text_pinyin)


print("total wav num is {}".format(len(wav_list)))

data = pd.DataFrame()

data["wav"] = wav_list
data["wav_path"] = path_list
data["durations"] = duration_list
data["txt"] = text_list
data['pinyin'] = pinyin_list
data["data_set"] = data_set_list

print("total durations is {}h".format(round(sum(data.durations)/3600.0, 3)))

data.to_csv(os.path.join(BASE_PATH, "data_tang_200.csv"), index=False)
