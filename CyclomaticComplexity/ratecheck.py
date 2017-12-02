import requests, json

r = requests.get('https://api.github.com/rate_limit')
json_data = json.loads(r.text)
print(json_data)
