import requests
from bs4 import BeautifulSoup
import ssl
import re
import json
import sys
import os

items = {"items": []}


def find_my_ip():
    global items
    # cancel authentication
    ssl._create_default_https_context = ssl._create_unverified_context
    # set header,url
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}
    url = "https://www.geoiptool.com/"
    try:
        html = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        return "request_error"
    bsObj = BeautifulSoup(html.content, "html.parser")
    print(bsObj)
    ip = bsObj.find("h2", {"id": "myip"}).get_text()
    info = bsObj.find("div", {"id": "info1"}).get_text()
    add_item(title=ip, subtitle=info)
    return json.dumps(items)  # indent=2


def add_item(title, subtitle, valid=False):
    items["items"].append({"title": title, "subtitle": subtitle, "valid": False, "text": {
        "copy": title,
        "largetype": title
    }})


if __name__ == '__main__':
    result = find_my_ip()
    if result == "{\"items\": []}":
        add_item(title="Cannot access 'www.whoisip.org' now", subtitle="Please check the internet ", valid=False)
        sys.stdout.write(str(items))
    else:
        sys.stdout.write(result)
