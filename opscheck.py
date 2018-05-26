import requests
from requests.auth import HTTPDigestAuth
import argparse
import json
import subprocess

def check_alerts(args):
    groups_r = requests.get(args.url + "/api/public/v1.0/groups", auth=HTTPDigestAuth(args.username, args.key))
    groups_r.raise_for_status()
    groups_j = groups_r.json()

    if args.tag != None:
        groups = [ r["id"] for r in groups_j["results"] if args.tag in r["tags"]]
    else:
        groups = [ r["id"] for r in groups_j["results"] ]

    for group in groups:
        alerts_r = requests.get(args.url + "/api/public/v1.0/groups/" + group + "/alerts", auth=HTTPDigestAuth(args.username, args.key))
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
                
                command = args.command.replace("$node", host)
                command = command.replace("$msg", msg)
                command = command.replace("$rs", rs_name)
                subprocess.call(command, shell=True)
            else:
                clusterId = alert["clusterId"]
                hosts_r = requests.get(args.url + "/api/public/v1.0/groups/" + group + "/hosts?clusterId=" + clusterId, auth=HTTPDigestAuth(args.username, args.key))
                hosts_r.raise_for_status()
                hosts_j = hosts_r.json()
                hosts = [ h["hostname"] for h in hosts_j["results"] ]
                for host in hosts:
                    command = args.command.replace("$node", host)
                    command = command.replace("$msg", msg)
                    command = command.replace("$rs", rs_name)
                    subprocess.call(command, shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ops Manager alert checker")
    required = parser.add_argument_group("Required arguments")
    required.add_argument("--url", help="Ops Manager base url", required=True)
    required.add_argument("--username", help="Ops Manager user name (email)", required=True)
    required.add_argument("--key", help="API key to use", required=True)
    required.add_argument("--command", help="Command to run ($node, $msg, $rs will be substituted)")
    alert = parser.add_argument_group("Alert filter")
    alert.add_argument("--eventTypeName", help="Event type that raised the alert", required=True)
    alert.add_argument("--metric", help="Metric (in case of OUTSIDE_METRIC_THRESHOLD")
    alert.add_argument("--tag", help="Restrict to groups with tag")

    parsed_args = parser.parse_args()

    check_alerts(parsed_args)