#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "You must run this script as root!"
  exit
fi

cd Pi
sudo python3 main.py
cd ..
