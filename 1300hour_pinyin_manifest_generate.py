
# coding: utf-8

import os
import json
import codecs
import pandas as pd

BASE_PATH = os.getcwd()

path_prefix = '/DeepSpeech'
manifest_path_prefix = '/root/DeepSpeech/data/1300hour_data/1300h_manifest'


magic_data = pd.read_csv(os.path.join(BASE_PATH,'MAGIC_DATA/magic_data.csv'))
thch30_data = pd.read_csv(os.path.join(BASE_PATH, 'THCH30/thch30.csv'))
aidatatang_data = pd.read_csv(os.path.join(BASE_PATH,'aidatatang_200zh/data_tang_200.csv'))
primewords_data = pd.read_csv(os.path.join(BASE_PATH,'primewords_md_2018_set1/primewords_md_2018_set1.csv'))
aishell1_data = pd.read_csv(os.path.join(BASE_PATH,'aishell_1/aishell_1.csv'))
stcmd_data = pd.read_csv(os.path.join(BASE_PATH,'ST-CMDS-20170001_1-OS/ST-CMDS-2017.csv'))


aishell_train = aishell1_data[aishell1_data['data_set']== 'train']
aishell_test = aishell1_data[aishell1_data['data_set']== 'test']
aishell_dev = aishell1_data[aishell1_data['data_set']== 'dev']

print('total test set data duration is {}h'.format(round(float(sum(aishell_test.durations))/3600.0,3)))
print('total dev set data duration is {}h'.format(round(float(sum(aishell_dev.durations))/3600.0,3)))

train_manifest_list = []
test_manifest_list = []
dev_manifest_list = []


print('add magic_data...')
train_manifest_list.extend(magic_data.apply(lambda x: json.dumps({'audio_filepath':'{}/{}'.format(path_prefix, x[1]), 
                                                                  'duration':x[2],
                                                                  'text':x[4]}, ensure_ascii=False), axis=1))

print('num of train_manifest is {}'.format(len(train_manifest_list)))


print('add thch30_data...')
train_manifest_list.extend(thch30_data.apply(lambda x: json.dumps({'audio_filepath':'{}/{}'.format(path_prefix, x[1]), 
                                                                   'duration':x[4],
                                                                   'text':x[3]}, ensure_ascii=False), axis=1))

print('num of train_manifest is {}'.format(len(train_manifest_list)))


print('add aidatatang_data...')
train_manifest_list.extend(aidatatang_data.apply(lambda x: json.dumps({'audio_filepath':'{}/{}'.format(path_prefix, x[1]), 
                                                                       'duration':x[2],
                                                                       'text':x[4]}, ensure_ascii=False), axis=1))

print('num of train_manifest is {}'.format(len(train_manifest_list)))


print('add primewords_data...')
train_manifest_list.extend(primewords_data.apply(lambda x: json.dumps({'audio_filepath':'{}/{}'.format(path_prefix, x[6]),
                                                                       'duration':x[2],
                                                                       'text':x[5]}, ensure_ascii=False), axis=1))

print('num of train_manifest is {}'.format(len(train_manifest_list)))


print('add aishell_train...')
train_manifest_list.extend(aishell_train.apply(lambda x: json.dumps({'audio_filepath':'{}/{}'.format(path_prefix, x[1]), 
                                                                     'duration':x[2],
                                                                     'text':x[5]}, ensure_ascii=False), axis=1))

print('num of train_manifest is {}'.format(len(train_manifest_list)))


print('add stcmd_data...')
train_manifest_list.extend(stcmd_data.apply(lambda x: json.dumps({'audio_filepath':'{}/{}'.format(path_prefix, x[3]),
                                                                  'duration':x[4],
                                                                  'text':x[2]}, ensure_ascii=False), axis=1))

print('num of train_manifest is {}'.format(len(train_manifest_list)))


print('prepare aishell_test...')
test_manifest_list.extend(aishell_test.apply(lambda x: json.dumps({'audio_filepath':'{}/{}'.format(path_prefix, x[1]), 
                                                                   'duration':x[2],
                                                                   'text':x[5]}, ensure_ascii=False), axis=1))

print('num of test_manifest is {}'.format(len(test_manifest_list)))


print('prepare aishell_dev...')
dev_manifest_list.extend(aishell_dev.apply(lambda x: json.dumps({'audio_filepath':'{}/{}'.format(path_prefix, x[1]), 
                                                                 'duration':x[2],
                                                                 'text':x[5]}, ensure_ascii=False), axis=1))

print('num of dev_manifest is {}'.format(len(dev_manifest_list)))


def save_manifest(manifest_path, manifest_list):
    with codecs.open(manifest_path, 'w', 'utf-8') as fout:
        for line in manifest_list:
            fout.write(line + '\n')
    print('manifest saved in {}'.format(manifest_path))


train_manifest_path = manifest_path_prefix + '.' + 'train'
test_manifest_path = manifest_path_prefix + '.' + 'test'
dev_manifest_path = manifest_path_prefix + '.' + 'dev'


save_manifest(train_manifest_path, train_manifest_list)
save_manifest(test_manifest_path, test_manifest_list)
save_manifest(dev_manifest_path, dev_manifest_list)
