#! /usr/bin/python3
#
# Author steggy
# ver 0.2
# Basic editing of isc-kea reservations
CHECKVERSION = "0.2"

import os, sys, re, json, requests, platform, socket 
import pprint
from valid import *
from option_data_valid import *
import readwriteconfig as CF
from tabulate import tabulate
from datetime import datetime


configfile = 'parse.conf'
title = f"Basic isc-kea reservation editing ver {CHECKVERSION}"
PipeLineFile = 'pipe-kea-dhcp4.conf'

def init():
    global configdict
    global configlist
    global ver 
    
    wd = os.path.dirname(os.path.abspath(__file__)) + '/' + configfile
    if not is_valid_file(wd):
        print(f"Config file {configfile} missing")
        return 
    try:
        configdict = dict(CF.Config(wd).Fetch('dataoptions'))
        configlist = list(configdict.values())
        ver = str(CF.Config(wd).Fetch('version')[0][1])
        return True
    except Exception as e:
        print(str(e))
        return 0


def border_text(txt):
    table = [[txt]]
    output = tabulate(table, tablefmt='grid')

    print(output)


def parse_api():
    response = requests.post('http://192.168.33.136:8000/', headers=headers, json=json_data2)
    data = response.json()
    print(data)
    #print('\n\n',data[0])
    #pprint.pprint(data, compact=True)

    #print(data[0]['arguments']['leases'][0])

    #for i in data[0]['arguments']['leases']:
    #    print(i['hostname'], i['hw-address'], i['ip-address'])


def get_file():
    if not is_valid_file(keajson):
        print('No file', keajson, 'Please pull new file')
        quit()
    else:
        with open(keajson) as f:
            d = json.load(f)
            f.close()
    return d

def write_json(res):
    fn = UniqFile(PipeLineFile)
    with open(fn, 'x') as file:
        json.dump(res, file, indent=4)
    file.close()



def parse_reservation(resv):
    #print(res['Dhcp4']['reservations'])
    for idx,x in enumerate(resv['Dhcp4']['reservations']):
        #print(x)
        print(f"\n{idx}) {x['hostname']} {x['hw-address']} {x['ip-address']}")
        if 'option-data' in x:
            #print('YES')
            #print(x['option-data'])
            for k in x['option-data']:
                print(k)
            #print(i[0]('hostname'))
        if idx > 1: 
            write_json(resv)
            quit()
    x = resv['Dhcp4']['reservations']
    print(x)
    resv['Dhcp4']['reservations'].append({"hostname": "steggynew","hw-address": "30:83:98:b1:36:ff","ip-address": "192.168.38.0",
        "option-data":[{"space": "dhcp4","name": "domain-name-servers","code": 6,"data": "192.168.33.45"}]}) 
    x = resv['Dhcp4']['reservations']
    print(x)
    print(type(x))
    write_json(resv)

def display_single_record(resv,num):
    obj = list(enumerate(resv['Dhcp4']['reservations']))
    for i in obj[num][1]:
        if 'option-data' not in i:
            print(f"{i}: {obj[num][1][i]}")
        else:
            for n in obj[num][1]['option-data']:
                if 'user-context' not in n:
                    print(n['name'])


def search_record(resv):
    result = []
    querytype = {'h':'hostname','i':'ip-address','m':'hw-address'}
    q = ''
    query = input('Type query for hostaname or "return" for IP:\n')
    q = 'h'
    if query == "":
        query = input('Type query for IP or "return" for MAC:\n')
        q = 'i'
        if query == '':
            query = input('Type query for MAC or "return" for All:\n')
            q = 'm'
    

    x = resv['Dhcp4']['reservations']
    for idx,row in enumerate(x):
        if query in row[querytype[q]]:
            result.append([idx,row['hostname'],row['ip-address'],row['hw-address']])
    if len(result) < 1:
        print('Record not found')
        return
    for idx,val in enumerate(result):
        print(f"{str(idx + 1).rjust(3, ' ')}) {val[1]} {val[2]} {val[3]}")
    answer = input('Enter number to edit:\n ')
    try:
        num = int(answer)
        num = num - 1
    except:
        print('Enter a number')
        return 
    print(result[num])
    edit_record(resv,result[num][1],result[num][0])




def parse_single(record):
    pad = 20
    print('\n\n')
    print(f"{str('Hostname').ljust(pad,' ')}:{record['hostname']}")
    print(f"{str('MAC').ljust(pad, ' ')}:{record['hw-address']}")
    print(f"{str('IP').ljust(pad, ' ')}:{record['ip-address']}")
    # check for "option-data" in record
    if 'option-data' in record:
        #print(record['option-data'][1])
        for i in record['option-data']:
            if 'name' in i:
                print(f"{str(i['name']).ljust(pad,' ')}:{i['data']}")
    else:
        print('Adding "option-data" for the use of "comment" field')
    print(f"{'=' * 30}")    
    ui = input('Edit record? y/n: ')
    return ui


def list_reservations(resv):
    x = resv['Dhcp4']['reservations']
    rows_read = 0
    for idx,row in enumerate(x):
        print(f"{str(idx).rjust(3, ' ')}) {str(row['hostname']).ljust(25, ' ')} {row['ip-address']}")
        if rows_read > 0 and rows_read % 20 == 0 or rows_read == len(x) - 1:
            while True:
                ui = input(f'{"*" * 55}\n Type number to view - [Enter] to continue - [t]op - [s]ave - [q]uit:\n ').lower()
                if ui == 'q':
                    quit()
                if ui == 't':
                    clears()
                    list_reservations(resv)
                if ui == '':
                    break
                try:
                    num = int(ui)
                    edit_record(resv,x[num]['hostname'],num)
                    break
                except Exception as e:
                    print(e)
                    print('Need a valid number or valid option')
                #clears()
                     
            clears() 
        # do stuff with each row
        rows_read += 1
    
    # do something else after 10 rows are read
    rows_read = 0


def verify_new_record_input(prompt,field,resv,dup = 0):
    needsdupcheck = ['hostname','ip-address','hw-address']
    while True:
        h = get_user_input(f"{prompt}: ")
        if h == 'q':
            return 'q'
        if dup == 1:
            result = dup_check(resv,field,h)
            if result:
                print(f"{h} Already in use")
                continue
        if is_valid(field,h):
            return h
            

def add_record_info(resv):
    newstore = {}
    newstore['hostname'] = verify_new_record_input('Hostname','hostname',resv,1)
    answer = verify_new_record_input('IP Address','ip-address',resv,1)
    if answer : newstore['ip-address'] = answer
    
    answer = verify_new_record_input('MAC Address','hw-address',resv,1)
    if answer : newstore['hw-address'] = answer
    optionsdata = [['domain-name-servers','Domain Name Server','ip-address','[k]eep - [return] to continue:'],
                   ['domain-name','Domain Name','host-name','[k]eep - [return] to continue:'],
                   ['broadcast-address','Broadcast Address','ip-address','[k]eep - [return] to continue:'],
                   ['subnet-mask','Subnet Mask','ip-address','[k]eep - [return] to continue:'],
                   ['routers','Router','ip-address','[k]eep - [return] to continue:']] 
    for i in optionsdata:
        ans = input(f"{i[1]}: {configdict[i[0]]}\n{i[3]}:\n")
        if ans.lower() == 'q':
            break
        if ans.lower() == 'k':
            newstore[i[0]] = configdict[i[0]]
        else:
            newstore[i[0]] = verify_new_record_input(i[1],i[2],resv)
    newstore['host-name'] = newstore['hostname'] 
    clears()
    border_text(title)
    for key in newstore:
        print(key, ":", newstore[key])
    ans = input('\nConfirm add record: y/n\n').lower()
    if ans == 'y':
        now = datetime.now()
        dte = now.strftime("%Y-%m-%d_%H:%M")
        od = []
        optdata = [['host-name',12],['domain-name-servers',6],['domain-name',15],['broadcast-address',28],['subnet-mask',1],['routers',3]]
        for i in optdata:
            od.append({'space': 'dhcp4', 'name': i[0], 'code': i[1], 'data': newstore[i[0]]})
        vals = {'hostname':newstore['hostname'],'hw-address':newstore['hw-address'],'ip-address':newstore['ip-address'],
                'user-context':{'comment': 'add record', 'last-modified': dte, 'description': ''},'option-data':od
                }
        resv['Dhcp4']['reservations'].append(vals)
        write_json(resv)     
        clears()
        return resv
    return resv
    

def edit_record(resv,host,num):
    store = {}
            
    valid_option_data(resv,num)        
    obj = list(enumerate(resv['Dhcp4']['reservations']))
    print('list obj',list(obj)[num][1]['hostname'])
    print('obj',obj[num][1]['hostname'])

    store['hostname'] = list(obj)[num][1]['hostname']        
    store['hw-address'] = list(obj)[num][1]['hw-address']
    store['ip-address'] = list(obj)[num][1]['ip-address']
    store['user-context'] = list(obj)[num][1]['user-context']

    
    for i in list(obj[num])[1]['option-data']:
        print(i)
        if 'name' in i:
            store[i['name']] = i['data']
            if i['name'] == 'host-name':
                if i['data'] == '':
                    store['host-name'] = store['hostname']
    print(store)
    clears()
    border_text(title)
    show_store_dict(store) 
    # Fields for promptuser_options list [ selection option] [store value] [validation type] [pretty prompt] [needs dup check] 
    promptuser_options ={'d':['[d]elete'],'s':['[s]ave'],'q':['[q]uit'],'h':['[h]ostname','hostname','hostname','Hostname',1],'i':['[i]p','ip-address','ip-address','IP Address',1],
                         'm':['[m]ac','hw-address','hw-address','MAC',1],'r':['[r]outer','routers','ip-address','Router',0],'k':['mas[k]','subnet-mask','ip-address','Subnet Mask',0],
                         'b':['[b]road-cast','broadcast-address','ip-address','Broadcast Address',0],'o':['d[o]main-name-server','domain-name-servers','ip-address','DNS',0],
                         'n':['domai[n]-name','domain-name','hostname','Domain name',0],'t':['descrip[t]ion','user-context','description','description',0],'w':['sho[w]-record']}
    print(list(promptuser_options)[0])
    while True:    
        res = input(f"{' '.join([str(promptuser_options[i][0]) for i in promptuser_options])}:\nEdit?\n").lower()
        if res in promptuser_options:
            if res == 'q':
                break
            #print('YES')
            if res == 'w':
                clears()

                show_store_dict(store)
                continue
            if res == 's':
                resv = save_record(store,num,resv)
                return resv
            if res == 'd':
                ans = input('Delete record? y/n\n')
                if ans.lower() == 'y':
                    del resv['Dhcp4']['reservations'][num]
                    write_json(resv)
                    return resv
            print(store[promptuser_options[res][1]])
            if res in promptuser_options:
                ans = verify_new_record_input(promptuser_options[res][3],promptuser_options[res][2],resv,promptuser_options[res][4])
                if not ans == 'q':
                    store[promptuser_options[res][1]] = ans
                
def save_record(record,num,resv):            
    obj = list(enumerate(resv['Dhcp4']['reservations']))
    #show_store_dict(record)
    clears()
    now = datetime.now()
    dte = now.strftime("%Y-%m-%d_%H:%M")
    record['host-name'] = record['hostname']
    #print(dte)
    border_text(title)
    for key in record:
        print(f"{key}: {record[key]}")
    answer = get_user_input("Save Record?\ny to save\nEnter/Return to continue\n" )
    if answer.lower() == 'y':   
        print('Saving Record')
        obj[num][1]['hostname'] = record['hostname']
        obj[num][1]['ip-address'] = record['ip-address']
        obj[num][1]['hw-address'] = record['hw-address']
        obj[num][1]['user-context'] = record['user-context']
        obj[num][1]['user-context']['comment'] = 'Record edited'
        obj[num][1]['user-context']['last-modified'] = dte
        for i in obj[num][1]['option-data']:
            i['data'] = record[i['name']]
            if i['name'] == 'host-name':
                i['data'] = record['hostname']
        print(obj[num][1])
        write_json(resv)
        return resv
    else:
        return resv


def show_store_dict(dict):
    for key in dict:
        print(f"{str(key).ljust(20, ' ')}:{dict[key]}")

def get_edit_input(key):
    res = input(f'Enter new value for {key}:\n')
    return res

def get_user_input(prompt):
    res = input(prompt)
    return res

def main():
    global keajson
    intt = init()
    if not intt:
        quit()
    if len(sys.argv) >= 2:
        keajson = sys.argv[1] 
    else: 
        print('enter filename')
        quit()
    res = get_file()
    #parse_reservation(res)
    clears()
    
    while True:
        border_text(title)
        answer = get_user_input(f"\nchoose:\n[l]ist/edit [s]earch [a]dd [q]uit\n ")
        if answer == 'l':
            stat = list_reservations(res)
            if stat == 'q':
                quit()
        if answer == 's':
            search_record(res)  
        if answer == 'a':
            res = add_record_info(res)
        if answer == 'q':
            quit()



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nThanks for playing")
        sys.exit()




#EOF


