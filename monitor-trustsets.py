#!/usr/bin/env python

""" Tool to monitor trustsets """

__author__      = "Hurukan"
__copyright__   = "Copyright 2013, XRP Talk"


from __future__ import division

import datetime
import json
import re
import sys
import time
import websocket


###########
# Formats #
###########

### Set a comma in a number ###

def commafy(s):
    r = []
    for i, c in enumerate(reversed(s)):
        if i and (not (i % 3)):
            r.insert(0, ',')
        r.insert(0, c)
    return ''.join(r)

### Delete trailing zeros in a number ###

def del_zeros(num):
    if num.find('.') == -1:
        return num
    j=0
    for c in reversed(num):
        if c == '0':
            j = j + 1
        elif c == '.':
            j = j + 1
            break;
        else:
            break
    if j == 0:
        return num
    return num[:-j]

### Format Numbers/Values ###

re_digits_nondigits = re.compile(r'\d+|\D+')

def format_numbers(format, value):
    parts = re_digits_nondigits.findall(format % (value,))
    for i in xrange(len(parts)):
        s = parts[i]
        if s.isdigit():
            parts[i] = commafy(s)
            break
    return del_zeros(''.join(parts))


###############
# Web sockets #
###############

### Open Event ###

def on_open(ws):

    # Subscribe to the Transactions Stream

    ws.send('{"command":"subscribe","streams":["transactions"]}')

### Message Event ###

def on_message(ws, message):

    # Message converted to JSON

    try:
        json_message = json.loads(message)
    except Exception, e:
        print "[on_message]{exception}: %s" % e

    # Transaction

    if not 'transaction' in json_message:
        return False

    # Transaction Type

    if not 'TransactionType' in json_message['transaction']:
        return False

    transaction_type = json_message['transaction']['TransactionType']
    if transaction_type != 'TrustSet':
        return False

    # Engine Result Code

    if not 'engine_result_code' in json_message:
        return False

    engine_result_code = json_message['engine_result_code']
    if engine_result_code != 0:
        return False

    # Account

    if not 'Account' in json_message['transaction']:
        return False

    account = json_message['transaction']['Account']

    # Amount 

    if not 'LimitAmount' in json_message['transaction']:
        return False

    if not 'value' in json_message['transaction']['LimitAmount']:
        return False

    limit_amount = float(json_message['transaction']['LimitAmount']['value'])
    limit_amount_str = format_numbers('%.6f', limit_amount)

    # Currency

    if not 'currency' in json_message['transaction']['LimitAmount']:
        return False

    currency = json_message['transaction']['LimitAmount']['currency']

    # Issuer

    if not 'issuer' in json_message['transaction']['LimitAmount']:
        return False

    issuer = json_message['transaction']['LimitAmount']['issuer']

    # Date 

    if not 'date' in json_message['transaction']:
        return False

    date = int(json_message['transaction']['date']) + 946684800
    date_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(date))

    # Print

    print "[%s] %s has trusted %s for %s %s" % (date_str, account, issuer, limit_amount_str, currency)
    sys.stdout.flush()

    return True

### Error Event ###

def on_error(ws, error):

    print "[on_error] %s" % error

### Close Event ###

def on_close(ws):

    pass


########
# Main #
########

if __name__ == "__main__":

    # Usage

    if len(sys.argv) != 2:
        print "Usage: python monitor-trustsets.py [url]"
        print "    -> wss://s1.ripple.com:51233/"
        print "    -> wss://s2.ripple.com:51233/"
        sys.exit(1)

    # Web Sockets

    try:
        ws = websocket.WebSocketApp(sys.argv[1],
                                    on_open = on_open,
                                    on_message = on_message,
                                    on_error = on_error,
                                    on_close = on_close)
        ws.run_forever()

    except Exception, e:
        print "[main]{exception}: %s" % e

