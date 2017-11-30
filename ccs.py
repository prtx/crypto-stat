#!/usr/bin/python3

import requests
import json
import argparse


RED    = "\033[1;31m"  
GREEN  = "\033[0;32m"
NORMAL = "\033[0;0m"
BOLD   = "\033[;1m"


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Market statistics for cryptocurrencies.")
    parser.add_argument("coin_id", type=str, nargs='?', help="Provide coin name for individual coin stats.")

    if args:
        return parser.parse_args(args)
    return parser.parse_args()


def color_value(value):
    color = NORMAL
    if value > 0: color = GREEN
    if value < 0: color = RED

    return color, value, NORMAL


def check(request):
    if request.status_code != 200:
        print("Something went wrong. Turn on the bat signal.")
        exit()


def leaderboard():
    url = "https://api.coinmarketcap.com/v1/ticker/?limit=10"
    request = requests.get(url)
    check(request)    
   
    header = (BOLD, 'Name', 'Symbol', 'Price(USD)', '1h % Chg', '1d % Chg', '7d % Chg', NORMAL,)
    print('%s| %-20s | %-6s | %-10s | %-8s | %-8s | %-8s |%s' % header)
    
    content = request.content.decode()
    for i in json.loads(str(content)):
        data = (
            i['name'],
            i['symbol'],
            float(i['price_usd']),
            *color_value(float(i['percent_change_1h'])),
            *color_value(float(i['percent_change_24h'])),
            *color_value(float(i['percent_change_7d'])),
        )
        raw = '| %-20s | %-6s | %10.2f | %s%8.2f%s | %s%8.2f%s | %s%8.2f%s |'
        print(raw % data)


def individual_stats(coin_id):
    url = "https://api.coinmarketcap.com/v1/ticker/%s/" % coin_id
    request = requests.get(url)
    check(request)    
    
    content = request.content.decode()
    for i in json.loads(str(content)):
        print('%-10s : %s%s%s' % ('Name', BOLD, i['name'], NORMAL))
        print('%-10s : %s' % ('Symbol', i['symbol']))
        print('%-10s : %s' % ('Rank', i['rank']))
        print('%-10s : %s' % ('Price(USD)', i['price_usd']))
        print('%-10s : %s%f%s' % ('1h % Chg', *color_value(float(i['percent_change_1h']))))
        print('%-10s : %s%f%s' % ('1d % Chg', *color_value(float(i['percent_change_24h']))))
        print('%-10s : %s%f%s' % ('7d % Chg', *color_value(float(i['percent_change_7d']))))


def main(args):
    print(BOLD)
    print("Cryptocurrency Statistics:".upper())
    print(NORMAL)

    if args.coin_id:
        individual_stats(args.coin_id)
    else:
        leaderboard()


if __name__ == "__main__":
    main(parse_args())
