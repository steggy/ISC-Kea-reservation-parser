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

def is_valid_file(fn):
    if os.path.isfile(fn):
        return True

def is_valid_hostname(hname):
    res = " " in hname
    return res 

def is_valid(field,val):
    if field == 'hostname':
        if " " not in val:
            return True
        print('Spaces not allowed in Hostname')

    if field == 'ip-address':
        try:
            socket.inet_aton(val)
            return True
        except socket.error:
             print(f"IP {val} not formatted correctly")
    if field == 'hw-address':
        allowed = re.compile(r"""
                             (
                             ^([0-9A-F]{2}[-]){5}([0-9A-F]{2})$
                            |^([0-9A-F]{2}[:]){5}([0-9A-F]{2})$
                             )
                             """,
                             re.VERBOSE|re.IGNORECASE)

        if allowed.match(val) is None:
            print(f"MAC {val} not valid") 
        else:
            return True 

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

def dup_check(data,field,query):
    for idx,val in enumerate(data['Dhcp4']['reservations']):
        if query == val[field]:
            #print(val[field])
            return True

#EOF


