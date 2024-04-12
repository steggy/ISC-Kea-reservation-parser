#! /usr/bin/python3
#
# Author steggy
# ver 0.1
# Basic editing of isc-kea reservations


import os
import sys
import json
import requests
import pprint
import platform

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


def parse_single(record):
    print('Hostname: ', record['hostname'])
    print('MAC: ', record['hw-address'])
    print('IP: ', record['ip-address'])
    #print(record['option-data'][1])
    for i in record['option-data']:
        print(i['name'], i['data'])
        #for key in i:
        #    printf(key, "->", i[key], end =" ")
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
        if rows_read > 0 and rows_read % 20 == 0:
            ui = input(f'{"*" * 55}\n * Number to view\n * "Enter/Return" to continue\n * "q" to quit:\n ')
            if ui == 'q':
                break
            if ui:
                try:
                    num = int(ui)
                    clears()
                    ui = parse_single(x[num])
                    if ui.lower() == 'y':
                        #print(x[num]['hostname'])
                        edit_record(resv,x[num]['hostname'],num) 
                    #break
                    clears()
                except Exception as e:
                    print('Need a number')
                    print(e)
            
        # do stuff with each row
        rows_read += 1
    
    # do something else after 10 rows are read
    rows_read = 0



def edit_record(resv,host,num):
    for idx,rec in enumerate(resv['Dhcp4']['reservations']):
        if rec['hostname'] == host:
            print(idx)
    obj = list(enumerate(resv['Dhcp4']['reservations']))
    while True:
        res = input(f"Edit?\n[s]ave [q]uit [h]ostname [i]p [m]ac [r]outer [r]eminder [c]olor [d]escr:")
        if res.lower() == 'q':
            break
        #list(obj[num])[1]['hostname'] = 'wled2fred'
        print(list(obj[num])[1]['hostname'])
        #write_json(resv)
        #print(obj[num].hostname)
        #    print(list(enumerate(resv['Dhcp4']['reservations'][num][0]['hostname'])))

def main():
    global keajson
    if len(sys.argv) >= 2:
        keajson = sys.argv[1] 
    else: 
        print('enter filename')
        quit()
    res = get_file()
    #parse_reservation(res)
    list_reservations(res)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nThanks for playing")
        sys.exit()




#EOF


