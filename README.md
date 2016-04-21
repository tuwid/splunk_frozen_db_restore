# splunk_frozen_db_restore
Script to restore splunk frozen databases that containt events in a specific timeframe 


Usage:

    root@XXXXXX:~# python splunk_frozen_db_restore.py
    We're using the default index path, for custom indexes please adjust the path variable here
    Enter index:winevents_security
    Enter start date: (eg 30.12.2015): 31.12.2015
    Enter end date: (eg 30.12.2015): 01.01.2016
    [+] Searching dates on index winevents_security
    in /opt/splunk/var/lib/splunk/winevents_security/frozendb/
    1451516400
    1451602800
    Got 313 elements from /opt/splunk/var/lib/splunk/winevents_security/frozendb/
    Found : db_1452350660_1451453107_329
    [+] Copying databases into thaweddb..
    cp -R /opt/splunk/var/lib/splunk/winevents_security/frozendb/db_1452350660_1451453107_329 /opt/splunk/var/lib/splunk/winevents_security/thaweddb/
    [+] Rebuilding DBs
    splunkd fsck repair --one-bucket --include-hots --bucket-path=/opt/splunk/var/lib/splunk/winevents_security/thaweddb/db_1452350660_1451453107_329 --log-to--splunkd-log
    root@XXXXXX:~#