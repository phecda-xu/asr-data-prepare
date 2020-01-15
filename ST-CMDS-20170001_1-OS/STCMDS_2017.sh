#! /usr/bin/bash

tar -xzvf ST-CMDS-20170001_1-OS.tar.gz

cd ST-CMDS-20170001_1-OS

mkdir metadata
mkdir wav
mkdir txt

find . -maxdepth 1 -name "*.metadata"  -exec mv {} metadata/  \;
find . -maxdepth 1 -name "*.wav"  -exec mv {} wav/  \;
find . -maxdepth 1 -name "*.txt"  -exec mv {} txt/  \;

python STCMDS_PROCESSING.py