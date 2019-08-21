import socket
import yaml

from getpass import getpass
from pyzabbix import ZabbixAPI, ZabbixAPIException

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
for h in zapi.hostinterface.get(output=["dns","ip","useip","hostid"],selectHosts=["host"],filter={"main":1,"type":1}):
    # Make sure the hosts are named according to their FQDN
    if h['dns'] != h['hosts'][0]['host']:
        print('Warning: %s has dns "%s"' % (h['hosts'][0]['host'], h['dns']))

    # Make sure they are using hostnames to connect rather than IPs (could be also filtered in the get request)
    if h['useip'] == '1':
        print('Hostname=%s IP=%s HOSTID=%s' % (h['hosts'][0]['host'], h['ip'], h['hostid']))
        continue

    # Do a DNS lookup for the host's DNS name
    try:
        lookup = socket.gethostbyaddr(h['dns'])
    except socket.gaierror as e:
        print(h['dns'], e)
        continue
    actual_ip = lookup[2][0]

    # Check whether the looked-up IP matches the one stored in the host's IP
    # field
    if actual_ip != h['ip']:
        print("%s has the wrong IP: %s. Changing it to: %s" % (h['hosts'][0]['host'],
                                                               h['ip'],
                                                               actual_ip))

        # Set the host's IP field to match what the DNS lookup said it should
        # be
        try:
            #zapi.hostinterface.update(interfaceid=h['interfaceid'], ip=actual_ip)
            print(h['interfaceid'], " ", actual_ip)
            
        except ZabbixAPIException as e:
            print(e)
