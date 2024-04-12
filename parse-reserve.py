#! /usr/bin/python3
#
# Author steggy
# ver 0.1
# Basic editing of isc-kea reservations


import os, sys, re, json, requests, platform, socket 
import pprint



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



def clears():
# Clears the on-screen display  
    if platform.system() == 'Windows':
      os.system('cls')
    else:
      os.system('clear')



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
    if not os.path.isfile(keajson):
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


def restart():
    clears()
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

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


def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return 0
    except socket.error:
        return 1

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


def parse_single(record):
    pad = 20
    print(f"{str('Hostname').ljust(pad,' ')}:{record['hostname']}")
    print(f"{str('MAC').ljust(pad, ' ')}:{record['hw-address']}")
    print(f"{str('IP').ljust(pad, ' ')}:{record['ip-address']}")
    #print(record['option-data'][1])
    for i in record['option-data']:
        print(f"{str(i['name']).ljust(pad,' ')}:{i['data']}")
        #for key in i:
        #    printf(key, "->", i[key], end =" ")
    print(f"{'=' * 15}")    
    ui = input('Edit record? y/n: ')
    return ui


def list_reservations(resv):
    x = resv['Dhcp4']['reservations']
    #print(resv['Dhcp4']['reservations'])
    #print(len(x))
    #for i in x[0:9]:
    #    #print(i['hostname'])
    #    pass
    

    #number_of_rows = len(x)
    rows_read = 0
    for idx,row in enumerate(x):
        #print(Fore.LIGHTWHITE_EX + "{: <20}  {: <20} {: <20}".format(*i))
        print(f"{str(idx).rjust(3, ' ')}) {str(row['hostname']).ljust(25, ' ')} {row['ip-address']}")
        #print(rows_read % 10)
        if rows_read > 0 and rows_read % 20 == 0 or rows_read == len(x) - 1:
            ui = input(f'{"*" * 55}\n * Number to view\n * "Enter/Return" to continue\n * "s" to start from top\n * "q" to quit:\n ')
            ui = ui.lower()
            if ui == 'q':
                quit()
            if ui == 's':
                #return 'restart'
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



def edit_record(resv,host,num):
    store = {'hostname':'','mac':'','ip':'','domain-name-servers':'','domain-name':'','broadcast-address':'','subnet-mask':'','routers':'','host-name':''}
    for idx,rec in enumerate(resv['Dhcp4']['reservations']):
        if rec['hostname'] == host:
            print(idx)
    obj = list(enumerate(resv['Dhcp4']['reservations']))
    #print(list(obj)[num])
    store['hostname'] = list(obj)[num][1]['hostname']        
    store['mac'] = list(obj)[num][1]['hw-address']
    store['ip'] = list(obj)[num][1]['ip-address']

    #print(len(list(obj[num])[1]['option-data']))
    for i in list(obj[num])[1]['option-data']:
            #print(i['name'])
            store[i['name']] = i['data']
            #if i['name'] == 'domain-name':
            #    print(i['data'])
    
    print('store',store)
    while True:
        
        res = input(f"Edit?\n[s]ave [q]uit [h]ostname [i]p [m]ac [r]outer mas[k] [b]road-cast domain-[n]ame-server [d]omain-name:")
        res = res.lower()
        if res == 'q':
            break
        if res == 'i':
            n = 'ip'
            print(store[n])
            v = get_edit_input(n)
            if is_valid_ip(v) == 1:
                print('Need valid IP')
                continue
            store[n] = v    
        if res.lower() == 'd':
            n = 'domain-name'
            print(store[n])
            v = get_edit_input(n)
        if res == 'm':
            n = 'mac'
            print(store[n])
            v = get_edit_input(n)
            if not is_valid_mac(v):
                print('Need valid mac format[00:00:00:00:00:00]')
            v = v.replace('-', ':')
            print(v)
        if res == 'k':
            n = 'subnet-mask'
            print(store[n])
            v = get_edit_input(n)
            if is_valid_ip(v) == 1:
                print('Need valid IP')
                continue
            store[n] = v    
                      
        if res == 's':
            print('Saving Record')
            obj[num][1]['ip-address'] = store['ip']
            #list(obj[num])[1]['hostname'] = 'wled2fred'
            write_json(resv)
        #print(obj[num].hostname)
        #    print(list(enumerate(resv['Dhcp4']['reservations'][num][0]['hostname'])))

def get_edit_input(key):
    res = input(f'Enter new value for {key}:\n')
    return res


def main():
    global keajson
    if len(sys.argv) >= 2:
        keajson = sys.argv[1] 
    else: 
        print('enter filename')
        quit()
    res = get_file()
    #parse_reservation(res)
    clears()
    stat = list_reservations(res)
    if stat == 'restart':
        restart()
    if stat == 'q':
        quit()



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nThanks for playing")
        sys.exit()




#EOF


