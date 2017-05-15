import argparse
import json
import requests

#parser setup
description = 'Convert currency'
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
	help = 'returns raw Python dict')
	
parser.add_argument('-v', '--verbose',
	action = 'store_true',
	help = 'prints out unimportant stuff, opposite of silent')

#defs
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
	if raw is true, just whole dict is printed
	otherwise print formated JSON
	"""
	#build dict and input
	result = {}
	result['input'] = {}
	result['input']['amount'] = args.amount
	result['input']['currency'] = args.input
	#append output key depending if to print one or more currencies
	result['output'] = {}
	if isinstance(output, float): #print just one
		result['output'][args.output] = float('{0:.3f}'.format(output * args.amount))
	elif isinstance(output, dict): #print all
		for currency, value in output.items():
			result['output'][currency] = float('{0:.3f}'.format(value * args.amount))
	elif isinstance(output, str): #no calculation
		result['output'][args.output] = float('{0:.3f}'.format(args.amount))
	
	if raw:
		if args.verbose: print('returning raw dict')
		print(result)
	else:
		if args.verbose: print('returning prettified JSON')
		"""in Python 3.6 sorting is not needed, since we get the data in order
		for more info about why we can trust the order in dicts now see:
		https://www.youtube.com/watch?v=p33CVV29OG8"""
		print(json.dumps(result, indent=4, sort_keys=False))

def main(args):
	"""main logic of convert_currency.py"""
	#amount is not required, default is 1
	if args.amount is None:
		if args.verbose: print('WARNING: No amount provided, using value "1"')
		args.amount = 1
	
	#check if user is joking
	#if no input is provided, use EUR
	if args.input is None:
		if args.verbose:  print('WARNING: No input currency provided, using value "EUR"')
		args.input = 'EUR'
		#TODO print out only supported currencies
	elif args.input == args.output:
		print('ERROR: Input and Output arguments are same, no calculation done')
		calculate_print_output(amount=args.input, output=args.output, raw=args.raw)
		exit()
	
	#now we can get the currency_rates from fixer
	fixer_output = get_currency_rates(args.input)
	
	#if we got fixer_output, continue
	if fixer_output:
		#if no output is provided, lets calculate and print everything
		if args.output is None:
			if args.verbose: print('No output value provided converting to all known currencies, using base currency', args.input)
			calculate_print_output(amount=args.input, output=fixer_output['rates'], raw=args.raw)	
		#print out just the output, but check if output currency is valid first
		else:
			if any(args.output in currency for currency in fixer_output['rates'].keys()):
				calculate_print_output(amount=args.input, output=fixer_output['rates'][args.output], raw=args.raw)
			else:
				print('ERROR: Output currency', args.output, 'not supported.')
				print('Supported currencies are:',"|".join([currency for currency in fixer_output['rates'].keys()]))
	else:
		print('ERROR: failed to get currency_rates')
		calculate_print_output(output=None, raw=args.raw)
	
if __name__ == '__main__':
	args = parser.parse_args()
	main(args)