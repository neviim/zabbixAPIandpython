#!/usr/bin/python

"""
ZABBIX-REPORT-GENERATOR

Utility to generate report of tiggers occur in a particular date interval. 00:00:00 is the time period 
when date entered as command-line argument.

Example: python reports.py -f 11/08/2016 -t 12/08/2016

More Information: python reports.py -h or --help
  
"""
import yaml
import sys, argparse
import time
import datetime
from pyzabbix import ZabbixAPI

with open("config.yml", 'r') as ymlfile:    #reading config.yml for credentails
    cfg = yaml.load(ymlfile)

ZABBIX_SERVER = cfg['zabbix']['server']
USERNAME = cfg['zabbix']['user']
PASSWD = cfg['zabbix']['passwd']
zabbixServer = ZabbixAPI(ZABBIX_SERVER)
count = 0

# Disable SSL certificate verification
zabbixServer.session.verify = False

# Login to the Zabbix API
zabbixServer.login(USERNAME, PASSWD)

def epoctime( dateCurrent ):
   "this will convert date to epoc"
   epochTime=str(int(time.mktime(datetime.datetime.strptime(dateCurrent, "%d/%m/%Y").timetuple())))
   return epochTime


def reportTrigger( sinceEpoch, tillEpoch, summ, count, sinceDate, tillDate ):
   "this function process the time in EPOCH and provide with the result of triggers in calculated period of time"
   print("Report based on time::")
   for h in zabbixServer.trigger.get(output=["triggerid","description","priority", "error"],expandData="1",expandDescription="1",lastChangeSince=sinceEpoch,lastChangeTill=tillEpoch,sortfield="priority",sortorder="DESC"):
      count += 1
      if not(summ):
         if h['priority'] == "1":
             print('"DESCRIPTION:" %s "PRIORITY:" INFORMATION ' % h['description'])
         elif h['priority'] == "2":
             print('"DESCRIPTION:" %s "PRIORITY:" WARNING ' % h['description'])
         elif h['priority'] == "3":
             print('"DESCRIPTION:" %s "PRIORITY:" AVERAGE ' % h['description'])
         elif h['priority'] == "4":
             print('"DESCRIPTION:" %s "PRIORITY:" HIGH ' % h['description'])
         elif h['priority'] == "5":
             print('"DESCRIPTION:" %s "PRIORITY:" DISASTER' % h['description'])
         else:
             print('"DESCRIPTION:" %s "PRIORITY:" OBD ' % h['description'])
   if summ:
      print ('Total count of triggers from %s to %s is: %s' % (sinceDate, tillDate, count)) 
   return


def reportTriggerPerHost( sinceEpoch, tillEpoch, summ, count, host, sinceDate, tillDate ):
   "this function process the time in EPOCH and provide with the result of triggers per host in calculated period of time"
   print("Report based on time::")
   for hostname in zabbixServer.hostinterface.get(output=["dns","ip","useip","hostid"],selectHosts=["host"],filter={"main":1,"type":1}):
      print('SERVER %s has IP %s and ID %s' % (hostname['hosts'][0]['host'], hostname['ip'], hostname['hostid']))
      print('=================================================================')
   
      for h in zabbixServer.trigger.get(output=["triggerid","description","priority", "error"],expandData="1",expandDescription="1",hostids=hostname['hostid'],lastChangeSince=sinceEpoch,lastChangeTill=tillEpoch,sortfield="priority",sortorder="DESC"):
         count += 1
         if not(summ):
            if h['priority'] == "1":
                print('"DESCRIPTION:" %s "PRIORITY:" INFORMATION ' % h['description'])
            elif h['priority'] == "2":
                print('"DESCRIPTION:" %s "PRIORITY:" WARNING ' % h['description'])
            elif h['priority'] == "3":
                print('"DESCRIPTION:" %s "PRIORITY:" AVERAGE ' % h['description'])
            elif h['priority'] == "4":
                print('"DESCRIPTION:" %s "PRIORITY:" HIGH ' % h['description'])
            elif h['priority'] == "5":
                print('"DESCRIPTION:" %s "PRIORITY:" DISASTER' % h['description'])
            else:
                print('"DESCRIPTION:" %s "PRIORITY:" OBD ' % h['description'])
      if summ:
         print('Total count of triggers from %s to %s is: %s' % (sinceDate, tillDate, count))
         count = 0
         print("") 
   return


def main(argv):
   "process command-line arguments"
   parser = argparse.ArgumentParser()
   parser.add_argument("-f", "--fromdate",required=True, help="from date")
   parser.add_argument("-t", "--todate",required=True, help="to date")
   parser.add_argument("-a", "--host", help="host based report", action="store_true")
   parser.add_argument("-s", "--summary", help="increase output verbosity",
                    action="store_true")
   args = parser.parse_args()
   fromTime = args.fromdate
   toTime = args.todate
   summ = args.summary
   hosts = args.host
   if (args.host) and (args.summary):
       newfrom=epoctime(fromTime)
       newto=epoctime(toTime)
       reportTriggerPerHost(newfrom, newto, summ, count, hosts, fromTime, toTime)
   elif args.host:
       newfrom=epoctime(fromTime)
       newto=epoctime(toTime)
       reportTriggerPerHost(newfrom, newto, summ, count, hosts, fromTime, toTime)
   elif args.summary:
       newfrom=epoctime(fromTime)
       newto=epoctime(toTime)
       reportTrigger(newfrom, newto, summ, count, fromTime, toTime)
   else:
       newfrom=epoctime(fromTime)
       newto=epoctime(toTime)
       reportTrigger(newfrom, newto, summ, count, fromTime, toTime)
   
if __name__ == "__main__":
   main(sys.argv[1:])

