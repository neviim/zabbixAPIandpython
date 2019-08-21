from pyzabbix import ZabbixAPI
from config import *

# The hostname at which the Zabbix web interface is available
zapi = ZabbixAPI(url=server, user=username, password=password)

# Disable SSL certificate verification
zapi.session.verify = False

# Loop through all hosts interfaces, getting only "main" interfaces of type "agent"
for h in zapi.hostinterface.get(output=["dns","ip","useip","hostid"],
                                selectHosts=["host"],
                                filter={"main":1,"type":1}):

    print('Server %s has IP %s has ID %s' % (h['hosts'][0]['host'], h['ip'], h['hostid']))
