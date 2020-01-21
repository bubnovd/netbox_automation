#!/usr/bin/python3

import requests, json

d= { 21: "branch1", 22: "branch2", 23: "branch3" }
turl = 'http://10.10.10.10:32769/api//dcim/sites/'
headers = {'content-type': 'application/json', 'Authorization': 'Token QFS2t4353qRwsr2qwrfDGWFgvw4524'}

for key, value in d.items():
  url = turl + str(key) + "/"
  payload = {"physical_address": value}
  r = requests.patch(url, data=json.dumps(payload), headers=headers)
  print(r.url, r.text)