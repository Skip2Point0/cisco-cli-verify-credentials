# cisco-ssh-verify-credentials

Summary:

This script is intended for an environment where many combinations of different usernames and passwords exist. It will 
attempt to SSH, and then Telnet, into switches defined in the config PARAMETERS of the script and will try to authenticate.
Upon successful authentication, credentials for that specific device will be displayed in the console. Might take a while 
to run depending on the number of switches and username/password combinations. This was tested primarily in virtual Cisco
environment and might have different effect on specific physical Cisco models.

Requirements:

1) Interpreter: Python 3.8.0+
2) Python Packages: telnetlib, netmiko, paramiko, re

How to run:

1) Open verify_credentials.py file with a text editor of your choice. Replace example configurations in the PARAMETERS 
section. Lines 7-11. By default, ip addresses must be added to switches.txt file, one per line.
2) By default, both SSH and Telnet are enabled. 
   1) To disable SSH, comment out Line 111.
   2) To disable Telnet, comment out Line 112.
3) Run python3 verify_credentials.py in the terminal. Successful authentication will show in the terminal.