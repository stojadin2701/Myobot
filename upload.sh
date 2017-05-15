#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "You must run this script as root!"
  exit
fi

cd Arduino
ino build
ino upload
cd ..
