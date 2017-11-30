#!/usr/bin/python3

import requests
import json
import argparse


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Market statistics for cryptocurrencies.")
    parser.add_argument("coin_id", type=str, nargs='?', help="Provide coin name for individual coin stats.")

    if args:
        return parser.parse_args(args)
    return parser.parse_args()


def leaderboard():
    url = "https://api.coinmarketcap.com/v1/ticker/?limit=10"
    request = requests.get(url)
    
    if request.status_code != 200:
        print("Somethings wrong. Turn on the bat signal.")
        exit()
    
    header = ('Name', 'Symbol', 'Price(USD)', '1h % chg', '24h % chg', '7d % chg')
    print('| %-20s | %-6s | %-10s | %-8s | %-9s | %-8s |' % header)
    
    content = request.content.decode()
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


def individual_stats(coin_id):
    url = "https://api.coinmarketcap.com/v1/ticker/%s/" % coin_id
    request = requests.get(url)
    
    if request.status_code != 200:
        print("Somethings wrong. Turn on the bat signal.")
        exit()
    
    content = request.content.decode()
    for i in json.loads(str(content)):
        print('%-10s : %s' % ('Name', i['name']))
        print('%-10s : %s' % ('Symbol', i['symbol']))
        print('%-10s : %s' % ('Rank', i['rank']))
        print('%-10s : %s' % ('Price(USD)', i['price_usd']))
        print('%-10s : %s' % ('1h % chg', i['percent_change_1h']))
        print('%-10s : %s' % ('24h % chg', i['percent_change_24h']))
        print('%-10s : %s' % ('7d % chg', i['percent_change_7d']))


def main(args):
    if args.coin_id:
        individual_stats(args.coin_id)
    else:
        leaderboard()


if __name__ == "__main__":
    main(parse_args())
