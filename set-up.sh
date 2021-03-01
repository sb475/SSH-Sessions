#!/bin/bash

#besure to run as sudo
sudo mkdir /etc/ssh-sessions
sudo cp ssh-sessions.py /etc/ssh-sessions
sudo chmod 744 /etc/ssh-sessions/ssh-sessions.py
sudo ln /etc/ssh-sessions/ssh-sessions.py -T /usr/bin/ssh-sessions
