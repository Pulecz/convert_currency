import argparse
import json
import requests
import CONST

#parser setup
description = '''Convert currency using fixer.io
amount can be any non-negative float
input and output can be 3 letter currency code or currency symbol

when no parameters are provided script returns exchange rates for 1 EUR
when no output parameter is provided, script returns all supported exchange rates

please note that for example currency symbol "$" is used in many countries,
script will ask to provide specific country code in such cases.
'''
epilog = 'Enjoy!'
parser = argparse.ArgumentParser(description=description, epilog=epilog)

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

#defs
def validate_currency(user_input):
	"""Validates user_input based on data in CONST.py
	exits when user_input currency font is same for at least 2 countries
	otherwise returns currency_code if user_input is either currency_code or font
	"""
    #check if user_input is symbol for same currencies
	if user_input in [same_font for same_font in CONST.same_fonts]:
		print('Currency', user_input, 'is used in all these countries:')
		print('\n'.join(CONST.same_fonts[user_input]),'\nPlease try again and choose specific 3 letters long country code, the one in []')
		exit()
	#user provided country_code or unique font
	for currency_code, currency_data in CONST.supported_currencies.items():
		#if its country_code
		if user_input  == currency_code:
			return currency_code
		#if its unique_font
		elif currency_data['font'] == user_input:
			return currency_code

def get_currency_rates(base):
	"""
	returns json of currency rates using fixer.io which is taken from
	European Central Bank and updated daily at 4PM CET
	"""
	r = requests.get('https://api.fixer.io/latest?base=' + base)
	if r.ok: return r.json()

def calculate_print_output(amount = 1.0, output=None, raw=False):
	"""
	builds final output, input from args, output whatever dict
	if raw is true, print whole dict
	otherwise print formated JSON
	"""
	#build dict and input
	result = {}
	result['input'] = {}
	result['input']['amount'] = args.amount
	result['input']['currency'] = args.input

	#append output key depending if to print one or more currencies
	result['output'] = {}
	if isinstance(output, float): #output is exchange rate from fixer.io, add just one
		result['output'][args.output] = float('{0:.3f}'.format(output * args.amount))
	elif isinstance(output, dict): #output is all rates, add all
		for currency, value in output.items():
			result['output'][currency] = float('{0:.3f}'.format(value * args.amount))
	elif isinstance(output, str): #user provided same input and output, no calculation
		result['output'][args.output] = float('{0:.3f}'.format(args.amount))

	if raw:
		if args.verbose: print('returning raw dict')
		print(result)
	else:
		if args.verbose: print('returning prettified JSON')
		"""in Python 3.6 sorting keys is not needed, since we get the data in order
		for more info about why we can trust the order in dicts now see:
		https://www.youtube.com/watch?v=p33CVV29OG8"""
		print(json.dumps(result, indent=4, sort_keys=False))

def main(args):
	"""main logic of convert_currency.py
	validate input args, if they are ok or they are not provided
	use validate_currency() to get country_code
	then use get_currency_rates(country_code)
	then calculate_print_output() for one or all countries"""

	#validate amount
	##amount is not required, default is 1
	if args.amount is None:
		if args.verbose: print('WARNING: No amount provided, using value "1"')
		args.amount = 1
	#it can't be negative
	elif int(args.amount) < 0:
		print('ERROR: Won\'t calculate negative amount')
		exit()

	#validate input
	##if no input is provided, use EUR
	if args.input is None:
		if args.verbose:  print('WARNING: No input currency provided, using value "EUR"')
		args.input = 'EUR'
	##check if user provided same input and output currencies
	elif args.output is not None and args.input.upper() == args.output.upper():
		print('ERROR: Input and Output arguments are same, no calculation done')
		#pass output as user provided output, which is same as user provided input
		calculate_print_output(amount=args.input, output=args.output, raw=args.raw)
		exit()
	##check if its symbol or currency code and get country_code
	else:
		args.input = validate_currency(args.input.upper())

	#now we can get the currency_rates from fixer
	fixer_output = get_currency_rates(args.input)

	#if we got fixer_output, continue
	if fixer_output:
		#validate output
		##if no output is provided, lets calculate and print everything
		if args.output is None:
			if args.verbose: print('No output value provided converting to all known currencies, using base currency', args.input)
			#pass output as all exchange_rates
			calculate_print_output(amount=args.input, output=fixer_output['rates'], raw=args.raw)

		#otherwise print out just the output currency
		else:
			#check if its symbol or currency code and get country_code
			validated_args_output = validate_currency(args.output.upper())
			if validated_args_output is None:
				print('ERROR: Output currency', args.output, 'not supported.')
				print('Supported currencies are:',"|".join([currency for currency in fixer_output['rates'].keys()]))
			else:
				#pass output as choosen exchange_rate
				calculate_print_output(amount=args.input, output=fixer_output['rates'][validated_args_output], raw=args.raw)
	else:
		print('ERROR: failed to get currency_rates')
		calculate_print_output(output=None, raw=args.raw)

if __name__ == '__main__':
	args = parser.parse_args()
	main(args)
