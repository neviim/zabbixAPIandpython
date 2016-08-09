from pyzabbix import ZabbixAPI

# The hostname at which the Zabbix web interface is available
ZABBIX_SERVER = 'http://10.0.132.171:8080/zabbix'

zapi = ZabbixAPI(ZABBIX_SERVER)

# Disable SSL certificate verification
zapi.session.verify = False

# Login to the Zabbix API
zapi.login('Admin', 'zabbix')

# Loop through all hosts interfaces, getting only "main" interfaces of type "agent"
for h in zapi.trigger.get(output=["triggerid","description","priority"],expandData="1",expandDescription="1",lastChangeSince="1470737192",sortfield="priority",sortorder="DESC"):
    print('Server %s ' % h['description'])

