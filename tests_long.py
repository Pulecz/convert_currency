#!/usr/bin/env python
import convert_currency
import unittest
from CONST import supported_currencies

class Args_for_convert_currency:
    'simulate Namespace class for argsparse with all arguments convert_currency takes'
    def __init__(self, amount, user_input, output, raw, verbose, unittest):
        self.amount = amount
        self.input = user_input
        self.output = output
        self.raw = raw
        self.verbose = verbose
        self.unittest = unittest

class TestStringMethods(unittest.TestCase):
    '''main TestCases'''

    def test_all_possible_runs_with_None_output(self):
        '''
        go over each currency_code and print output for all
        since input is always different, request from API is needed in each run
        therefore we can just run the main with different input parameter for each country_code
        and test that it returns 0
        '''
        print('Starting test for all supported input currencies:\n')
        tests = len(supported_currencies)
        for test, currency_code in enumerate(supported_currencies):
            print('Testing {} | Test #{} out of {}'.format(currency_code, test + 1, tests))
            #amount,input,output,raw,verbose, unittest
            with self.assertRaises(SystemExit) as cm:
                convert_currency.main(Args_for_convert_currency(1, currency_code, None, False, False, True))
            self.assertEqual(cm.exception.code, 0)

    def test_all_possible_combinations(self):
        '''go over each currency_code, take it as input
        request exchange_rates for current input country_code
        then run it over each _currency_code as output
        testing if calculate_print_output returns output with tested output currency and its float
        with current CONSTS, it should be 32*32 - 32(overlapping countries) tests'''

        print('Starting test for all possible combinations:\n')
        #for input
        tests = len(supported_currencies)**2 - len(supported_currencies)
        inverted_count = tests
        for currency_code in supported_currencies:
            #get the exchange_rates for current input
            fixer_output = convert_currency.get_currency_rates(currency_code)
            #for output
            for _currency_code in supported_currencies:
                if currency_code == _currency_code: continue
                print('Testing -I {} -O {} | Test #{} out of {}'.format(currency_code, _currency_code, (inverted_count * -1) + tests + 1, tests))
                #amount,input,output,raw,verbose, unittest
                validated_args_output = convert_currency.validate_currency(_currency_code, True)
                output = convert_currency.calculate_print_output(amount=1,
                 cinput=convert_currency.validate_currency(currency_code, True),
                 coutput=(validated_args_output, fixer_output['rates'][validated_args_output]),
                 raw=True,
                 verbose=False,
                 test=True)
                self.assertIsInstance(output['output'][_currency_code], float)
                inverted_count -= 1

if __name__ == '__main__':
    unittest.main()
