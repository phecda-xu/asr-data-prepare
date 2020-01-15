#! /usr/bin/env  bash

tar -xzvf aidatatang_200zh.tgz

path=aidatatang_200zh/corpus

files=$(ls $path)
for setname in $files
    # train,test,dev set
    do
        setpath=$path'/'$setname
        #
        gzfiles=$(ls $setpath)
        for gzfile in $gzfiles
            # .gz file in set 
            do
                gzfilepath=$setpath'/'$gzfile
                echo $gzfilepath
                pwd
                tar -xzvf $gzfilepath -C  $setpath
                rm $gzfilepath
            done
    done

python data_tang_process.py