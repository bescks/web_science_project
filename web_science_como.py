from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import datetime
import random
import ssl
import re
import sys
import json

# cancel authentication
ssl._create_default_https_context = ssl._create_unverified_context



# set header, host, geo
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/62.0.3202.94 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}
host = "http://twitter.com/"
spry = "&src=typd"
data_max_position = ""
streaming_num = 0
tweet_count = 0


def get_html(first=False):
    global data_max_position
    if first:
        url = "https://twitter.com/search?f=tweets&vertical=place&q=place%3Acd661902b07eb657%20since%3A2016-5-28&src=typd"
    else:
        url = "https://twitter.com/i/search/timeline?f=tweets&vertical=place&q=place%3Acd661902b07eb657%20since%3A2016-5-28&include_available_features=1&include_entities=1&max_position=" + data_max_position.replace(
            "=", "%3D") + "&reset_error_state=false"
    try:
        html = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        return e
    if first:
        return BeautifulSoup(html.content, "html.parser")
    else:
        return html.content.decode("utf-8")


def save_json_list(tweet_list):
    for tweet in tweet_list:
        date = datetime.datetime.fromtimestamp(int(tweet['timestamp_ms'])).strftime('%Y-%m-%d')
        filename = "tweets/" + date + ".json"
        with open(filename, 'a') as outfile:
            outfile.write(json.dumps(tweet))
            outfile.write('\n')
            outfile.close()


def open_first_html():
    global data_max_position, streaming_num, tweet_count
    streaming_num = 0
    tweet_count = 0
    bsObj = get_html(first=True)
    print(bsObj)
    data_max_position = bsObj.findAll("div", {"class": "stream-container "})[0].attrs['data-max-position']
    tweet_list = get_tweet_list(bsObj)
    print(str(len(tweet_list)) + " tweets in the first html.")
    tweet_count = tweet_count + len(tweet_list)
    save_json_list(tweet_list)


def get_tweet_list(bsObj):
    results = bsObj.findAll("li", {"class": "js-stream-item stream-item stream-item "})
    tweet_list = []
    for result in results:
        tweet = {}
        header = result.find("div", {"class": "stream-item-header"})
        tweet["timestamp"] = header.find("a", {"class": "tweet-timestamp js-permalink js-nav js-tooltip"}).attrs[
            "title"]
        timestamp = header.find("span", {"class": "_timestamp js-short-timestamp "})
        if timestamp is not None:
            tweet["timestamp_ms"] = timestamp.attrs["data-time"]
        else:
            tweet["timestamp_ms"] = \
                header.find("span", {"class": "_timestamp js-short-timestamp js-relative-timestamp"}).attrs["data-time"]
        tweet["fullname"] = header.find("span", {"class": "FullNameGroup u-textTruncate"}).get_text().encode(
            "ascii",
            "ignore").decode(
            "utf-8")
        tweet["username"] = header.find("span", {"class": "username u-dir"}).get_text().encode("ascii",
                                                                                               "ignore").decode("utf-8")
        tweet["content"] = result.find("div", {"class": "js-tweet-text-container"}).get_text().encode("ascii",
                                                                                                      "ignore").decode(
            "utf-8")
        tweet_list.append(tweet)
    return tweet_list


def streaming():
    global data_max_position, streaming_num, tweet_count
    while True:
        response = json.loads(get_html())
        data_max_position = response['min_position']
        bsObj = BeautifulSoup(response['items_html'], "html.parser")
        tweet_list = get_tweet_list(bsObj)
        tweet_count = tweet_count + len(tweet_list)
        streaming_num = streaming_num + 1
        print("stream " + str(streaming_num) + ": " + str(len(tweet_list)) + " tweets" + ", " + str(
            tweet_count) + " tweets in total, new_latent_count is " + str(
            response['new_latent_count']))
        save_json_list(tweet_list)
        # if response['new_latent_count'] == 0:
        #    break


open_first_html()
streaming()
