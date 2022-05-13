import datetime
import json
import requests
import argparse


def available_currency() -> set:
    """
    Makes a request with a list of all available currencies
    at the current moment and takes the key from the dictionary to the set.
    :return: set
    """
    all_currency = set()
    response = requests.request(
        "GET",
        "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
    )
    for i in json.loads(response.text):
        all_currency.add(i.get("cc"))
    return all_currency


def check_currency(currency: str) -> bool:
    """
    Checking the value in the list of currencies.
    :param currency: str
    :return: bool
    """
    if currency in available_currency():
        return True
    else:
        return False


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
        if (date - datetime.datetime.now()).days < 0 and date.year > 1998:
            return True
        else:
            return False


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


def parser() -> list:
    """
    It accepts arguments from the command line. Returns a list.
    Empty if no arguments are received or [0]currency, [1]date.
    :return list:
    """
    parser_args = argparse.ArgumentParser()
    parser_args.add_argument(
        "currency_date", nargs="*", default=[],
        help="input currency"
             "and optional date. "
             "format <XYZ(currency code USD/etc.) yyyy-mm-dd>"
    )
    return parser_args.parse_args().currency_date


def modify_args() -> tuple:
    """
    Checks the incoming arguments for a match, if there are no arguments
    or the argument does not match.
    Returns None (except for the date,
    the date is returned today if there is a currency)
    :return: tuple
    """
    args = parser()
    if len(args) == 0:
        pretty_printer("SystemError")
        return None, None
    else:
        currency = args[0].upper()  # checking the first argument
        if check_currency(currency) == 0:
            pretty_printer(
                f"{currency}",
                f"Invalid currency name: {currency}"
            )
            currency = None

        if len(args) > 1:  # checking the second argument if it exists
            date = args[1]
            if check_date(date) == 0:
                pretty_printer(f"Invalid date {date}")
                date = None
            else:
                date = date.replace("-", "")
            # date in a format suitable for the request
        else:
            date = datetime.datetime.today().strftime("%Y%m%d")
            # add today if the date has not get

        return currency, date


def get_info():
    """
    API request with formatted command line arguments.
    """
    currency, date = modify_args()
    if None not in [date, currency]:                        # check for data
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
