#!/usr/bin/python3
# Меняет опцию Prometheus Labels у всех девайсов

import requests, json

api_url = 'http://10.10.10.10:32769/api'
#ipaddr_path = '/ipam/ip-addresses/'
devices_path = '/dcim/devices/'

headers = {'content-type': 'application/json', 'Authorization': 'Token QFS2t4353qRwsr2qwrfDGWFgvw4524'}

devices = requests.get(api_url+devices_path, headers=headers, params={"limit": 200})
json_devices = devices.json()

for result in json_devices['results']:
  device_id = result['id']
  payload = {"custom_fields": {'prom_labels': '{"env": "sk"}'}}
  r = requests.patch(api_url+devices_path+str(device_id)+"/", data=json.dumps(payload), headers=headers)
  print(r.url, r.text)
  #print(result['id'], result['custom_fields'])
