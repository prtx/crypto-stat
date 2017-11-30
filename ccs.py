#!/usr/bin/python3

import requests
import json
import argparse


RED    = "\033[1;31m"  
GREEN  = "\033[0;32m"
YELLOW = "\033[0;33m"
NORMAL = "\033[0;0m"
BOLD   = "\033[;1m"


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Market statistics for cryptocurrencies.")
    parser.add_argument("coin_id", type=str, nargs='?', help="Provide coin name for individual coin stats.")
    
    sort_group = parser.add_mutually_exclusive_group()
    sort_group.add_argument("-p", "--price-sort", action="store_true", help="Sort by Price(USD)")
    sort_group.add_argument("-hr", "--hourly-sort", action="store_true", help="Sort by Hourly %% Change")
    sort_group.add_argument("-day", "--daily_sort", action="store_true", help="Sort by Daily %% Change")
    sort_group.add_argument("-wk", "--weekly-sort", action="store_true", help="Sort by Weekly %% Change")

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
        print("%sSomething went wrong. Turn on the bat signal.%s" % (YELLOW, NORMAL))
        exit()


def leaderboard(sort_key=None):
    url = "https://api.coinmarketcap.com/v1/ticker/?limit=10"
    request = requests.get(url)
    check(request)    
   
    header = (BOLD, 'Name', 'Symbol', 'Price(USD)', '1h % Chg', '1d % Chg', '7d % Chg', NORMAL,)
    raw_str = '| %-20s | %-6s | %10.2f | %s%8.2f%s | %s%8.2f%s | %s%8.2f%s |'
    print('%s| %-20s | %-6s | %-10s | %-8s | %-8s | %-8s |%s' % header)
    
    content = request.content.decode()
    data = []
    for i in json.loads(str(content)):
        data.append((
            i['name'],
            i['symbol'],
            float(i['price_usd']),
            *color_value(float(i['percent_change_1h'])),
            *color_value(float(i['percent_change_24h'])),
            *color_value(float(i['percent_change_7d'])),
        ))
    
    if sort_key: data.sort(key=lambda x: x[sort_key], reverse=True)
    for row in data:
        print(raw_str % row)


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
        sort_key = None
        if args.price_sort:  sort_key = 2
        if args.hourly_sort: sort_key = 4
        if args.daily_sort:  sort_key = 7
        if args.weekly_sort: sort_key = 10
        leaderboard(sort_key)
    
    print()


if __name__ == "__main__":
    main(parse_args())
