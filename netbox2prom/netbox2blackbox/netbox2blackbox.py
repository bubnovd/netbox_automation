#!/usr/bin/python3
# 
# Создает yml для blackbox-exporter с параметрами в лейблах: ip, device_name, device_physical_location. 

from jinja2 import Template, Environment, FileSystemLoader
import os, sys, pynetbox


usage = """Usage: python3 netbox2blackbox.py [netbox_ip] [API Token] [device_roles] [output_file]
e.g. python3 netbox2blackbox.py 10.0.0.10:32769 Gdstwt53t6gdsTGSXHey ats /etc/prometheus/file_sd/targets.yml"""

if len(sys.argv) != 5:
    print(usage)
    sys.exit(0)

netbox_url = 'http://' + sys.argv[1]
token = sys.argv[2]
# What device types export to targets.yml
role = sys.argv[3]
target_file = sys.argv[4]

# Fetch device list from NetBox
try:
  nb = pynetbox.api(url=netbox_url, token=token)
except pynetbox.core.query.RequestError as error:
  print(error.error)
  sys.exit(1)

data = '''
#
# Managed by netbox2prom.py. DON'T EDIT THIS FILE!!!
#

{% for device in devices %}
- labels:
    nb_name: "{{ device.nb_name }}"
    nb_physical_address: "{{ device.nb_physical_address }}"
  targets: [{{ device.address }}]
{% endfor %}
'''

template = Template(data)
# Select devices by role
dev_group = nb.dcim.devices.filter(role=role)

# Make config from template
devices = []
for device in dev_group:
  if str(device.status) == "Active":
    target = {}
    target['nb_physical_address'] = device.site.physical_address
    target['nb_name'] = device.name
    target['address'] = str(device.primary_ip)[:-3]
    devices.append(target)
    
config = template.render(devices=devices)
#print(config)
with open(target_file, 'w') as file:
    file.write(config)