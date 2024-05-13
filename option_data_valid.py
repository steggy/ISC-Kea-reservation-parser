#! /usr/bin/python3



# check for option-data - if not create
def valid_option_data(records,num):
    optdata = [['host-name',12],['domain-name-servers',6],['domain-name',15],['broadcast-address',28],['subnet-mask',1],['routers',3]] 
    obj = list(enumerate(records['Dhcp4']['reservations']))
    if 'option-data' in list(obj[num])[1]:
        for i in optdata:
            if not next((item for item in obj[num][1]['option-data'] if "name" in item and item["name"] == i[0]), None):
                obj[num][1]['option-data'].append({'space': 'dhcp4', 'name': i[0], 'code': i[1], 'data': ''})
        chk = 'n'    
        #for i in obj[num][1]['option-data']:
        #    if 'user-context' in i:
        #        chk = 'y'
        #if chk == 'n':
        #    list(obj[num])[1]['option-data'].append({'user-context':{'comment':'','last-modified':'','description':''}})
    else:
        print('NO OPTION-DATA')
        list(obj)[num][1]['option-data'] = [{'space': 'dhcp4', 'name': 'host-name', 'code': 12, 'data': ''}]
        list(obj)[num][1]['option-data'].append({"space": "dhcp4","name": "domain-name-servers","code": 6,"data": ""})
        list(obj)[num][1]['option-data'].append({"space": "dhcp4","name": "domain-name","code": 15,"data": "syntax.lo"})
        list(obj)[num][1]['option-data'].append({"space": "dhcp4","name": "broadcast-address","code": 28,"data": ""})
        list(obj)[num][1]['option-data'].append({"space": "dhcp4","name": "subnet-mask","code": 1,"data": ""})
        list(obj)[num][1]['option-data'].append({"space": "dhcp4","name": "routers","code": 3,"data": ""})
        #list(obj)[num][1]['option-data'].append({'user-context':{'comment':'','last-modified':'','description':''}})
    if 'user-context' not in list(obj[num])[1]:
        print('NO CONTEX')
        list(obj[num])[1]['user-context'] = {'comment':'','last-modified':'','description':''}
        
    if 'user-context' in list(obj[num])[1]:
        print(list(obj[num])[1]['user-context'])

    print(list(obj)[num][1])
    #quit()




