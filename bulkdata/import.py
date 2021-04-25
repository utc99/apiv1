import csv 
import json 
import requests
import sys

API_ENDPOINT = "http://127.0.0.1:5000/api/users"

if len(sys.argv) != 2:
  print("Usage: .\import.py source.csv")
  sys.exit(2)

source = sys.argv[1]

jsonArray = []
      
#Read csv file
with open(source, encoding='utf-8') as csvf: 

    csvReader = csv.DictReader(csvf) 

    for row in csvReader: 
        jsonArray.append(row)

for item in jsonArray:

    r = requests.post(url = API_ENDPOINT, json=item)
    pastebin_url = r.text
    print("The pastebin URL is:%s"%pastebin_url)