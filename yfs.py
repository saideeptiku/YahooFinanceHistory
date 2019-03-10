""" get historical data

download link:
https://query1.finance.yahoo.com/v7/finance/download/GOOGL?period1=1549749596&period2=1552168796&interval=1d

page link:
https://finance.yahoo.com/quote/GOOGL/history?period1=0000000&period2=1552183545&interval=1d

"""

import requests
from time import time
import json
import os

# ######################################################################################################################
# Constants
# ######################################################################################################################

# go to page that shows history, used to get base cookies required for download
BASE_URL = "https://finance.yahoo.com/quote"

DOWNLOAD_URL = "https://query1.finance.yahoo.com/v7/finance/download"

HISTORY_PAGE = "history"

PAYLOAD = {
    'period1': int(),
    'period2': int(),
    'interval': '1d'
}

TICKER_SYMBOLS = ["AAPL", ]

SAVE_DIR = "history"


# ######################################################################################################################


#
# https://query1.finance.yahoo.com/v7/finance/download/GOOGL?period1=1549749596&period2=1552168796&interval=1d
# https://finance.yahoo.com/quote/GOOGL
# https://finance.yahoo.com/quote/GOOGL/history?period1=0000000&period2=1552183545&interval=1d
# https://query1.finance.yahoo.com/v7/finance/download/GOOGL?period1=1092895200&period2=1552114800&interval=1d&events=history
#

def mkdir_if_not_exist(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def drop_binary(binary_literal):
    """ fixes b'' in a string"""
    return str(binary_literal)[2:-1]


def is_json(my_json):
    """check if the object is JSON"""
    try:
        _ = json.loads(my_json)
    except ValueError:
        return False
    return True


def get_history_csv(ticker, start_time=00000000000, end_time=int(time()), download_dir=None, verbose=False):
    """
    Get the share history as a CSV
    :param download_dir:
    :param verbose:
    :param ticker: name of share ticker
    :param start_time: unix time
    :param end_time: unix time
    """
    if verbose:
        print("Getting", ticker, "...", end=" ")

    # # setup the base url
    # quote_url = BASE_URL + "/" + ticker + "/" + HISTORY_PAGE
    #
    # set up the time period
    PAYLOAD['period1'] = start_time
    PAYLOAD['period2'] = end_time
    #
    # # set up request
    # response = requests.get(quote_url, params=PAYLOAD)
    #
    # # save cookies for future use
    # cookie_jar = dict(response.cookies)

    # build download link
    csv_url = DOWNLOAD_URL + "/" + ticker

    # make download query
    response = requests.post(csv_url, params=PAYLOAD)  # , cookies=cookie_jar)

    # check if response is not a json error message
    if is_json(response.text):
        exit("ERROR RESPONSE")

    else:
        if download_dir is None:
            response.raw.decode_content = True
            print(response.text, file=open(SAVE_DIR + "/" + ticker + ".csv", "w"))
        else:
            mkdir_if_not_exist(download_dir)
            response.raw.decode_content = True
            print(response.text, file=open(download_dir + "/" + ticker + ".csv", "w"))

    if verbose:
        print("done.")


def main():
    get_history_csv(TICKER_SYMBOLS[0])


if __name__ == '__main__':
    main()
