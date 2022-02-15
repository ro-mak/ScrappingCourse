import requests
import json
from pprint import pprint
import os

organizationsReq = requests.get("https://api.github.com/organizations")
organizations = json.loads(organizationsReq.text)
repos = [requests.get(organizations[0]["repos_url"])]
parsed_json = json.loads(repos[0].text)

with open('data.json', 'w') as fp:
    json.dump(parsed_json, fp)

loaded_data = None
with open('data.json', 'r') as fp:
    loaded_data = json.load(fp)

pprint(f"Loaded from file: {loaded_data}")
os.remove("data.json")