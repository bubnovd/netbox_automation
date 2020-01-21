#!/usr/bin/python3
# 

from jinja2 import Template, Environment, FileSystemLoader
import requests, json, os, sys


usage = """Usage: python3 netbox2mikrotik.py [netbox_ip] [API Token] [output_file]
e.g. python3 netbox2mikrotik.py 10.0.0.10:32769 Gdstwt53t6gdsTGSXHey /etc/mikrotik/targets.yml"""

if len(sys.argv) != 4:
    print(usage)
    sys.exit(0)

api_url = 'http://' + sys.argv[1] + '/api'
devices_path = '/dcim/devices/'
token = 'Token ' + sys.argv[2]
headers = {'content-type': 'application/json', 'Authorization': token}
target_file = sys.argv[3]

# Fetch device list from NetBox
try:
  netbox_devices = requests.get(api_url+devices_path, headers=headers, params={"limit": 200})
except requests.exceptions.RequestException as error:
  print(error)
  sys.exit(1)

json_netbox_devices = netbox_devices.json()

# If token incorrect
if 'detail' in json_netbox_devices:
  print(json_netbox_devices['detail'])
  sys.exit(1)

# Preflight with template
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
file_loader = FileSystemLoader(THIS_FOLDER)
env = Environment(loader=file_loader)
template  = env.get_template('template.j2')

devices = []

# Make config from template
for result in json_netbox_devices['results']:
  if result['device_type']['manufacturer']['name'] == "Mikrotik":
    # if RouterOS
    if result['platform']['id'] == 1:
      target = {}
      target['devname'] = result['display_name']
      target['address'] = result['primary_ip']['address'].split("/", 2)[0]
      devices.append(target)

# Write config to file
config = template.render(devices=devices)
#print(config)
with open(target_file, 'w') as file:
    file.write(config)

