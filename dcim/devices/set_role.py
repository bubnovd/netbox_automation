#!/usr/bin/python3
# 
import pynetbox
from netaddr import *

netbox_url = 'http://10.10.10.10:32769/api'
token = 'QFS2t4353qRwsr2qwrfDGWFgvw4524'
role = 'pos'

# Connect to NetBox
try:
  nb = pynetbox.api(url=netbox_url, token=token)
except pynetbox.core.query.RequestError as error:
  print(error.error)
  sys.exit(1)

ips = nb.ipam.ip_addresses.all()

for ip in ips:
  if IPAddress(str(ip)[:-3]) in IPNetwork("10.204.0.0/16"):
    ip_dict = dict(
        role = 40
    )

    ip.update(ip_dict)
    ip_modified = nb.ipam.ip_addresses.get(address=ip.address)
    print(ip_modified, ip_modified.role)





