import sys
import os
import csv
import time
import shlex
import urlparse

from datetime import datetime
from datetime import timedelta

# third part lib imports
import requests

from distutils.version import StrictVersion
if StrictVersion(requests.__version__) < StrictVersion("1.2.3"):
    # only in 1.2.3+ did response objects support iteration 
    raise ImportError("requires requests >= 1.2.3")

# our imports
sys.path.insert(0, "../../")
from cbfeeds import CbReport
from cbfeeds import CbFeed
from cbfeeds import CbFeedInfo

def get_zeus():
    reports = []
    r = requests.get("https://zeustracker.abuse.ch/blocklist.php?download=domainblocklist")
    lines = r.text.split("\n")
    domains = []
    for line in lines:
        if len(line) < 3: continue
        if line[0] == "#": continue

        domains.append(line.strip())

    fields = {'iocs': {
                        "dns": domains,
                      },
              'timestamp': int(time.mktime(time.gmtime())),
              'link': "https://zeustracker.abuse.ch/blocklist.php?download=domainblocklist",
              'id': 'abusech-zeus',
              'title': 'abuse.ch Zeus hit on Standard domain blocklist',
              'score': 50,
            }
    reports.append(CbReport(**fields))
    return reports

def get_palevo():
    reports = []
    r = requests.get("https://palevotracker.abuse.ch/blocklists.php?download=domainblocklist")
    lines = r.text.split("\n")
    domains = []
    for line in lines:
        if len(line) < 3: continue
        if line[0] == "#": continue

        domains.append(line.strip())

    fields = {'iocs': {
                        "dns": domains,
                      },
              'timestamp': int(time.mktime(time.gmtime())),
              'link': "https://palevotracker.abuse.ch/blocklists.php?download=domainblocklist",
              'id': 'abusech-palevo',
              'title': 'abuse.ch Palevo hit on domain blocklist',
              'score': 50,
            }
    reports.append(CbReport(**fields))
    return reports

def get_spyeye():
    reports = []
    r = requests.get("https://spyeyetracker.abuse.ch/blocklist.php?download=domainblocklist")
    lines = r.text.split("\n")
    domains = []
    for line in lines:
        if len(line) < 3: continue
        if line[0] == "#": continue

        domains.append(line.strip())

    fields = {'iocs': {
                        "dns": domains,
                      },
              'timestamp': int(time.mktime(time.gmtime())),
              'link': "https://spyeyetracker.abuse.ch/blocklist.php",
              'id': 'abusech-spyeye',
              'title': 'abuse.ch SpyEye hit on domain blocklist',
              'score': 50,
            }
    reports.append(CbReport(**fields))
    return reports

def create():
    reports = []
    reports.extend(get_zeus())
    reports.extend(get_palevo())
    reports.extend(get_spyeye())
   
    feedinfo = {'name': 'abusech',
                'display_name': "abuse.ch Malware Domains",
                'provider_url': "http://www.abuse.ch",
                'summary': "abuse.ch tracks C&C servers for Zeus, SpyEye and Palevo malware. " + 
                           "This feed combines the three domain names blocklists.",
                'tech_data': "There are no requirements to share any data to receive this feed.",
                "icon": "abuse.ch.jpg"
                }

    # the lazy way to the icon 
    old_cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    feedinfo = CbFeedInfo(**feedinfo)
    feed = CbFeed(feedinfo, reports)
    bytes = feed.dump()

    os.chdir(old_cwd)

    return bytes

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "usage: generte_abushch_feed.py [outfile]"
        sys.exit()

    bytes = create()
    open(sys.argv[1], "w").write(bytes)

