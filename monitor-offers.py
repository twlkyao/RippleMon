#!/usr/bin/env python

from __future__ import division

import datetime
import decimal
import json
import re
import sys
import thread
import time
import websocket

""" Tool to monitor offers """

__author__      = "Hurukan"
__copyright__   = "Copyright 2013, XRP Talk"


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

    ws.send('{"command":"subscribe","streams":["transactions"]}')

### Message Event ###

def on_message(ws, message):

    # Message to JSON

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
    if ((transaction_type != 'OfferCreate') and (transaction_type != 'OfferCancel')):
        return False

    # Status

    if not 'engine_result_code' in json_message:
        return False

    if json_message['engine_result_code'] != 0:
        return False

    # Sequence

    if not 'Sequence' in json_message['transaction']:
        return False

    sequence = json_message['transaction']['Sequence']

    # OfferSequence

    offer_sequence = None

    if 'OfferSequence' in json_message['transaction']:
        offer_sequence = json_message['transaction']['OfferSequence']

    # Account

    if not 'Account' in json_message['transaction']:
        return False

    account = json_message['transaction']['Account']
    
    # TakerGets

    taker_gets_value = None
    taker_gets_value_str = None
    taker_gets_currency = None

    if  'TakerGets' in json_message['transaction']:

        # TakerGets - Value

        if 'value' in json_message['transaction']['TakerGets']:
            taker_gets_value = float(json_message['transaction']['TakerGets']['value'])
            taker_gets_value_str = format_numbers('%.6f', taker_gets_value)
        else:
            taker_gets_value = float(json_message['transaction']['TakerGets']) / 1000000
            taker_gets_value_str = format_numbers('%.6f', taker_gets_value)

        # TakerGets - Currency
            
        if 'currency' in json_message['transaction']['TakerGets']:
            taker_gets_currency = json_message['transaction']['TakerGets']['currency']
        else:
            taker_gets_currency = "XRP"

    # TakerPays

    taker_pays_value = None
    taker_pays_value_str = None
    taker_pays_currency = None

    if 'TakerPays' in json_message['transaction']:

        # TakerPays - Value

        if 'value' in json_message['transaction']['TakerPays']:
            taker_pays_value = float(json_message['transaction']['TakerPays']['value'])
            taker_pays_value_str = format_numbers('%.6f', taker_pays_value)
        else:
            taker_pays_value = float(json_message['transaction']['TakerPays']) / 1000000
            taker_pays_value_str = format_numbers('%.6f', taker_pays_value)

        # TakerPays - Currency

        if 'currency' in json_message['transaction']['TakerPays']:
            taker_pays_currency = json_message['transaction']['TakerPays']['currency']
        else:
            taker_pays_currency = "XRP"

    # Date

    if not 'date' in json_message['transaction']:
        return False

    date = int(json_message['transaction']['date']) + 946684800
    date_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(date))

    # Print

    if transaction_type == 'OfferCreate':
        print "[%s]{%s-%s} %s made offer to give %s %s for %s %s"      \
            % (date_str, transaction_type, sequence, account,
               taker_gets_value_str, taker_gets_currency, 
               taker_pays_value_str, taker_pays_currency)

    elif transaction_type == 'OfferCancel':
        print "[%s]{%s-%s} %s has cancelled offer #%s" \
            % (date_str, transaction_type, offer_sequence, account, offer_sequence)

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
        print "Usage: python monitor-offers.py [url]"
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

