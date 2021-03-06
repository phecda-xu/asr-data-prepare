
# coding: utf-8

import os
import re
import pandas as pd
import soundfile as sf
from pypinyin import lazy_pinyin


BASE_PATH = os.getcwd()

data_path = os.path.join(BASE_PATH, 'magic_data')


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


real_wav_list = []
for data_set in ["train", "test", "dev"]:
    for person in os.listdir(os.path.join(data_path,'wav',data_set)):
        for i in os.listdir(os.path.join(data_path,'wav',data_set, person)):
            real_wav_list.append(i)

print('total real num of wavs is {}'.format(len(real_wav_list)))

TRANS_list = []
for data_set in ["train", "test", "dev"]:
    with open('magic_data/transcript/{}_TRANS.txt'.format(data_set), 'r') as f:
        lines = f.readlines()[1:]
        TRANS_list.extend(lines)

wav_txt_dic = {}
for i in TRANS_list:
    wav_file, person, txt = i.strip('\n').split('\t')
    wav_txt_dic[wav_file] = re.sub('[^\w\u4e00-\u9fff]+', '', txt.replace('[FIL]', '').replace('[SPK]', ''))

print('total files in TRANS {}'.format(len(TRANS_list)))

scp_list = []
for data_set in ["train", "test", "dev"]:
    with open("magic_data/metadata/{}.scp".format(data_set), 'r') as f:
        lines = f.readlines()
        scp_list.extend(lines)

print('total files in scp {}'.format(len(scp_list)))

wav_file_list = []
path_list = []
durations_list = []
for wav in scp_list:
    wav_file, path = wav.strip('\n').split('\t')
    wav_file_list.append(wav_file)
    path_list.append('MAGIC_DATA/magic_data/{}'.format(path))
    sig, sr = sf.read(os.path.join(data_path, path))
    durations_list.append(round(float(len(sig))/float(sr), 3))



data = pd.DataFrame()

data['wav'] = wav_file_list
data['wav_path'] = path_list
data['durations'] = durations_list
data['txt'] = data.wav.apply(lambda x: wav_txt_dic[x])
data['pinyin'] = data.txt.apply(lambda x: ' '.join([pinyin_cover(i) for i in lazy_pinyin(x, errors='ignore')]))

print('total duration is {}'.format(round(float(sum(data.durations))/3600.0, 3)))

data.to_csv('{}/magic_data.csv'.format(BASE_PATH), index=False)
