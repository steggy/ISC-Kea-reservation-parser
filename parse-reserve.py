#! /usr/bin/python3
#
# Author steggy
# ver 0.1
# Basic editing of isc-kea reservations


import os, sys, re, json, requests, platform, socket 
import pprint
from valid import *
import readwriteconfig as CF

configfile = 'parse.conf'
title = f"{'=' * 30}\nBasic isc-kea reservation editing"

headers = {
    'Content-Type': 'application/json',
}


json_data = {
    'command': 'lease4-get-all',
    'service': [
        'dhcp4',
    ],
}

json_data2 = {
    "command": "reservation-get-all",
    "arguments": {
        "subnet-id": 1
    },
    'service': [
        'dhcp4',
    ],
}





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
    with open('data.json', 'w') as file:
        json.dump(res, file, indent=4)




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

def search_record(resv):
    result = []
    query = input('Enter search:\n')
    x = resv['Dhcp4']['reservations']
    for idx,row in enumerate(x):
        if query in row['hostname']:
            #d = {idx,row['hostname']}
            result.append([idx,row['hostname']])
    if len(result) < 1:
        print('Record not found')
        return
    for idx,val in enumerate(result):
        print(f"{str(idx + 1).rjust(3, ' ')}) {val[1]}")
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
    #print(record['option-data'][1])
    for i in record['option-data']:
        print(f"{str(i['name']).ljust(pad,' ')}:{i['data']}")
        #for key in i:
        #    printf(key, "->", i[key], end =" ")
    print(f"{'=' * 30}")    
    ui = input('Edit record? y/n: ')
    return ui


def list_reservations(resv):
    x = resv['Dhcp4']['reservations']
    rows_read = 0
    for idx,row in enumerate(x):
        print(f"{str(idx).rjust(3, ' ')}) {str(row['hostname']).ljust(25, ' ')} {row['ip-address']}")
        if rows_read > 0 and rows_read % 20 == 0 or rows_read == len(x) - 1:
            ui = input(f'{"*" * 55}\n * Number to view\n * "Enter/Return" to continue\n * "s" to start from top\n * "q" to quit:\n ')
            ui = ui.lower()
            if ui == 'q':
                quit()
            if ui == 's':
                clears()
                list_reservations(resv)
            if not ui == '':
                try:
                    num = int(ui)
                except Exception as e:
                    print('Need a number')
                    print(e)
                clears()
                ui = parse_single(x[num])
                if ui.lower() == 'y':
                    #print(x[num]['hostname'])
                    edit_record(resv,x[num]['hostname'],num) 
            clears() 
        # do stuff with each row
        rows_read += 1
    
    # do something else after 10 rows are read
    rows_read = 0
def verify_new_record_input(prompt,field,resv = ''):
    needsdupcheck = ['hostname','ip-address','hw-address']
    while True:
        h = get_user_input(f"{prompt}: ")
        if len(resv) > 0:
            result = dup_check(resv,field,h)
            if result:
                print(f"{h} Already in use")
                continue
        if is_valid(field,h):
            return h
            

def add_record_info(resv):
    newstore = {}
    newstore['hostname'] = verify_new_record_input('Hostname','hostname',resv)
    #if answer : newstore['hostname'] = answer

    answer = verify_new_record_input('IP Address','ip-address',resv)
    if answer : newstore['ip-address'] = answer
    
    answer = verify_new_record_input('MAC Address','hw-address',resv)
    if answer : newstore['hw-address'] = answer
    print(newstore)
    quit()
    
    while True:
        h = get_user_input('MAC Adress:')
        result = dup_check(resv,'hw-address',h)
        if result:
            print(f"{h} Already in use")
        else:
            if not is_valid_mac(h):
                print(f"MAC {h} not valid")
            else:
                newstore['hw-address'] = h
                break
    print(newstore)

def edit_record(resv,host,num):
    #store = {'hostname':'','mac':'','ip':'','domain-name-servers':'','domain-name':'','broadcast-address':'','subnet-mask':'','routers':'','host-name':''}
    store = {}
    '''for idx,rec in enumerate(resv['Dhcp4']['reservations']):
        if rec['hostname'] == host:
            print(idx)'''
    obj = list(enumerate(resv['Dhcp4']['reservations']))
    #print(list(obj)[num])
    store['hostname'] = list(obj)[num][1]['hostname']        
    store['hw-address'] = list(obj)[num][1]['hw-address']
    store['ip-address'] = list(obj)[num][1]['ip-address']

    #print(len(list(obj[num])[1]['option-data']))
    for i in list(obj[num])[1]['option-data']:
            #print(i['name'])
            store[i['name']] = i['data']
            #if i['name'] == 'domain-name':
            #    print(i['data'])

    # Check for host-name in option-data
    hashost = 0
    for i in obj[num][1]['option-data']:
        #print(i)
        if i['name'] == 'host-name':
            hashost = 1
            break
    if hashost == 0:
        print('NO HOST')
        obj[num][1]['option-data'].append({'space': 'dhcp4', 'name': 'host-name', 'code': 12, 'data': ''})
        store['host-name'] = store['hostname']
    #print('store',store)
    while True:
        
        res = input(f"Edit?\n[d]elete [s]ave [q]uit [h]ostname [i]p [m]ac [r]outer mas[k] [b]road-cast d[o]main-name-server [d]omain-name sho[w]-record:\n")
        res = res.lower()
        if res == 'q':
            break
        if res == 'i':
            n = 'ip-address'
            print(store[n])
            store[n] = verify_new_record_input('IP Address',n,resv)
                
        if res == 'b':
            n = 'broadcast-address'
            print(store[n])
            store[n] = verify_new_record_input('Broadcast Address','ip-address')
            '''v = get_edit_input(n)
            if not is_valid_ip(v):
                print('Need valid IP')
                continue
            store[n] = v'''    
        if res == 'r':
            n = 'routers'
            print(store[n])
            store[n] = verify_new_record_input('Router','ip-address')
            '''v = get_edit_input(n)
            if not is_valid_ip(v):
                print('Need valid IP')
                continue
            store[n] = v'''    
        if res == 'o':
            n = 'domain-name'
            print(store[n])
            v = get_edit_input(n)
            store[n] = v
        if res == 'h':
            n = 'hostname'
            print(store[n])
            store['hostname'] = verify_new_record_input('Hostname',n,resv)
            
            
        if res == 'm':
            n = 'hw-address'
            print(store[n])
            store[n] = verify_new_record_input('MAC',n,resv)
            
        if res == 'n':
            n = 'domain-name-servers'
            print(store[n])
            v = get_edit_input(n)
            store[n] = v
        if res == 'w':
            show_store_dict(store)
        if res == 'k':
            n = 'subnet-mask'
            print(store[n])
            v = get_edit_input(n)
            if not is_valid_ip(v):
                print('Need valid IP')
                continue
            store[n] = v    
                      
        if res == 's':
            show_store_dict(store)
            answer = get_user_input("Are you sure you want to save?\ny to save\nEnter/Return to continue\n" )
            if answer.lower() == 'y':
                print('Saving Record')
                obj[num][1]['ip-address'] = store['ip']
                #list(obj[num])[1]['hostname'] = 'wled2fred'
                #write_json(resv)
        #print(obj[num].hostname)
        #    print(list(enumerate(resv['Dhcp4']['reservations'][num][0]['hostname'])))


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
        print(title)
        answer = get_user_input(f"\nchoose:\n[l]ist/edit [s]earch [a]dd [q]uit\n ")
        if answer == 'l':
            stat = list_reservations(res)
            if stat == 'q':
                quit()
        if answer == 's':
            search_record(res)  
        if answer == 'a':
            add_record_info(res)
            #add record
            #print(len(res['Dhcp4']['reservations']))
            #print(res['Dhcp4']['reservations'][*]['hostname'])
            #quit()
            
            #anw = input('Enter test data\n')
            ##tres = dup_check(res,'hostname',anw)
            #tres = dup_check(res,'ip-address',anw)
            #print(tres)
            #pass
        if answer == 'q':
            quit()



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nThanks for playing")
        sys.exit()




#EOF


