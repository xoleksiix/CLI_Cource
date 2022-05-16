import argparse
import datetime
import json
import requests


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


def modify_date(date: str) -> str or None:
    """
    Checks the date and formats it into
    the appropriate format for the request.
    If non-correct date return None.
    @param date: str
    @return: str or None
    """
    if check_date(date):
        return date.replace("-", "")
    else:
        pretty_printer(f"Invalid date {date}")
        return None


def get_data(date: str) -> list[dict]:
    """
    API requests with date params, returns data for the selected date
    with all available currencies.
    Returns an empty list if something went wrong.
    @param date: str
    @return: list of dicts
    """
    url = f"https://bank.gov.ua/NBUStatService/v1/statdirectory" \
          f"/exchange?date={date}&json"
    response = requests.request("GET", url)
    if response.status_code != 200 or json.loads(response.text) == []:
        pretty_printer("SystemError")
        return []
    else:
        return json.loads(response.text)


def get_info():
    currency, raw_date = parser()  # take
    date = modify_date(raw_date)  # modify date

    if currency and date:
        currency = currency.upper()
        data = get_data(date)
        if data:
            # search currency and rate in dicts
            rate = [
                i.get("rate") for i in data if
                i.get("cc") == currency
            ]
            if rate:
                # if found print currency and rate
                pretty_printer(currency, *rate)
            else:
                # if not found currency print error
                pretty_printer(
                    f"{currency}",
                    f"Invalid currency name: {currency}"
                )
    elif not currency:
        # if the currency did not come from the command line
        pretty_printer("SystemError")


if __name__ == '__main__':
    get_info()
