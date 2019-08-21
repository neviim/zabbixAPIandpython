from pyzabbix import ZabbixAPI
from config import *

# The hostname at which the Zabbix web interface is available
zapi = ZabbixAPI(url=server, user=username, password=password)

# Disable SSL certificate verification
zapi.session.verify = False

#query_api='{"name": "Registration action","eventsource": 2,"status": 0,"esc_period": 0,"filter": {"evaltype": 0,"conditions": [{"conditiontype": 24,"operator": 2,"value": "application"}]},"operations": [{"esc_step_from": 1,"esc_period": 0,"operationtype": 4,"esc_step_to": 1,"opgroup": [{"groupid": "4"}]}]}'
# Loop through all hosts interfaces, getting only "main" interfaces of type "agent"
for h in zapi.hostgroup.get(output=["name","groupid"], filter={"name": ["Zabbix servers"]}):
   print('Group ID of %s is %s' % (h['name'], h['groupid']))
   
   zapi.action.create(name="Registration action",
		eventsource=2,
		status=0,
		esc_period=0,
		filter={
			"evaltype": 0,
			"conditions": [{
				"conditiontype": 24,
				"operator": 2,
				"value": "application"
			}]
		},
		operations=[{
			"esc_step_from": 1,
			"esc_period": 0,
			"operationtype": 4,
			"esc_step_to": 1,
                        "opgroup": [{"groupid":h['groupid']}]

		}])  
   print("registration rule created")
   