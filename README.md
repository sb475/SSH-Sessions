# ssh-sessions
Very simple SSH tool to help track SSH connections and tunnels.



ssh-sessions.py is a very simple python script that can track your tunnels. It can be used exactly as a user would run an ssh command, however it will track the tunnels and add or remove as you tear down or put up connections.

Installation:

run the "setup.sh" script. This will create the appropriate directories and link the script for easy use.
```
sudo mkdir /etc/ssh-sessions
sudo cp ssh-sessions.py /etc/ssh-sessions
sudo chmod 744 /etc/ssh-sessions/ssh-sessions.py
sudo ln /etc/ssh-sessions/ssh-sessions.py -T /usr/bin/ssh-sessions
```

Usage:

To use the ssh-sessions, simply type ssh-sessions instead of ssh at the beginning of your commands.

`ssh-sessions -L2201:192.168.1.1:22 root@127.0.0.1`

If your command is incorrect, you will be prompted with the ssh command options, just as if you typed it wrong with ssh.

View active connections simple type the command with no arguments. This will also keep track of your ssh command history in case you need to reference it at a later point. The active tunnels and command history are kept in two files in the /etc/ssh-sessions/ directory.

Command history: "/etc/ssh-sessions/ssh_command_history"
Active connections: "/etc/ssh-sessions/active_tunnels"

Limitations:
If you manually shut down a tunnel ssh-sessions will not be able to track that change...yet.


