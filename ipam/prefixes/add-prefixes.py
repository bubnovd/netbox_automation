#!/usr/bin/python3

import requests, json

d= {21: "10.202.16.0/24",
22: "10.202.17.0/24",
23: "10.202.18.0/24"
}

url = 'http://10.10.10.10:32769/api/ipam/prefixes/'
headers = {'content-type': 'application/json', 'Authorization': 'Token QFS2t4353qRwsr2qwrfDGWFgvw4524'}

for key, value in d.items():
  payload = {"prefix": value, "site": key}
  #print(payload)
  r = requests.post(url, data=json.dumps(payload), headers=headers)
  print(r.url, r.text)

