#! /usr/bin/python3
#
# Author steggy
# ver 0.1
# Validating function


import os, sys, re, json, requests, platform, socket 
import pprint
def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return 

def is_valid_mac(value):
    allowed = re.compile(r"""
                         (
                             ^([0-9A-F]{2}[-]){5}([0-9A-F]{2})$
                            |^([0-9A-F]{2}[:]){5}([0-9A-F]{2})$
                         )
                         """,
                         re.VERBOSE|re.IGNORECASE)

    if allowed.match(value) is None:
        return 
    else:
        return True 

def is_valid_hostname(hname):
    res = " " in hname
    return res 

def is_valid_domain_server(dname):
    pcnt = dname.count('.')
    if pcnt == 3:
        is_valid_ip(dname)

def restart():
    clears()
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

def clears():
# Clears the on-screen display  
    if platform.system() == 'Windows':
      os.system('cls')
    else:
      os.system('clear')



#EOF


