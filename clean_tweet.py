import json
import datetime
import csv

file = open('sum.json', 'r')
lines = file.readlines()
jsons = []
i = 0
for line in lines:
    i += 1
    jsons.append(json.loads(line))  # 读取第一行

count = {}
for json in jsons:
    date = datetime.datetime.fromtimestamp(int(json['timestamp_ms']) / 1000).strftime('%Y-%m-%d')
    if date in count:
        count[date] = count[date] + 1
    else:
        count[date] = 1

with open('tweets_count.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Date", "tweet_count"])
    for key, value in count.items():
        writer.writerow([key, value])
