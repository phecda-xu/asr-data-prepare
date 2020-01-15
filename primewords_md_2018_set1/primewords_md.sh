#! /usr/bin/bash

tar -xzvf primewords_md_2018_set1.tar.gz
cd primewords_md_2018_set1

mkdir wav

cd audio_files
pwd

data_sets=$(ls) 


for i in $data_sets
	do
		cd $i
		pwd
		dirname=$(ls)
		for j in $dirname
			do
			mv $j/*.wav ../../wav/
			done
		cd ..
	done

python primewords_md.py