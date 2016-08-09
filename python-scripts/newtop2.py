import yaml
from pyzabbix import ZabbixAPI

with open("config.yml", 'r') as ymlfile:    #reading config.yml for credentails
    cfg = yaml.load(ymlfile)

ZABBIX_SERVER = cfg['zabbix']['server']   
USERNAME = cfg['zabbix']['user']
PASSWD = cfg['zabbix']['passwd']
TIMESTAMP = '1470737192'
zabbixServer = ZabbixAPI(ZABBIX_SERVER)

# Disable SSL certificate verification
zabbixServer.session.verify = False

# Login to the Zabbix API
zabbixServer.login(USERNAME, PASSWD)

# Loop through all hosts interfaces, getting only "main" interfaces of type "agent"
print("Report based on time::")
for h in zabbixServer.trigger.get(output=["triggerid","description","priority"],expandData="1",expandDescription="1",lastChangeSince=TIMESTAMP, sortfield="priority",sortorder="DESC"):
    print(' %s ' % h['description'])
