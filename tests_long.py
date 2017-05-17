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
    #TODO all these tests will dl from fixer, io, no need to test that, let it download once and use it later for all
    #would require inject it to the main or simulate main here
    #long tests for now, sorry fixer.io API

    def test_all_possible_runs_with_None_output(self):
        '''go over each currency_code and print output for all'''
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
        then run it over each _currency_code as output
        with current CONSTS, it should be 32*32 - 32(overlapping countries)'''
        print('Starting test for all possible combinations:\n')
        #for input
        tests = len(supported_currencies)**2 - len(supported_currencies)
        inverted_count = tests
        for currency_code in supported_currencies:
            #for output
            for _currency_code in supported_currencies:
                if currency_code == _currency_code: continue
                print('Testing -I {} -O {} | Test #{} out of {}'.format(currency_code, _currency_code, (inverted_count * -1) + tests + 1, tests))
                #amount,input,output,raw,verbose, unittest
                with self.assertRaises(SystemExit) as cm:
                    convert_currency.main(Args_for_convert_currency(1, currency_code, _currency_code, False, False, True))
                self.assertEqual(cm.exception.code, 0)
                inverted_count -= 1

if __name__ == '__main__':
    unittest.main()
