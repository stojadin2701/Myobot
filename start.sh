#!/bin/bash

check_u_flag() {
    if [ "$u_appeared" = false ]
		then 
			./upload.sh
			u_appeared=true
		else return
	fi	
}

if [ "$EUID" -ne 0 ]
	then echo "You must run this script as root!" >&2
	exit
fi

u_appeared=false

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