
# coding: utf-8

# In[34]:


import os
import pandas as pd
import json
import soundfile as sf
from pypinyin import lazy_pinyin


BASE_PATH = os.getcwd()
data_path = os.path.join(BASE_PATH, 'THCH30/data_thchs30')

wav_list = [i for i in os.listdir(os.path.join(data_path, 'data')) if i.endswith('.wav')]

data = pd.DataFrame()

data["wav"] = wav_list
data["wav_path"] = data.wav.apply(lambda x: "THCH30/data_thchs30/data/{}".format(x))


def read_text(x):
    path = os.path.join(BASE_PATH, x)
    with open("{}.trn".format(path)) as f:
        a = f.readlines()[0].strip('\n').replace(" ", "")
    return a


def read_wav(x):
    path = os.path.join(BASE_PATH, x)
    sig,sr = sf.read(path)
    duration = round(float(len(sig))/float(sr), 3)
    return duration


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


data["txt"] = data.wav_path.apply(lambda x:read_text(x))
data["pinyin"] = data.txt.apply(lambda x : ' '.join([pinyin_cover(i) for i in lazy_pinyin(x)]))
data["durations"] = data.wav_path.apply(lambda x:read_wav(x))

total_duration = round(sum(data.durations)/3600, 4)
total_wavfile = len(data.wav)

print("total durations is {}h, total wavfiles is {}".format(total_duration, total_wavfile))

data.to_csv(os.path.join(BASE_PATH, "thch30.csv"),index=False)
