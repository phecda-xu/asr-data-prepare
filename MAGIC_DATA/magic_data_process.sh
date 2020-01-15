#! /usr/bin/bash

mkdir magic_data
mkdir magic_data/metadata
mkdir magic_data/transcript

tar -xzvf metadata.tar.gz -C magic_data/metadata

tar -xzvf dev_set.tar.gz -C magic_data/wav
tar -xzvf test_set.tar.gz -C magic_data/wav
tar -xzvf train_set.tar.gz -C magic_data/wav


mv magic_data/wav/dev/TRANS.txt magic_data/transcript/dev_TRANS.txt
mv magic_data/wav/test/TRANS.txt magic_data/transcript/test_TRANS.txt
mv magic_data/wav/train/TRANS.txt magic_data/transcript/test_TRANS.txt

python magic_data.py
