import requests
import json
from pprint import pprint
import os
username = input("Enter username:")
usersReq = requests.get(f"https://api.github.com/users/{username}")
user = json.loads(usersReq.text)
repos = requests.get(user["repos_url"])
parsed_json = json.loads(repos.text)

with open('data.json', 'w') as fp:
    json.dump(parsed_json, fp)

loaded_data = None
with open('data.json', 'r') as fp:
    loaded_data = json.load(fp)

pprint(f"Loaded from file: {loaded_data}")
os.remove("data.json")