import datetime
import json
from typing import Tuple, Any

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


def check_date(date: str):
    try:
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return False
    else:
        if (date - datetime.datetime.now()).days < 0 and date.year > 1998:
            return True
        else:
            return False


def pretty_printer(*args):
    if len(args) == 1:
        print(
            "______________",
            f"{args[0]}",
            "==============",
            sep="\n"
        )
    else:
        print(
            "______________",
            f"{args[0]}",
            "",
            f"{args[1]}",
            "==============",
            sep="\n"
        )


def parser():
    parser_args = argparse.ArgumentParser()
    parser_args.add_argument("currency_date", nargs="*", default=[])
    return parser_args.parse_args().currency_date


def modify_args() -> tuple[Any, str]:
    currency = None
    date = None
    args = parser()
    if len(args) == 0:
        pretty_printer("SystemError")
        sys.exit()
    else:
        currency = args[0].upper()  # проверка первого аргумента
        if check_currency(currency) == 0:
            pretty_printer(
                f"{currency}",
                f"Invalid currency name: {currency}"
            )
            sys.exit()

        if len(args) > 1:  # проверка втрого аргумента если он есть
            date = args[1]
            if check_date(date) == 0:
                pretty_printer(f"Invalid date {date}")
                sys.exit()

    formated_date = date.replace("-", "") if date else \
        datetime.datetime.today().strftime("%Y%m%d")
    # добавляем сегодня если не пришла дата с аргументов или форматируем для запоса пришедшую дату
    return currency, formated_date


def get_info():
    currency, date = modify_args()
    url = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/" \
          f"exchange?valcode={currency}&date={date}&json"
    response = requests.request("GET", url)
    info = json.loads(response.text)[0]
    rate = info.get("rate")
    pretty_printer(currency, rate)


if __name__ == '__main__':
    get_info()

# поработать с точками выхода с программы на аргументах
