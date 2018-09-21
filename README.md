Ops Manager Alert Checker
=========================


This scripts connects to MongoDB Ops Manager and extracts all alerts that are raised and match some basic criteria (mostly alert type and project tag). For each alert found, it calls the provided command line. This is typically useful to raise alerts in other, corporate alerting / monitoring systems like Nagios, Centreon etc.

Two versions are provided:

- opscheck.py: check alerts and run a command for all alerts found
- opscheck_bis.py: check alerts on a host and return a status code (0 for no alert, non-0 for alerts)

Usage
=====

opscheck.py
-----------

```bash
usage: opscheck.py [-h] --url URL --username USERNAME --key KEY
                   [--command COMMAND] --eventTypeName EVENTTYPENAME
                   [--metric METRIC] [--tag TAG]

Ops Manager alert checker

optional arguments:
  -h, --help            show this help message and exit

Required arguments:
  --url URL             Ops Manager base url
  --username USERNAME   Ops Manager user name (email)
  --key KEY             API key to use
  --command COMMAND     Command to run ($node, $msg, $rs will be substituted)

Alert filter:
  --eventTypeName EVENTTYPENAME
                        Event type that raised the alert
  --metric METRIC       Metric (in case of OUTSIDE_METRIC_THRESHOLD
  --tag TAG             Restrict to groups with tag
```

opscheck_bis.py
---------------

```bash
usage: opscheck_bis.py [-h] --url URL --username USERNAME --key KEY
                       [--cacert CACERT] --project PROJECT --host HOST
                       --eventTypeName EVENTTYPENAME [--metric METRIC]
                       [--severity SEVERITY]

Ops Manager alert checker

optional arguments:
  -h, --help            show this help message and exit

Connection to Ops Manager:
  --url URL             Ops Manager base url
  --username USERNAME   Ops Manager user name (email)
  --key KEY             API key to use
  --cacert CACERT       Path to CA certificate(s)

Alert filter:
  --project PROJECT     ProjectId to check
  --host HOST           Host to check for alerts
  --eventTypeName EVENTTYPENAME
                        Event type that raised the alert
  --metric METRIC       Metric (in case of OUTSIDE_METRIC_THRESHOLD
  --severity SEVERITY   Integer code to return in case of alert (default: 2)
```
  
Examples
========

Check host node1.vagrant.dev for HOST_DOWN alert:
```python opscheck_bis.py --url https://opsmgr:8443 --username admin@localhost.com --key XXXX --cacert /etc/pki/cacert.crt --project <projectid> --host node1.vagrant.dev --eventTypeName HOST_DOWN```
  
