import requests
from bs4 import BeautifulSoup
from datetime import timedelta, date
import ssl
import json

# disable https
ssl._create_default_https_context = ssl._create_unverified_context

# set header, host, geo
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}
host = "http://twitter.com/"

# the default geo is corresponding to new york
geo = "geocode%3A40.730610%2C73.935242%2C3km%20"
spry = "&src=spry"
since = None
until = None
data_max_position = ""
since_prefix = "%20since%3A"
until_prefix = "%20until%3A"
streaming_num = 0
tweet_count = 0
start_date = None
end_date = None


def get_html(first=False):
    global since, until, data_max_position
    proxies = {
        "http": "http://35.198.34.142:80",
        "https": "http://35.198.34.142:80",
    }
    if first:
        url = host + "search?q=" + geo + since_prefix + since + until_prefix + until + spry
    else:
        url = host + "i/search/timeline?vertical=default&q=" + geo + since_prefix + since + until_prefix + until + spry + "&include_available_features=1&include_entities=1&lang=en&max_position=" + data_max_position.replace(
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
    global since, until
    filename = since + " to " + until + ".json"
    with open(filename, 'a') as outfile:
        for tweet in tweet_list:
            # json.dump(tweet, outfile)
            outfile.write(json.dumps(tweet))
            outfile.write('\n')
        outfile.close()


def open_first_html():
    global data_max_position, streaming_num, tweet_count
    streaming_num = 0
    tweet_count = 0
    bsObj = get_html(first=True)
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
        tweet["timestamp_ms"] = header.find("span", {"class": "_timestamp js-short-timestamp "}).attrs["data-time-ms"]
        tweet["fullname"] = header.find("span", {"class": "FullNameGroup u-textTruncate"}).get_text().encode("ascii",
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
        if response['new_latent_count'] == 0:
            break


def daterange(start, end):
    for n in range(int((end - start).days)):
        yield start + timedelta(n)


def set_geo(latitude, longitude, radius):
    global geo
    geo = "geocode%3A" + str(latitude) + "%2C" + str(longitude) + "%2C" + str(radius) + "km%20"


def set_date(start_y, start_m, start_d, end_y, end_m, end_d):
    global start_date, end_date
    start_date = date(start_y, start_m, start_d)
    end_date = date(end_y, end_m, end_d)


def start_scraping():
    global start_date, end_date, since, until
    for single_date in daterange(start_date, end_date):
        since = single_date.strftime("%Y-%m-%d")
        until = (single_date + timedelta(1)).strftime("%Y-%m-%d")
        print(since + " to " + until)
        open_first_html()
        streaming()


if __name__ == '__main__':
    set_geo(40.730610, -73.935242, 5)
    set_date(2016, 5, 29, 2016, 5, 31)
    start_scraping()

# print(html['has_more_items'])
