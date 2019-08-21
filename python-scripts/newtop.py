import yaml
from pyzabbix import ZabbixAPI

with open("config.yml", 'r') as ymlfile:    #reading config.yml for credentails
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

ZABBIX_SERVER = cfg['zabbix']['server']
USERNAME = cfg['zabbix']['user']
PASSWD = cfg['zabbix']['passwd']

zapi = ZabbixAPI(url=ZABBIX_SERVER, user=USERNAME, password=PASSWD)
count = 0

# Disable SSL certificate verification
zapi.session.verify = False

# Loop through all hosts interfaces, getting only "main" interfaces of type "agent"
for h in zapi.trigger.get(output=["triggerid","description","priority"],expandData="1",expandDescription="1",lastChangeSince="1470737192",sortfield="priority",sortorder="DESC"):
    print('Server %s ' % h['description'])

