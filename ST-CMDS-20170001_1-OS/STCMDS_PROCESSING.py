
# coding: utf-8

import os
import pandas as pd
import json
import soundfile as sf


BASE_PATH = os.getcwd()
data_path = os.path.join(BASE_PATH, 'ST-CMDS-20170001_1-OS')

wav_list = []
text_list = []
wav_path_list = []
durations_list = []
for wav_name in os.listdir(os.path.join(data_path, 'wav')):
    wav_list.append(wav_name)
    with open(os.path.join(data_path, 'txt/{}'.format(wav_name.replace('wav','txt')))) as f:
        trans = f.readlines()[0]
        text_list.append(trans)
        wav_path_list.append('wav/{}'.format(wav_name))
        sig, _ = sf.read(os.path.join(data_path, 'wav/{}'.format(wav_name)))
        duration = round(len(sig)/16000.0,4)
        durations_list.append(duration)

print("total file num is {}".format(len(wav_list)))

ST_data = pd.DataFrame()
ST_data["wav"] = wav_list
ST_data["txt"] = text_list
ST_data["wav_path"] = wav_path_list
ST_data["durations"] = durations_list

total_time = round(sum(ST_data["durations"])/3600.0, 2)
print("total duration is {}".format(total_time))

ST_data.to_csv(os.path.join(BASE_PATH, "ST-CMDS-2017.csv"))
