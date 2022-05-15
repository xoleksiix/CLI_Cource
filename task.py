import argparse
import datetime
import json
import requests

ALL_CURRENCY = ['NZD', 'LYD', 'XDR', 'LBP', 'XAG', 'ILS', 'JPY', 'RUB',
                'XAU', 'THB', 'AMD', 'BRL', 'GBP', 'VND', 'HKD', 'MDL',
                'BYN', 'KRW', 'MAD', 'AZN', 'TWD', 'ZAR', 'CAD', 'EUR',
                'DZD', 'TMT', 'CHF', 'MXN', 'TRY', 'CNY', 'AUD', 'KZT',
                'EGP', 'NOK', 'UZS', 'SEK', 'TJS', 'PKR', 'HRK', 'XPT',
                'SAR', 'XPD', 'IDR', 'DOP', 'RSD', 'GEL', 'MYR', 'IQD',
                'TND', 'BGN', 'HUF', 'DKK', 'CZK', 'INR', 'SGD', 'RON',
                'IRR', 'KGS', 'PLN', 'BDT', 'AED', 'USD']


def check_currency(currency: str, all_currency: list) -> bool:
    """
    Checking the value in the list of currencies.
    :param all_currency: list
    :param currency: str
    :return: bool
    """
    return currency in all_currency


def check_date(date: str) -> bool:
    """
    Checks the incoming string for the correct date.
    :param date: str
    :return: bool
    """
    try:
        # checks for correct date format "%Y-%m-%d"
        # and whether such a date exists, if not, an error is raised
        # and returns FALSE
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return False
    else:
        # checking for dates on a condition
        # through the delta is not a future date entered
        # or earlier than 1999 (the API does not support earlier dates)
        return (date - datetime.datetime.now()).days < 0 and date.year > 1998


def pretty_printer(*args):
    """
    Takes strings (one or two, ignores the rest) as arguments
    and prints them out wrapped in character lines.
    """
    frst_line, scnd_line = "______________", "=============="
    if len(args) == 1:
        print(frst_line, f"{args[0]}", scnd_line, sep="\n")
    else:
        print(frst_line, f"{args[0]}", "", f"{args[1]}", scnd_line, sep="\n")


def parser() -> tuple:
    """
    It accepts arguments from the command line. Returns a list.
    Empty if no arguments are received or [0]currency, [1]date.
    :return list:
    """
    parser_args = argparse.ArgumentParser()
    parser_args.add_argument("currency", nargs="?", default=None)
    parser_args.add_argument(
        "date", nargs="?",
        default=datetime.datetime.today().strftime("%Y-%m-%d")
    )
    return parser_args.parse_args().currency, parser_args.parse_args().date


def modify_args() -> tuple:
    """
    Checks the incoming arguments for a match.
    :return: tuple
    """
    currency, date = parser()
    if currency:
        currency = currency.upper()
        if check_currency(currency, ALL_CURRENCY) == 0:
            pretty_printer(
                f"{currency}",
                f"Invalid currency name: {currency}"
            )
            currency = None
        else:
            if check_date(date):
                date = datetime.datetime.today().strftime("%Y%m%d")
            else:
                pretty_printer(f"Invalid date {date}")
                date = None
    else:
        pretty_printer("SystemError")
    return currency, date


def get_info():
    """
    API request with formatted arguments from command line.
    """
    currency, date = modify_args()
    if currency and date:
        url = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/" \
              f"exchange?valcode={currency}&date={date}&json"
        response = requests.request("GET", url)
        if response.status_code != 200 or json.loads(response.text) == []:
            pretty_printer("SystemError")
        else:
            # getting a dictionary with data and course values by key
            info = json.loads(response.text)[0]
            rate = info.get("rate")
            pretty_printer(currency, rate)


if __name__ == '__main__':
    get_info()
