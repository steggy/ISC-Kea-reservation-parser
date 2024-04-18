



def valid_option_data(records,num):
    obj = list(enumerate(records['Dhcp4']['reservations']))
    if 'option-data' in list(obj[num])[1]:
        print(list(obj[num])[1])
        if not next((item for item in list(obj[num])[1]['option-data'] if "name" in item and item["name"] == 'host-name'), None):
            list(obj)[num][1]['option-data'].append({'space': 'dhcp4', 'name': 'host-name', 'code': 12, 'data': ''})
        if 'user-context' not in list(obj[num])[1]['option-data']:
            print('No Context')
            list(obj[num])[1]['option-data'].append({'user-context':{'comment':'','last-modified':'','description':''}})
        #if not next((item for item in list(obj[num])[1]['option-data'] if not item["user-context"]), None):
        #    list(obj)[num][1]['option-data'].append({'user-context':{'comment':'','last-modified':'','description':''}})
            dd = list(obj[num])[1]['option-data']
            print(dd)
            #print(test)
            #if 'host-name' in list(obj[num])[1]['option-data']:
            #    print('I HAVE HOST-NAME')
        else:
            print('No host-name')
    else:
        print('NO OPTION-DATA')
        print(list(obj)[num][1])
        list(obj)[num][1]['option-data'] = [{'space': 'dhcp4', 'name': 'host-name', 'code': 12, 'data': ''}]
        list(obj)[num][1]['option-data'].append({'user-context':{'comment':'','last-modified':'','description':''}})
        print(list(obj)[num][1])
    #res = records
    #retrun res 




