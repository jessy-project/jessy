#!/bin/bash
cd /
wget http://incrediblepbx.com/picotts-raspi.tar.gz
tar zxvf picotts-raspi.tar.gz
rm -f picotts-raspi.tar.gz
cd /root
echo "Installing Pico TTS..."
./picotts-install.sh
