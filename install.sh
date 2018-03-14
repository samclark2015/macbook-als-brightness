#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

cp ./brightness.py /usr/local/bin/brightness.py
chmod +x /usr/local/bin/brightness.py

cp ./brightness.service /etc/systemd/system/brightness.service
chmod +x /etc/systemd/system/brightness.service

systemctl enable brightness
systemctl start brightness
