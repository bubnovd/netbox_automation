#!/usr/bin/python3
# Привязывает IP адрес к интерфейсу устройства. Третий октет адреса должен совпадать с частью имени. Адрес привязывается к bridge1

import requests, json

api_url = 'http://10.10.0.10:8080/api'
ipaddr_path = '/ipam/ip-addresses/'
interfaces_path = '/dcim/interfaces/'
iface_name = "eth1"

headers = {'content-type': 'application/json', 'Authorization': 'Token qwrfsdfwerqwedsfwfsf'}

ipaddr = requests.get(api_url+ipaddr_path, headers=headers, params={"limit": 300})
json_ipaddr = ipaddr.json()

ifaces = requests.get(api_url+interfaces_path, headers=headers, params={"limit": 200000})
json_ifaces = ifaces.json()

for result in json_ipaddr['results']:
  third = result['address'].split(".", 2)[2].split(".")[0]
  ipaddr_id = result['id']
  for iface_result in json_ifaces['results']:
    if iface_result['name'] == iface_name:
      iface_name_num = iface_result['device']['name'].split(".",3)[1]
      #print(iface_name_num) 

      if iface_name_num == third:
        payload = {"id": ipaddr_id, "address": result['address'], "nat_outside": "", "interface": iface_result['id']}
        #print(api_url+ipaddr_path+str(ipaddr_id)+"/", payload)
        r = requests.put(api_url+ipaddr_path+str(ipaddr_id)+"/", data=json.dumps(payload), headers=headers)
        print(r.url, r.text)
