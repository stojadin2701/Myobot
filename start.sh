#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "You must run this script as root!"
  exit
fi

./upload.sh

cd Pi
sudo python main.py
cd ..
