# zabbixAPIandpython
This repository containes json files which we pass to Zabbix API. It will then process the query and provide you with the result. Along with this, some python code to process json output.


		curl -X POST -d @file-name.json "URL-of-Zabbix"/api_jsonrpc.php --header "Content-Type:application/json" 

	Example:
		curl -X POST -d @triggerget1.json http://10.0.132.171:8080/zabbix/api_jsonrpc.php --header "Content-Type:application/json" 


