#!/bin/bash

u_appeared=false

check_u_flag() {
    if [ "$u_appeared" = false ]
		then 
			cd Arduino
			ino build
			ino upload
			cd ..
			u_appeared=true
		else return
	fi	
}

if [ "$EUID" -ne 0 ]
	then echo "You must run this script as root!" >&2
	exit
fi

while getopts "u" opt; do
  case $opt in
    u) check_u_flag
		;;
    \?)		
		exit
		;;
  esac
done

cd Pi
sudo python3 main.py
cd ..