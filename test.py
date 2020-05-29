import requests

headers={}

r = requests.get('https://api.fortnitetracker.com/v1/profile/psn/Brodio22')
r.json()
