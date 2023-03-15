import csv
import json

dict = {}
counter = 0
with open('coords.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in spamreader:
        lat = float(row[0])
        lon = float(row[1])
        dict[str(counter)] = {}
        dict[str(counter)]["lat"] = lat
        dict[str(counter)]["lon"] = lon 
        print([lat,lon])
        counter = counter + 1

with open("coords.json", "w") as outfile:
    json.dump(dict, outfile)