Ops Manager Alert Checker
=========================


This scripts connects to MongoDB Ops Manager and extracts all alerts that are raised and match some basic criteria (mostly alert type and project tag). For each alert found, it calls the provided command line. This is typically useful to raise alerts in other, corporate alerting / monitoring systems like Nagios, Centreon etc.

