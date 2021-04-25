#Export data from API to csv file
import csv 
import json 
import requests
import sys

if len(sys.argv) != 2:
  print("Usage: .\import.py destination.csv")
  sys.exit(2)
  
destination = sys.argv[1]

API_ENDPOINT = "http://127.0.0.1:5000/api/users"

#Get all users
r = requests.get(url = API_ENDPOINT)
json_data = r.json()

users_data = json_data["users"]

data_file = open(destination, 'w', newline='')
csv_writer = csv.writer(data_file)

#Counter for header
count = 0
  
for user in users_data:

    #Remove ids
    if 'id' in user:
            del user['id']

    #Add header
    if count == 0:
        header = user.keys()
        csv_writer.writerow(header)
        count += 1
        
    #Add user data to csv
    csv_writer.writerow(user.values())
  
data_file.close()