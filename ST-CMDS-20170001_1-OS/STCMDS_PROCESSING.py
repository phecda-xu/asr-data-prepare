
# coding: utf-8

import os
import pandas as pd
import json
import soundfile as sf
from pypinyin import lazy_pinyin


BASE_PATH = os.getcwd()
data_path = os.path.join(BASE_PATH, 'ST-CMDS-20170001_1-OS')


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
text_list = []
wav_path_list = []
durations_list = []
pinyin_list = []
for wav_name in os.listdir(os.path.join(data_path, 'wav')):
    wav_list.append(wav_name)
    with open(os.path.join(data_path, 'txt/{}'.format(wav_name.replace('wav','txt')))) as f:
        trans = f.readlines()[0]
        text_list.append(trans)
        pinyin_text = ' '.join([pinyin_cover(i) for i in lazy_pinyin(trans)])
        pinyin_list.append(pinyin_text)
        wav_path_list.append('ST-CMDS-20170001_1-OS/ST-CMDS-20170001_1-OS/wav/{}'.format(wav_name))
        sig, _ = sf.read(os.path.join(data_path, 'wav/{}'.format(wav_name)))
        duration = round(len(sig)/16000.0,4)
        durations_list.append(duration)

print("total file num is {}".format(len(wav_list)))

ST_data = pd.DataFrame()
ST_data["wav"] = wav_list
ST_data["txt"] = text_list
ST_data["pinyin"] = pinyin_list
ST_data["wav_path"] = wav_path_list
ST_data["durations"] = durations_list

total_time = round(sum(ST_data["durations"])/3600.0, 2)
print("total duration is {}".format(total_time))

ST_data.to_csv(os.path.join(BASE_PATH, "ST-CMDS-2017.csv"), index=False)
