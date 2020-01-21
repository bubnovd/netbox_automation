#!/usr/bin/python3
# 

from jinja2 import Template, Environment, FileSystemLoader
import os, sys, pynetbox


usage = """Usage: python3 netbox2wmi.py [netbox_ip] [API Token] [manufacturer] [output_file]
e.g. python3 netbox2blackbox.py 10.0.0.10:32769 Gdstwt53t6gdsTGSXHey Microsoft /etc/prometheus/file_sd/targets.yml"""

if len(sys.argv) != 5:
    print(usage)
    sys.exit(0)

netbox_url = 'http://' + sys.argv[1]
token = sys.argv[2]
# What device manufacturer export to targets.yml
manufacturer = sys.argv[3]
target_file = sys.argv[4]

# Fetch vm list from NetBox
try:
  nb = pynetbox.api(url=netbox_url, token=token)
except pynetbox.core.query.RequestError as error:
  print(error.error)
  sys.exit(1)

data = '''
#
# Managed by netbox2wmi.py. DON'T EDIT THIS FILE!!!
#

{% for vm in vms %}
- labels:
    vm_name: "{{ vm.name }}"
    env: prod
  targets: {{ vm.address }}
{% endfor %}
'''

template = Template(data)

# Select VM by manufacturer
vm_group = nb.virtualization.virtual_machines.all()
vms = []
for vm in vm_group:
  if str(vm.platform.manufacturer) == manufacturer:
    target = {}
    target['name'] = vm.name
    target['address'] = str(vm.primary_ip)[:-3]
    vms.append(target)

#  print(vm.platform)

config = template.render(vms=vms)
#print(config)
with open(target_file, 'w') as file:
    file.write(config)