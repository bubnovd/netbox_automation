#!/usr/bin/python3

import requests, json

d = {"101": "CRS125-24G-1S",
"102": "CRS125-24G-1S",
"106": "CRS326-24G-2S+"
}

api_url = 'http://10.10.10.10:32769/api'
dev_type_path = '/dcim/device-types/'
site_path = '/dcim/sites/'
prefix_path = '/ipam/prefixes/'
dev_path = '/dcim/devices/'
headers = {'content-type': 'application/json', 'Authorization': 'Token QFS2t4353qRwsr2qwrfDGWFgvw4524'}

role = 1
platform = 1
custom_fields = {"prom_labels": "{'env': 'sk'}"}

dev_types = requests.get(api_url+dev_type_path, headers=headers)
json_dev_types = dev_types.json()

sites = requests.get(api_url+site_path, headers=headers, params={"limit": 200})
json_sites = sites.json()

for key, value in d.items():
  name = "R." + key + ".SK"
  for result in json_dev_types['results']:
    if result['model'] == value:
      modelid = result['id']
  for result in json_sites['results']:
    if result['name'] == key:
      siteid = result['id']
  #print(f"name={name}, modelid={modelid}, siteid={siteid}, roleid={role}, platformid={platform}, LABELS={prom_labels}")
  payload = {"name": name, "device_type": modelid, "device_role": role, "platform": platform, "site": siteid, "custom_fields": custom_fields}
  r = requests.post(api_url+dev_path, data=json.dumps(payload), headers=headers)
  print(r.url, r.text)