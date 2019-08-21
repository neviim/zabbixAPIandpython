import json

j = json.loads('{"interfaceid": "5","hostid": "10107","main": "1","type": "1","useip": "1","ip": "192.168.3.1","dns": "","port": "10050","bulk": "1","hosts": [{"hostid": "10107","hosting": "Linux server", "host": "rajiv" }, {"hostid": "101071","hosting": "Linux1server", "host": "1rajiv" }],"id": 1}')

print(j["hosts"][1]["hostid"])
