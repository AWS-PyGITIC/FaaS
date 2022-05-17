#!/bin/bash

dirs=$(ls -l . | awk '{if ($1 ~ /^d/) { print $9 }}' )

for item in $dirs
do
    rm $(echo $item.zip)
    zip $(echo $item.zip) $item/*
done

