import urllib2
import json
import csv
import os
import io
import requests


def create_json_file(viewID, schema="faostat-test"):
    url = "http://faostat3.fao.org/faostat-browse-dbms/rest/parametric/nosql/get/view/"
    q = {
        "schema": schema,
        "viewID": viewID
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    print "request"

    try:
        r = requests.post(url, data=q, headers=headers)
        obj = open('json/' + viewID + ".json", 'wb')
        t = r.text.encode('ascii', 'ignore')
        print t
        obj.write(t)
        obj.close
    except Exception, e:
        print e


def create_json_groups():
    url_getgroups = "http://faostat3.fao.org/wds/rest/groups/faostat2/E"
    results = requests.get(url_getgroups)
    # print results.text
    cached = []
    for r in json.loads(results.text):
        if r[0] not in cached:
            cached.append(r[0])

    for r in cached:
        create_json_file(r)

def create_json_domains():
    url_getgroupsandomains = "http://faostat3.fao.org/wds/rest/groupsanddomains/faostat2/E"
    results = requests.get(url_getgroupsandomains)
    for r in json.loads(results.text):
        create_json_file(r[2])


def create_rankings():
    views = ["rankings_view",
             "commodities_by_regions",
             "commodities_by_country",
             "countries_by_commodity",
             "commodities_by_regions_imports",
             "commodities_by_country_imports",
             "major_commodities_imports",
             "commodities_by_regions_exports",
             "commodities_by_country_exports",
             "	major_commodities_exports"
    ]
    for v in views:
        create_json_file(v)

def create_aggregation_json():
    url = "http://faostat3.fao.org/testingjson"
    q = {}
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    r = requests.post(url, data=q, headers=headers)
    obj = open('json/aggregation_selector.json', 'wb')
    print r.text
    t = r.text.encode('ascii', 'ignore')
    print t
    obj.write(t)
    obj.close


create_aggregation_json()
#create_json_file("country_view")
#create_json_file("browse_by_domain_structure")
#create_rankings()
#create_json_groups()
#create_json_domains()





