#!/usr/bin/python3

import requests, json

devices = {
"54": "KX-TDE200",
"24": "KX-TDE200",
"16": "KX-TDE200",
"34": "KX-TDE200",
"17": "KX-TDE200",
"25": "KX-TDE200",
"18": "KX-TDE200",
"27": "KX-TDE200",
"32": "KX-TDE200",
"29": "KX-TDE200",
"30": "KX-TDE200",
"28": "KX-TDE200",
"33": "KX-TDE200"
}

api_url = 'http://10.10.0.10:8080/api'
dev_type_path = '/dcim/device-types/'
site_path = '/dcim/sites/'
prefix_path = '/ipam/prefixes/'
dev_path = '/dcim/devices/'
headers = {'content-type': 'application/json', 'Authorization': 'Token qwrfsdfwerqwedsfwfsf'}

# Device role. You can see this at http://10.10.0.10:8080/api/dcim/device-roles/
role = 3
#platform = 1
custom_fields = {"prom_labels": "{'env': 'sk'}"}

dev_types = requests.get(api_url+dev_type_path, headers=headers)
json_dev_types = dev_types.json()

sites = requests.get(api_url+site_path, headers=headers, params={"limit": 200})
json_sites = sites.json()

for site, dev_type in devices.items():
  name = "ATS." + site + ".SK"
  for result in json_dev_types['results']:
    if result['model'] == dev_type:
      modelid = result['id']
  for result in json_sites['results']:
    if result['name'] == site:
      siteid = result['id']
  # Print with PLATFORM. Change it if need
  #print(f"name={name}, modelid={modelid}, siteid={siteid}, roleid={role}, platformid={platform}, custom_fields={custom_fields})
  #print(f"name={name}, modelid={modelid}, siteid={siteid}, roleid={role}, custom_fields={custom_fields}")

  payload = {"name": name, "device_type": modelid, "device_role": role, "site": siteid, "custom_fields": custom_fields}
  r = requests.post(api_url+dev_path, data=json.dumps(payload), headers=headers)
  print(r.url, r.text)