#!/usr/bin/python3
# 
import pynetbox

netbox_url = 'http://10.10.10.10:32769/api'
token = 'QFS2t4353qRwsr2qwrfDGWFgvw4524'
role = 'pos'

# Connect to NetBox
try:
  nb = pynetbox.api(url=netbox_url, token=token)
except pynetbox.core.query.RequestError as error:
  print(error.error)
  sys.exit(1)

dev_group = nb.dcim.devices.filter(role=role)

for device in dev_group:
  thirdoctet = str(device)[5:-3]
  if len(thirdoctet) == 2:
    fourthoctet = str(device)[3:-6]
  elif len(thirdoctet) == 3:
    fourthoctet = str(device)[3:-7]  
  address = "10.204."+thirdoctet+"."+fourthoctet+"/32"
  interfaces = nb.dcim.interfaces.filter(device=str(device))
  for interface in interfaces:
    interface = interface.id

# New address  
  ip_add_dict = dict(
    address = address,
    status = 1,
    interface = interface
  )
  
  new_ip = nb.ipam.ip_addresses.create(ip_add_dict)
  print(
    "Device '{device}' created with interface '{interface}', which has IP {ipadd}.".format(
      device=device, interface=interface, ipadd=new_ip["address"]
    )
  )




