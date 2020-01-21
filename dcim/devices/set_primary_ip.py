#!/usr/bin/python3
# 
import pynetbox
from netaddr import *

netbox_url = 'http://10.10.10.10:32769/api'
token = 'QFS2t4353qRwsr2qwrfDGWFgvw4524'

# Connect to NetBox
try:
  nb = pynetbox.api(url=netbox_url, token=token)
except pynetbox.core.query.RequestError as error:
  print(error.error)
  sys.exit(1)

ips = nb.ipam.ip_addresses.all()

for ip in ips:
  if IPAddress(str(ip)[:-3]) in IPNetwork("10.204.0.0/16"):
    device = ip.interface.device
    ip_dict = dict(
      primary_ip = ip.id,
      primary_ip4 = ip.id
    )

    dev_to_modify = nb.dcim.devices.get(name=device)
    dev_to_modify.update(ip_dict)
    dev_modified = nb.dcim.devices.get(name=device)
    print(dev_modified, dev_modified.primary_ip)




