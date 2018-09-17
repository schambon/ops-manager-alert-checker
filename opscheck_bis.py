import requests
from requests.auth import HTTPDigestAuth
import argparse
import json
import sys

def check_alerts(args):
    alerts_r = requests.get("%s/api/public/v1.0/groups/%s/alerts" % (args.url, args.project), verify=args.cacert, auth=HTTPDigestAuth(args.username, args.key))
    alerts_r.raise_for_status()
    alerts_j = alerts_r.json()
    alerts = [ a for a in alerts_j["results"] if a["eventTypeName"] == args.eventTypeName ]

    if args.eventTypeName == "OUTSIDE_METRIC_THRESHOLD":
        alerts = [ a for a in alerts if a["metricName"] == args.metric ]

    for alert in alerts:
        if alert["eventTypeName"] == "OUTSIDE_METRIC_THRESHOLD":
            msg = "Metric: %s, value: %f %s" % (alert["metricName"], alert["currentValue"]["number"], alert["currentValue"]["units"])
        else:
            msg = alert["eventTypeName"]
        rs_name = alert["replicaSetName"] if "replicaSetName" in alert else "N/A"

        if "hostnameAndPort" in alert:
            host = alert["hostnameAndPort"].split(":")[0]
            
            if host == args.host:
                print(msg)
                sys.exit(args.severity)

        else:
            clusterId = alert["clusterId"]
            hosts_r = requests.get("%s/api/public/v1.0/groups/%s/hosts?clusterId=%s" % (args.url, args.project, clusterId), verify=args.cacert, auth=HTTPDigestAuth(args.username, args.key))
            hosts_r.raise_for_status()
            hosts_j = hosts_r.json()
            hosts = [ h["hostname"] for h in hosts_j["results"] ]

            if args.host in hosts:
                print(msg)
                sys.exit(args.severity)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ops Manager alert checker")
    required = parser.add_argument_group("Connection to Ops Manager")
    required.add_argument("--url", help="Ops Manager base url", required=True)
    required.add_argument("--username", help="Ops Manager user name (email)", required=True)
    required.add_argument("--key", help="API key to use", required=True)
    required.add_argument("--cacert", help="Path to CA certificate(s)", required=False)
    alert = parser.add_argument_group("Alert filter")
    alert.add_argument("--project", help="ProjectId to check", required=True)
    alert.add_argument("--host", help="Host to check for alerts", required=True)
    alert.add_argument("--eventTypeName", help="Event type that raised the alert", required=True)
    alert.add_argument("--metric", help="Metric (in case of OUTSIDE_METRIC_THRESHOLD")
    alert.add_argument("--severity", help="Integer code to return in case of alert (default: 2)", type=int, default=2)


    parsed_args = parser.parse_args()

    check_alerts(parsed_args)