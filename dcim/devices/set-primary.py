#!/usr/bin/python3
# Делает адрес Primary для девайса

import requests, json

api_url = 'http://10.10.0.10:8080/api'
ipaddr_path = '/ipam/ip-addresses/'
devices_path = '/dcim/devices/'

headers = {'content-type': 'application/json', 'Authorization': 'Token qwrfsdfwerqwedsfwfsf'}

ipaddr = requests.get(api_url+ipaddr_path, headers=headers, params={"limit": 300})
json_ipaddr = ipaddr.json()

devices = requests.get(api_url+devices_path, headers=headers, params={"limit": 300})
json_devices = devices.json()


for result in json_devices['results']:
    name_num = result['name'].split(".", 3)[1]
    site = result['site']['id']
    role = result['device_role']['id']
    dtype = result['device_type']['id']
    for ip_result in json_ipaddr['results']:
        third = ip_result['address'].split(".", 2)[2].split(".")[0]
        if third == name_num:
            device_id = result['id']
            payload = {"id": device_id, "primary_ip": ip_result['id'], "primary_ip4": ip_result['id'], "site": site, "device_role": role, "device_type": dtype}
            r = requests.put(api_url+devices_path+str(device_id)+"/", data=json.dumps(payload), headers=headers)
            print(r.url, r.text)
            #print(payload)
