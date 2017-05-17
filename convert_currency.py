#!/usr/bin/env python
import argparse
import json
import requests
from sys import exit as exit_with
from CONST import supported_currencies

#parser setup
description = '''Convert currency using http://fixer.io/

 - when no parameters are provided script returns exchange rates for 1 EUR
 - when no output parameter is provided, script returns all supported exchange rates

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
parser = argparse.ArgumentParser(description=description,
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog=epilog)

parser.add_argument('-A', '--amount',
	type = float,
	help = 'amount of money to convert')

parser.add_argument('-I', '--input',
	type = str,
	help = 'input currency - 3 letters name or currency symbol')

parser.add_argument('-O', '--output',
	type = str,
	help = 'output currency - 3 letters name or currency symbol')

parser.add_argument('-R', '--raw',
	action = 'store_true',
	help = 'returns raw Python dict instead of formatted JSON')

parser.add_argument('-v', '--verbose',
	action = 'store_true',
	help = 'prints out unimportant stuff, opposite of silent')

parser.add_argument('--unittest',
	action = 'store_true',
	help = 'only for unittest runs, doesn\'t print output')

#defs
def validate_currency(user_input, test):
	'''Validates user_input based on data in CONST.supported_currencies
	exits when user_input currency font is same for at least 2 countries
	otherwise returns currency_code if user_input is either currency_code or font
	'''

	def get_same_fonts(supported_currencies):
	    '''goes through supported_currencies dict
	    detects countries with same currency font
	    appends them to result

	    returns dict with key as a currency and list of countries (longer then 1)'''

	    result = {} #first dict
	    for currency_code, currency_data in supported_currencies.items():
	        result[currency_data['font']] = [] #create list for the currency font
	        #if some others country currency font is equal to the font being checked
	        for _currency_code, _currency_data in supported_currencies.items():
	            if currency_data['font'] == _currency_data['font']:
	                #append info about it
	                result[currency_data['font']].append('{0}({1}) [{2}]'.format(_currency_data['country'], _currency_data['currency'], _currency_code))

	    output = {} #second dict
	    #filter result for lists longer then 1 (nothing else then list is expected)
	    for key, value in result.items():
	        if len(value) > 1 and key is not None:
	            output[key] = value
	    return output

    #check if user_input is symbol for same currencies
	same_fonts = get_same_fonts(supported_currencies)
	for same_font in same_fonts:
		if user_input.lower() in same_font.lower():
			if not test:
				print('Currency', user_input, 'is used in all these countries:')
				print('\n'.join(same_fonts[same_font]),'\nPlease try again and choose specific 3 letters long country code, the one in []')
			exit_with(2)
	#user provided country_code or unique font
	for currency_code, currency_data in supported_currencies.items():
		#if its country_code, currency_code are always uppercase
		if user_input.upper() == currency_code:
			return currency_code
		#if its unique_font, always compare in lowercase
		elif currency_data['font'] is not None and currency_data['font'].lower() == user_input.lower():
			return currency_code

	print('ERROR: Currency', user_input, 'not supported.')
	print('Supported currencies are:','|'.join(currency for currency in supported_currencies.keys()))
	exit_with(1)

def get_currency_rates(base):
	'''
	returns json of currency rates using fixer.io which is taken from
	European Central Bank and updated daily at 4PM CET
	'''
	r = requests.get('https://api.fixer.io/latest?base=' + base)
	if r.ok: return r.json()

def calculate_print_output(amount=1.0, cinput=None, coutput=None, raw=False, verbose=False, test=False):
	'''
	builds final output, input from args, output whatever dict
	if raw is true, print whole dict
	otherwise print formated JSON
	'''
	#build dict and input
	result = {}
	result['input'] = {}
	result['input']['amount'] = amount
	result['input']['currency'] = cinput

	#append output key depending if to print one or more currencies
	result['output'] = {}
	if isinstance(coutput, tuple): #output is tuple of country_code and xchange rate from fixer.io, add just one
		result['output'][coutput[0]] = float('{0:.3f}'.format(coutput[1] * amount))
	elif isinstance(coutput, dict): #output is all rates, add all
		for currency, value in coutput.items():
			result['output'][currency] = float('{0:.3f}'.format(value * amount))
	elif isinstance(coutput, str): #user provided same input and output, no calculation
		result['output'][coutput] = float('{0:.3f}'.format(amount))

	if raw:
		if verbose: print('returning raw dict')
		if test:
			return result
		else:
			print(result)
	else:
		if verbose: print('returning prettified JSON')
		'''in Python 3.6 sorting keys should not be needed, since we get the data in order
		for more info about why we can "trust" the order in dicts now see:
		https://www.youtube.com/watch?v=p33CVV29OG8
        but for some reason EUR is moved is on the last pos when sorting is off,
		rather have it on'''
		if test:
			return json.dumps(result, indent=4, sort_keys=False)
		else:
			print(json.dumps(result, indent=4, sort_keys=False))

def main(args):
	'''main logic of convert_currency.py
	validate amount, if None, then default 1, can't be negative
	validate input args, if they are ok or they are not provided
	use validate_currency() to get country_code
	then use get_currency_rates(country_code)
	then calculate_print_output() for one or all countries'''

	#validate amount
	##amount is not required, default is 1
	if args.amount is None:
		if args.verbose: print('WARNING: No amount provided, using value "1"')
		args.amount = 1
	##its not none, but it can't be negative
	elif int(args.amount) < 0:
		print('ERROR: Won\'t calculate negative amount')
		exit_with(3)

	#prevalidate input/output - check if its symbol or currency code and get country_code
	#validate_currency() can cause exit when user provides symbol for multiple countries
	if args.input is not None:
		validated_args_input = validate_currency(args.input, args.unittest)
	elif args.input is None:
		##if no input is provided, use EUR
		if args.verbose: print('WARNING: No input currency provided, using value "EUR"')
		validated_args_input = 'EUR'

	if args.output is not None:
		validated_args_output = validate_currency(args.output, args.unittest)
		#check if user provided same input and output currencies
		if validated_args_input == validated_args_output:
			print('ERROR: Input and Output arguments are same, no calculation done')
			#pass output as user provided output, which is same as user provided input
			calculate_print_output(amount=args.amount, cinput=validated_args_input, coutput=validated_args_output, raw=args.raw, verbose=args.verbose, test=args.unittest)
			exit_with(4)

	#got validated_args_input and validated_args_output
	#now we can get the currency_rates from fixer
	fixer_output = get_currency_rates(validated_args_input)

	#if we got fixer_output, continue
	if fixer_output:
		if args.output is None:
			if args.verbose: print('No output value provided converting to all known currencies, using base currency', validated_args_input)
			#pass output as all exchange_rates
			calculate_print_output(amount=args.amount, cinput=validated_args_input, coutput=fixer_output['rates'], raw=args.raw, verbose=args.verbose, test=args.unittest)
			exit_with(0)
		#otherwise print out just the output currency
		else:
			calculate_print_output(amount=args.amount, cinput=validated_args_input, coutput=(validated_args_output, fixer_output['rates'][validated_args_output]), raw=args.raw, verbose=args.verbose, test=args.unittest)
			exit_with(0)
	else:
		print('ERROR: failed to get currency_rates')
		calculate_print_output(amount=args.amount, cinput=validated_args_input, coutput=None, raw=args.raw, verbose=args.verbose, test=args.unittest)
		exit_with(5)

if __name__ == '__main__':
	args = parser.parse_args()
	main(args)
