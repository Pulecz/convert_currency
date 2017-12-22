#!/usr/bin/env python
import argparse
import requests
import sys
import CONST


def main():
    args = parse_args(sys.argv[1:])

    # may cause exit 1
    args = validate_args(args)
    
    # may cause exit 5
    fixer_io_rates = get_currency_rates(args.input)['rates']
    calculate_and_print(args, fixer_io_rates)
   

def parse_args(argv):
    "parser expected to have argv as sys.argv[1:], for tests"
    description = '''Convert currency using http://fixer.io/

     - when no parameters are provided script returns exchange rates for 1 EUR
     - when no output parameter is provided:
           script returns all supported exchange rates
     - unsupported output currencies are ignored

    amount can be any non-negative float
    input and output can be 3 letter currency code or currency symbol'''
    epilog = '''
    exit codes:
    0 - all ok
    1 - user provided unsupported currency
    2 - user provided non unique currency font
    3 - user provided negative amount
    4 - user provided same currencies, no conversion happened
    5 - failed to get exchange_rates from fixer.io

    source @ https://github.com/Pulecz/convert_currency'''
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog)

    parser.add_argument(
        'amount', type=float,
        help='amount of money to convert')

    parser.add_argument(
        'input', type=str,
        help='input currency - 3 letters name or currency symbol')

    parser.add_argument(
        'output',
        nargs='*',
        type=str,
        help='output currency - 3 letters name or currency symbol')

    parser.add_argument(
        '-R', '--raw', action='store_true',
        help='returns raw Python dict instead of formatted JSON')

    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='prints out unimportant stuff, opposite of silent')

    parser.add_argument(
        '--unittest', action='store_true',
        help='only for unittest runs, doesn\'t print output')

    return parser.parse_args(argv)


#TODO currency font support


def validate_args(args):
    """validates user input"""
    validated = True
    # INPUT
    if not any(args.input in supported_currency \
               for supported_currency in CONST.supported_currencies.keys()):
                validated = False
    # OUTPUT 
    if args.output:
        if args.input in args.output:  # input is not in fixer['rates']
            while args.input in args.output:  # for multiple duplicated inputs in output
                args.output.remove(args.input)
    # remove unsupported
    args.output = [supported_currency for supported_currency in \
                       CONST.supported_currencies.keys() if supported_currency in args.output]
    
    # FINALLY
    #if args.output[0] == args.input:
    #    print('<>')
    if validated:
        return args
    else:
        print('ERROR: Currency', args.input, 'not supported.')
        print('Supported currencies are:',
              '|'.join(currency \
                  for currency in CONST.supported_currencies.keys()))
        sys.exit(1)


def get_currency_rates(base):
    '''
    returns json of currency rates using fixer.io which is taken from
    European Central Bank and updated daily at 4PM CET
    '''
    r = requests.get('https://api.fixer.io/latest?base=' + base)
    if r.ok:
        return r.json()
    else:
        sys.exit(5)


def calculate_and_print(args, rates):
    """takes rates dict from fixer, filters if needed, print raw or nice"""
    # TODO print raw or nice
    payload = {}
    if args.output:  # filter for wanted currencies
        for curr in args.output:
            payload[curr] = float('{0:.3f}'.format(rates[curr] * args.amount))
    else:  # return all 
        for curr, value in rates.items():
            payload[curr] = float('{0:.3f}'.format(value * args.amount))
    print(payload)

    
if __name__ == '__main__':
    main()
