import json, requests

url = 'http://api.sunrise-sunset.org/json'

params = dict(
    lat='57.70887',
    lng='11.97456',
    date='today'
)

resp = requests.get(url=url, params=params)
data = json.loads(resp.text)

print data