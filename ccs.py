#!/usr/bin/python3

import requests
import json

url = "https://api.coinmarketcap.com/v1/ticker/?limit=10"
request = requests.get(url)
content = request.content.decode()

if request.status_code != 200:
    print("Somethings wrong. Turn on the bat signal.")
    exit()

header = ('Name', 'Symbol', 'Price(USD)', '1h % chg', '24h % chg', '7d % chg')
print('| %-20s | %-6s | %-10s | %-8s | %-9s | %-8s |' % header)

for i in json.loads(str(content)):
    data = (
        i['name'],
        i['symbol'],
        float(i['price_usd']),
        float(i['percent_change_1h']),
        float(i['percent_change_24h']),
        float(i['percent_change_7d']),
    )
    raw = '| %-20s | %-6s | %10.2f | %8.2f | %9.2f | %8.2f |'
    print(raw % data)


