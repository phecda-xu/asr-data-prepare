
# coding: utf-8

# In[34]:


import os
import pandas as pd
import json
import soundfile as sf


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



data["txt"] = data.wav_path.apply(lambda x:read_text(x))
data["durations"] = data.wav_path.apply(lambda x:read_wav(x))

total_duration = round(sum(data.durations)/3600, 4)
total_wavfile = len(data.wav)

print("total durations is {}h, total wavfiles is {}".format(total_duration, total_wavfile))

data.to_csv(os.path.join(BASE_PATH, "thch30.csv"),index=False)
