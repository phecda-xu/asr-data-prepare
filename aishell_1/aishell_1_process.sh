#!/bin/bash

tar -xzvf data_aishell.tgz

cd data_aishell
cd wav

files=$(ls)
for filename in $files
    # 
    do
        tar -xzvf $filename
        rm $filename
    done