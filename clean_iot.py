import datetime
import csv
import re

file = open('files/iot/iot_all_serial.csv', 'r')
num_format = re.compile('\d+')
lines = file.readlines()
dict = {}
for line in lines[1:]:
    # 0:epoch  4:fw  5:bw   6:element id
    num_list = num_format.findall(line)
    date = datetime.datetime.fromtimestamp(int(num_list[0])).strftime('%Y-%m-%d %H:%M:%S')[:13]
    if date in dict:
        dict[date]["fw"].append(int(num_list[4]))
        dict[date]["bw"].append(int(num_list[5]))
    else:
        dict[date] = {"fw": [int(num_list[4])], "bw": [int(num_list[5])]}

dict_avg = {}
for key in dict:
    dict_avg[key] = {"fw": 0, "bw": 0}
    dict_avg[key]["fw"] = sum(dict[key]["fw"])
    dict_avg[key]["bw"] = sum(dict[key]["bw"])

with open('files/iot/iot_count.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["date", "hour", "fw", "bw"])
    for key, value in dict_avg.items():
        writer.writerow([key[:10], key[11:13], int(value["fw"]), int(value["bw"])])
