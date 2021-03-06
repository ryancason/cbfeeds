# Carbon Black Feeds

## Overview

Carbon Black 4.0+ ships with support for threat intelligence feeds.  The Indicators of Compromise (IOCs) 
contained in the feeds are compared to the sensor data as it arrives on the server.  Any activity matching an 
IOC is tagged; users can search for the tags and, optionally, register for e-mail alerts.

Feeds allow Carbon Black servers to use freely available threat intelligence, proprietary customer threat data,
and provides a mechanism to feed threat indicators from on-premise analytic sources to Carbon Black for verification,
detection, visibility and analysis.

The Carbon Black 4.0+ server supports three types of indicators:

  * Binary MD5s
  * IPv4 addresses
  * DNS names

The feed format, described in the "Feed Structure" section below, is designed for simplicity.  This should make it
easy to add support for feed data from any input source.

Example feed creation scripts are included.  See the 'Examples' section in this document for a listing of the examples.

## Using the Carbon Black Feeds API

The Carbon Black Feeds API (CBFAPI) is found on github at:

  https://github.com/carbonblack/cbfeeds

The CBFAPI is a collection of documentation, example scripts, and a helper library to help create and validate Carbon
Black feeds.  It is not required in order to build a Carbon Black feed - a feed can be created in any language that
allows for building JSON, or even built by hand.  The feed file itself must match the feed structure, or schema, 
defined in the "Feed Structure" section below.

### Getting started with CBFAPI

#### install git as needed

    [root@localhost carbonblack]# yum install git
    ...

#### clone the github cbfeed repository:

    [root@localhost carbonblack]# git clone https://github.com/carbonblack/cbfeeds.git
    Initialized empty Git repository in /root/repos/carbonblack/cbfeeds/.git/
    remote: Reusing existing pack: 80, done.
    remote: Counting objects: 25, done.
    remote: Compressing objects: 100% (25/25), done.
    Receiving objects: 100% (105/105), 38.03 KiB | 17 KiB/s, done.
    Resolving deltas: 100% (50/50), done.
    remote: Total 105 (delta 10), reused 0 (delta 0)

#### navigate to the newly-created cbfeeds directory

    [root@localhost carbonblack]# ls
    cbfeeds
    [root@localhost carbonblack]# cd cbfeeds/
    [root@localhost cbfeeds]# ls
    cbfeeds  generate_feed_from_raw_iocs.py  generate_tor_feed.py  images  README.md  setup.py  validate_feed.py

#### use the example "generate_tor_feed.py" script to generate a feed from live tor egress IPs

    [root@localhost cbfeeds]# python generate_tor_feed.py example_tor_feed.feed
    [root@localhost cbfeeds]# ls -l example_tor_feed.feed 
    -rw-r--r--. 1 root root 2179084 Mar 25 08:09 example_tor_feed.feed

#### use the example "validate_feed.py" script to validate the tor feed (or a feed of your choosing)

    [root@localhost cbfeeds]# python validate_feed.py --feedfile example_tor_feed.feed 
    -> Validated that file exists and is readable
    -> Validated that feed file is valid JSON
    -> Validated that the feed file includes all necessary CB elements
    -> Validated that all element values are within CB feed 

## Feed Structure

* Feed: a Carbon Black feed
  * FeedInfo: Feed metadata: name, description, etc
  * Reports: a list of report
      * Report metadata: title, id, URL
      * IOCs for this report

A feed is a JSON structure with two entries:

* feedinfo 
* reports

The `feedinfo` structure is a list of basic feed metadata.   `reports` is a list of `report` structures.  
Each `report` has report metadata and a list of IOCs.  

### feedinfo 

`feedinfo` is a JSON structure with the following entries:

| name           | status   | description | 
| -------------- | -------- |-------------| 
| `name`         | REQUIRED | Internal name; must not include spaces or special characters.  See Notes. | 
| `display_name` | REQUIRED | Display name for the user interface. | 
| `provider_url` | REQUIRED | Human-consumpable link to view more information about this feed. | 
| `summary`      | REQUIRED | A short description of this feed. | 
| `tech_data`    | REQUIRED | More detailed technical description, to include data sharing requirements (if any) | 
| `icon`         | OPTIONAL | A base64 encoded version of the image to use in the user interface | 

Notes:

The 'name' field must not include spaces or special characters.  Typically, it should be unique per-feed on a single server.  

An example `feedinfo` structure, from the example_tor.py script:

```
  "feedinfo": {
    "provider_url": "http://www.dan.me.uk",
    "display_name": "Tor Exit Nodes",
    "name": "tor",
    "tech_data": "There are no requirements to share any data to receive this feed.",
    "summary": "This feed is a list of Tor Node IP addresses, updated every 30 minutes.",
    "version": 1,
    "icon": "...."
   }
```

### report

A `report` is a JSON structure with the following entries:

| name           | status   | description | 
| -------------- | -------- |-------------| 
| `timestamp`    | REQUIRED | Time this report was last updated, in seconds since epoch (GMT).  This should always be updated whenever the content of the report changes.| 
| `id`           | REQUIRED | A report id, must be unique per feed `name` for the lifetime of the feed.  Must be alphanumeric (including no spaces).| 
| `link`         | REQUIRED | Human-consumbable link to information about this report.| 
| `title`        | REQUIRED | A one-line title describing this report.| 
| `score`        | REQUIRED | The severity of this report from -100 to 100, with 100 most critical.| 
| `iocs`         | REQUIRED | The IOCs for this report.  A match on __any__ IOC will cause the activity to be tagged with this report id.  The IOC format is described below.| 

### iocs

CB 4.0 ships with feeds version `1` and supports three kinds of IOCs:

* IPv4 addresses
* domain names
* md5s

`iocs` is a structure with one or more of these entries:

| name           | status   | description | 
| -------------- | -------- |-------------| 
| `ipv4`         | OPTIONAL | A list of IPv4 addresses in dotted decimal form| 
| `dns`          | OPTIONAL | A list of domain names| 
| `md5`          | OPTIONAL | A list of md5s| 

An example `reports` list with two `report` structures, each with one IPv4 IOC, from the example_tor.py script:

```
  "reports": [
    {
      "timestamp": 1380773388,
      "iocs": {
        "ipv4": [
          "100.2.142.8"
        ]
      },
      "link": "https://www.dan.me.uk/tornodes",
      "id": "TOR-Node-100.2.142.8",
      "title": "As of Wed Oct  2 20:09:48 2013 GMT, 100.2.142.8 has been a TOR exit for 26 days, 0:44:42. Contact: Adam Langley <agl@imperialviolet.org>"
    },
    {
      "timestamp": 1380773388,
      "iocs": {
        "ipv4": [
          "100.4.7.69"
        ]
      },
      "link": "https://www.dan.me.uk/tornodes",
      "id": "TOR-Node-100.4.7.69",
      "title": "As of Wed Oct  2 20:09:48 2013 GMT, 100.4.7.69 has been a TOR exit for 61 days, 2:07:23. Contact: GPG KeyID: 0x1F40CBDC Jeremy <jeremy@acjlaw.net>"
    }
  ]
```
    
## Examples 

Several example scripts are included in the 'example' subdirectory.  These example scripts illustrate using the Carbon Black cbfeeds API to generate Carbon Black feeds from a variety of data sources.

| directory | name            | description | 
| --------- | --------------- | ------------|
| abuse_ch  | abuse.ch        | The Swiss security blog abuse.ch tracks C&C servers for Zeus, SpyEye and Palevo malware.|
| isight    | iSIGHT Partners | iSIGHT Partners customers can use their API key to generate a Carbon Black feed from iSIGHT Partners cyber threat intelligence.|
| mdl       | Malware Domain List | Malware Domain List is a non-commercial community project to track domains used by malware.|
| raw       | raw             | Build a Carbon Black feed from a raw list of IOCs.|
| tor       | Tor             | Provide a Carbon Black feed from a live list of Tor exit nodes provided by torproject.org| 
