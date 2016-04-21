#!/usr/bin/python
import os
import time
from subprocess import call

# to run this in the backgroun you either use screen or 
#chmod+x splunk_frozen_db_restore.py
#nohup /path/to/splunk_frozen_db_restore.py & 


path = '/opt/splunk/var/lib/splunk/'
splunkbin = '/opt/splunk/bin/'
debug = 0

print "We're using the default index path, for custom indexes please adjust the path variable here"
print "Uncomment the system calls at the end for the actual execution "
# TODO: check for root here ?

index = raw_input('Enter index:').rstrip('\n')
#index='winevents_security'
if debug:
  print 'Index : ' + index


frozenpath = path + index + '/frozendb/'
if debug:
  print 'Frozenpath : ' + frozenpath

d1 = raw_input('Enter start date: (eg 30.12.2015): ')
#  TODO: regex here for validation
d2 = raw_input('Enter end date: (eg 30.12.2015): ')
##  TODO: regex here for validation
##  TODO: check of end > start (duuhhh )
if debug:
  print 'Date1 and Date2 : ' + d1 + ' ' + d2 

print '[+] Searching dates on index ' + index
print 'in ' + frozenpath
try:
  frozen_list = os.listdir(frozenpath)
except:
  print "[-] Unable to walk index directory, check if path exists : " + path + index + '/frozendb/' 
  exit(1)

if debug:
  print 'Frozen List ' + frozen_list

try:
  start_date = int(time.mktime(time.strptime(d1 + " 00:00:00", "%d.%m.%Y %H:%M:%S")));
  #start_date = int(time.mktime(time.strptime('31.12.2015' + " 00:00:00", "%d.%m.%Y %H:%M:%S")));
except:
  print "[-] Incorrect date inserted"
  exit(1)
try:
  end_date = int(time.mktime(time.strptime(d2 + " 00:00:00", "%d.%m.%Y %H:%M:%S")));
  #end_date = int(time.mktime(time.strptime('01.01.2016' + " 00:00:00", "%d.%m.%Y %H:%M:%S")));
except:
  print "[-] Incorrect date inserted"
  exit(1)

#t1 = int(time.mktime(time.strptime('31.12.2015' + " 00:00:00", "%d.%m.%Y %H:%M:%S")));
#t2 = int(time.mktime(time.strptime('01.01.2016' + " 00:00:00", "%d.%m.%Y %H:%M:%S")));
print start_date
print end_date

print "Got " + str(len(frozen_list)) + " elements from " + frozenpath 

restore_list = []

for line in frozen_list:
  tmp = line.split('_')
  t1 = int(tmp[2])
  t2 = int(tmp[1])
  # additional check here as it can produce potential errors
  
  if ( (start_date >= t1 and end_date >= t2 and start_date <= t1 ) or ( start_date >= t1 and end_date <= t2) or ( start_date <= t1 and end_date >= t2) or ( start_date <= t1 and end_date <= t2 and end_date >= t1)):
  #if((start_date in range(start_date,end_date)) or end_date in range(start_date,end_date) ):
    print 'Found : ' + line
    restore_list.append(line)

if len(restore_list) == 0:
  print 'List empty, nothing found..'
  exit(1)

print "[+] Copying databases into thaweddb.."

for db in restore_list:
  if debug:
    print "Executing: " + "cp -R " + frozenpath + db + " " + path + index + "/thaweddb/" 
  #call(["cp","-R " + frozenpath + db + " " + path + index + "/thaweddb/"])

print "[+] Rebuilding DBs"
for db in restore_list:
  if debug:
    print "Executing: " + splunkbin +  "splunkd fsck  repair --one-bucket --include-hots --bucket-path=" + path + index + "/thaweddb/" + db + " --log-to--splunkd-log"
  #call([splunkbin + "splunkd", "fsck  repair --one-bucket --include-hots --bucket-path=" + path + index + "/thaweddb/" + db + " --log-to--splunkd-log"])
