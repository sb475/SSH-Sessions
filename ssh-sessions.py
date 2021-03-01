#!/usr/bin/python3

import os
import sys
import subprocess
import argparse
import re

active_tunnels="/etc/ssh-sessions/active_tunnels"
ssh_history="/etc/ssh-sessions/ssh_command_history"
#clear buffer
stringToExecute = []

#count arguments and start after 1
n = len(sys.argv)
#print ("Total arguments passed:", n)
if (len(sys.argv) < 2):
    print ("You did not enter enough options for a command. Listing active tunnels:")
    subprocess.run(['cat', active_tunnels])
    sys.exit(1)
else:
    for i in range (1, n):
        stringToExecute.append(sys.argv[i])

#uncomment to debug commands
#print (stringToExecute)
stringToExecute.insert(0,'ssh')
if not '-fN' in stringToExecute:
    stringToExecute.append('-fN')

#if no options are included close down.


#string to log
cmd_string = subprocess.list2cmdline(stringToExecute)

#execute command
try:
    cmd_results = subprocess.run(stringToExecute, check=True)
    success = True
    #log command
except subprocess.CalledProcessError as e:
    output = e.output
    success = False
    #log output

def determine_ctl_cmd(stringToExecute):
    for string in stringToExecute:
        if string == ('-O'):
            i = stringToExecute.index(string)
            try:
                if (stringToExecute[i+1] == 'forward'):
                    return 'forward'
                elif (stringToExecute[i+1] == 'cancel'):
                    return 'cancel'
                else:
                    return False
            except IndexError:
                    return False

def check_for_active_connection(local_ip, local_port, remote_host, remote_port):
    #check to see if tunnel exists
    with open(active_tunnels, "r") as f:
        for line in f:
            if local_port in line:
                if local_ip in line:
                    if remote_host in line:
                        if remote_port in line:
                            return line
                        else:
                            continue
        return False

def add_tunnel_to_active_list(cmd_string):
    with open(active_tunnels, "a") as f:
        text=cmd_string + "\n"
        f.write(text)
    print (text, " written to active tunnels")

def remove_tunnel_from_active(cmd_string):
    with open(active_tunnels, "r+") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            if i != cmd_string:
                f.write(i)
        f.truncate()
    
    print ("Removed ", cmd_string," from active tunnels")

def add_cmd_to_history(cmd_string):
    with open(ssh_history, "a") as f:
        f.write(cmd_string + "\n")

def index_containing_substring(the_list, substring):
    for i, s in enumerate(stringToExecute):
        if substring in s:
            return i
    return -1

def parse_tunnel(option):
    options = []
    i = index_containing_substring(stringToExecute, option)
    #print ("Options to parse: ", option)
   # print ("Index of stringToExecute: ",i)
   # print (stringToExecute[i])
    if (stringToExecute[i] == option):
        i+=1
        options = stringToExecute[i].split(':')
        #print ("If Options: ", options)
    else:
        options=stringToExecute[i].split(':')
        options[0] = re.sub(option, '', options[0])
        #print ("Else Options: ", options)

    return options

def forward_tunnel(option):
    tunnel_options = parse_tunnel(option)
        #SSH -L localhost:localport:remotehost:remoteport
    if (len(tunnel_options) < 4):
        tunnel_options.insert(0,"127.0.0.1")
    
    local_ip = tunnel_options[0]
    local_port = tunnel_options[1]
    remote_host = tunnel_options[2]
    remote_port = tunnel_options[3]

    tunnel_active=check_for_active_connection(local_ip, local_port, remote_host, remote_port)
    cmd=determine_ctl_cmd(stringToExecute)

   # print ("Tunnel exists: ", tunnel_active)
    
    #print ("Command: ", cmd)
    if (cmd == 'forward'):
        if (tunnel_active == False):
            add_tunnel_to_active_list(cmd_string)
        else:
            print ("Tunnel already exists")
    elif (cmd == 'cancel'):
        if (tunnel_active == False):
            print ("Tunnel does not exists to cancel")
        else:
            print ("Tunnel line is: ", tunnel_active)
            remove_tunnel_from_active(tunnel_active)
    else:
        print ("Was that command correct? No '-O' cmd_ctrl option found")
        exit()

def remote_tunnel(option):
    tunnel_options = parse_tunnel(option)
        #SSH -L localhost:localport:remotehost:remoteport
    if (len(tunnel_options) < 4):
        tunnel_options.insert(0,"0.0.0.0")

    remote_host = tunnel_options[0]
    remote_port = tunnel_options[1] 
    local_ip = tunnel_options[2]
    local_port = tunnel_options[3]

    return remote_host, remote_port, local_ip, local_port


def dynamic_tunnel(option): 
    #SSH -D proxy
    dynamic_proxy_port = parse_tunnel(option)
    return dynamic_proxy_port



if (success):
    #print(cmd_results)
    print ("Command logged: ", cmd_string)
    add_cmd_to_history(cmd_string)
    #forward tunnels
    if any('-L' in s for s in stringToExecute):
       forward_tunnel('-L')
    #remote tunnels
    elif any('-R' in s for s in stringToExecute):
        remote_tunnel('-R')
    #dynamic tunnels
    elif any('-D' in s for s in stringToExecute):
        dynamic_tunnel('-D')


