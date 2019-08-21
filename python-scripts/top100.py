from pyzabbix import ZabbixAPI
from config import *

# The hostname at which the Zabbix web interface is available
zapi = ZabbixAPI(url=server, user=username, password=password)

# Disable SSL certificate verification
zapi.session.verify = False

# Loop through all hosts interfaces, getting only "main" interfaces of type "agent"
for h in zapi.trigger.get(output=["triggerid","description","priority"],expandData="1",expandDescription="1",lastChangeSince="1470737192",sortfield="priority",sortorder="DESC"):
    print('Server %s ' % h['description'])

