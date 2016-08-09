import yaml

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

abc=cfg['zabbix']['server']
cde=cfg['zabbix']['passwd']
print(abc)
print(cde)
