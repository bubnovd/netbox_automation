#!/usr/bin/python3

import requests, json

addresses = { 
"10.202.26.190",
"10.202.54.190",
"10.202.24.190"   
}

url = 'http://10.10.10.10:32769/api/ipam/ip-addresses/'
headers = {'content-type': 'application/json', 'Authorization': 'Token QFS2t4353qRwsr2qwrfDGWFgvw4524'}

for address in addresses:
  payload = {"address": address, "role": "40", "nat_outside": 0}
  #print(payload)
  r = requests.post(url, data=json.dumps(payload), headers=headers)
  print(r.url, r.text)

