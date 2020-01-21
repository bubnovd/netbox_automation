#!/usr/bin/python3

import requests, json, re

devices = [
"10.204.25.1",
"10.204.27.1",
"10.204.28.2"
]

sitess = [
"25",
"27",
"28"]
api_url = 'http://10.10.10.10:32769/api'
dev_type_path = '/dcim/device-types/'
site_path = '/dcim/sites/'
prefix_path = '/ipam/prefixes/'
dev_path = '/dcim/devices/'
headers = {'content-type': 'application/json', 'Authorization': 'Token QFS2t4353qRwsr2qwrfDGWFgvw4524'}

# Device role. You can see this at http://10.10.10.10:32769/api/dcim/device-roles/
role = 4
# Device type. You can see this at http://10.10.10.10:32769/api/dcim/device-types/
modelid = 8
#platform = 1
custom_fields = {"prom_labels": "{'env': 'sk'}"}

###dev_types = requests.get(api_url+dev_type_path, headers=headers)
###json_dev_types = dev_types.json()

sites = requests.get(api_url+site_path, headers=headers, params={"limit": 300})
json_sites = sites.json()

for address, site in zip(devices, sitess):
  splitaddress = re.split('(.*)\.(.*)\.(.*)\.(.*)', address)
  if splitaddress[-2] == "1":
    name = "POS1." + site + ".SK"
  elif splitaddress[-2] == "2":
    name = "POS2." + site + ".SK"
  elif splitaddress[-2] == "3":
    name = "POS3." + site + ".SK"

  for result in json_sites['results']:
    if result['name'] == site:
      siteid = result['id']
  # Print with PLATFORM. Change it if need
  #print(f"name={name}, modelid={modelid}, siteid={siteid}, roleid={role}, platformid={platform}, custom_fields={custom_fields})
  #print(f"name={name}, modelid={modelid}, siteid={siteid}, roleid={role}, custom_fields={custom_fields}")

  payload = {"name": name, "device_role": role, "site": siteid, "custom_fields": custom_fields, "primary_ip": address, "device_type": modelid}
  r = requests.post(api_url+dev_path, data=json.dumps(payload), headers=headers)
  print(r.url, r.text) 
  #print(payload)


# Эта часть добавляет девайс нужного типа. Для этого в списке devices должны быть типы девайсов и номер сайта
###for site, dev_type in devices.items():
###  name = "POS." + site + ".SK"
###  for result in json_dev_types['results']:
###    if result['model'] == dev_type:
###      modelid = result['id']
###  for result in json_sites['results']:
###    if result['name'] == site:
###      siteid = result['id']
###  # Print with PLATFORM. Change it if need
###  #print(f"name={name}, modelid={modelid}, siteid={siteid}, roleid={role}, platformid={platform}, custom_fields={custom_fields})
###  #print(f"name={name}, modelid={modelid}, siteid={siteid}, roleid={role}, custom_fields={custom_fields}")
###
###  payload = {"name": name, "device_type": modelid, "device_role": role, "site": siteid, "custom_fields": custom_fields}
###  #r = requests.post(api_url+dev_path, data=json.dumps(payload), headers=headers)
###  print(r.url, r.text)
 