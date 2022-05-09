import datetime
import json
import requests
import argparse
import sys


def available_currency() -> set:
    all_currency = set()
    response = requests.request(
        "GET",
        "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
    )
    for i in json.loads(response.text):
        all_currency.add(i.get("cc"))
    return all_currency


def check_currency(currency: str) -> bool:
    if len(currency) == 3 and currency.isalpha():
        if currency in available_currency():
            return True
        else:
            return False
    else:
        return False


def valid_date(date):
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return False
    else:
        return True


def check_date(date: str):
    if valid_date(date) and int(date.split("-")[0]) > 1998:
        return True
    else:
        return False


def parser():
    parser_args = argparse.ArgumentParser()
    parser_args.add_argument("currency_date", nargs="*", default=[])
    return parser_args.parse_args().currency_date


def modify_args() -> list:
    args = parser()
    if len(args) == 0:
        print("SystemError")
        sys.exit()
    else:
        currency = args[0].upper() #проверка первого аргумента
        if check_currency(currency) == 0:
            print(f"Invalid currency name: {currency}")
            sys.exit()

        if len(args) > 1: #проверка втрого аргумента если он есть
            date = args[1]
            if check_date(date) == 0:
                print(f"Invalid date {date}")
                sys.exit()

        else:
            date = datetime.datetime.today().strftime("%Y-%m-%d")
            # добавляем сегодня если не пришла дата с аргументов
    return currency, date


if __name__ == '__main__':
    currency, date = modify_args()
    print(currency, date)
    check_currency(currency)
