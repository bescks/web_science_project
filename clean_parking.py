from os import listdir
from os.path import isfile, join
from datetime import datetime
import re
import csv

files = [f for f in listdir("files/parking") if isfile(join("files/parking", f))]
free = re.compile('\d+')
date = re.compile('[\w]{3}\s[0-9]{2}\s[0-9]{4}\s\d+:\d+:\d+')
for filename in files:
    file = open('files/parking/' + filename, 'r')
    print('open', filename)
    free_dict = {}
    for line in file.readlines():
        date_str = datetime.strptime(date.findall(line)[0], '%b %d %Y %H:%M:%S').strftime('%Y-%m-%d %H')
        free_num = int(free.findall(line)[1])
        if date_str in free_dict:
            free_dict[date_str].append(free_num)
        else:
            free_dict[date_str] = [free_num]

    count_dict = {}
    for key, item in free_dict.items():
        count_dict[key] = int(sum(item) / len(item))
    print('saving', filename)
    with open('files/parking/' + filename[:-4] + '.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["date","hour", filename[:-4]])  # write header
        for key, value in count_dict.items():
            writer.writerow([key[:-3],key[-2:], value])
