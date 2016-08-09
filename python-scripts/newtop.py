import yaml
from pyzabbix import ZabbixAPI

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
# The hostname at which the Zabbix web interface is available
ZABBIX_SERVER = cfg['zabbix']['server']

zapi = ZabbixAPI(ZABBIX_SERVER)

# Disable SSL certificate verification
zapi.session.verify = False
USERNAME = cfg['zabbix']['user']
PASSWD = cfg['zabbix']['passwd']
# Login to the Zabbix API
zapi.login(USERNAME, PASSWD)

# Loop through all hosts interfaces, getting only "main" interfaces of type "agent"
for h in zapi.trigger.get(output=["triggerid","description","priority"],expandData="1",expandDescription="1",lastChangeSince="1470737192",sortfield="priority",sortorder="DESC"):
    print('Server %s ' % h['description'])

