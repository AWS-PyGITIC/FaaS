#!/bin/sh -l

echo "hola esto es un test $1"
echo "::set-output name=time::$1"
python3 /diagram.py
