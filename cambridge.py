import requests
from bs4 import BeautifulSoup
import ssl
import re
import json
import sys
import os

# cancel authentication
ssl._create_default_https_context = ssl._create_unverified_context

# set header, host, geo
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}
url1 = "https://dictionary.cambridge.org/us/dictionary/english-chinese-simplified/"
url2 = ""
items = {"items": []}
entry_body_num = 0


def cambridge_search(word):
    global url1, url2
    url = url1 + str(word)
    try:
        html = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        return "request_error"
    bsObj = BeautifulSoup(html.content, "html.parser")
    entry_bodies = bsObj.findAll("div", {"class": "entry-body__el clrd js-share-holder"})
    for entry_body in entry_bodies:
        parse_entry_body(entry_body)
    return json.dumps(items)  # indent=2


def parse_entry_body(entry_body):
    global entry_body_num
    entry_body_num = entry_body_num + 1
    head_word = entry_body.find("span", {"class": "headword"}).get_text()
    pron_info = entry_body.findAll("span", {"class": "pron-info"})
    pron_info_uk = pron_info[0].findAll("span", recursive=False)[1].get_text()
    pron_info_us = pron_info[1].findAll("span", recursive=False)[1].get_text()
    pron_url_uk = pron_info[0].find("span", {"class": "circle circle-btn sound audio_play_button uk"}).attrs[
        "data-src-mp3"]
    pron_url_us = pron_info[1].find("span", {"class": "circle circle-btn sound audio_play_button us"}).attrs[
        "data-src-mp3"]
    os.system('curl ' + pron_url_uk + ' --output pron_uk' + str(entry_body_num) + '.mp3')
    os.system('curl ' + pron_url_us + ' --output pron_us' + str(entry_body_num) + '.mp3')
    add_item(title="UK:" + pron_info_uk + " US:" + pron_info_us,
             subtitle='Hold cmd to pronounce ' + head_word + ' in US', valid=True, arg=entry_body_num)
    sense_blocks = entry_body.findAll("div", {"class": "sense-block"})
    for sense_block in sense_blocks:
        subtitle = sense_block.find("h3")
        if subtitle is None:
            subtitle = ""
        else:
            subtitle = subtitle.get_text()
        for tran in sense_block.findAll("div", {"class": "def-block pad-indent"}):
            title = tran.find("span", {"class": "trans"}).get_text()
            add_item(title=re.sub(r'[\r\n\t]+', '', title), subtitle=re.sub(r'[\r\n\t]+', '', subtitle))


def add_item(title, subtitle, valid=False, arg=None):
    items["items"].append({"title": title, "subtitle": subtitle, "valid": valid, "arg": arg})


if __name__ == '__main__':
    # query = sys.argv[1]
    query = "name123"
    result = cambridge_search(query)
    title = "Search " + query + " in Cambridge English Dictionary..."
    if result == "{\"items\": []}":
        add_item(title=title, subtitle="Press Enter to open in Chrome", arg=query, valid=True)
        sys.stdout.write(str(items))
    else:
        sys.stdout.write(result)
