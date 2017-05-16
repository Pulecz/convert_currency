#!/usr/bin/env python
import convert_currency
import unittest

class Args_for_convert_currency:
    'simulate Namespace class for argsparse with all arguments convert_currency takes'
    def __init__(self, amount, user_input, output, raw, verbose):
        self.amount = amount
        self.input = user_input
        self.output = output
        self.raw = raw
        self.verbose = verbose

class TestStringMethods(unittest.TestCase):
    '''main TestCases'''
    def test_get_currency_rates(self):
        "test if get_currency_rates(base) returns dict, base is default EUR"
        self.assertIsInstance(convert_currency.get_currency_rates('EUR'), dict)

    def test_default_run(self):
        'simulates default arguments, when convert_currency is run without any parameters'
        #amount,input,output,raw,verbose
        NoParamaters = Args_for_convert_currency(1, None, None, False, False)
        self.assertIsNone(convert_currency.main(NoParamaters))

    #TODO all these tests will dl from fixer, io, no need to test that, let it download once and use it later for all

    #probably all supported currencies and no output

    #random or all combinations(1024) supported currency for input and output, probably separate test

    #negative amount

    #same input and output 1, same country codes

    #same input and output 2, same fonts of countries with unique font

    #same input and output 3, input country code, output unique font

    #same input and output 3, input unique font, output country code

    #do for for all supported country_codes and unique fonts
    def test_validate_currency():
        pass

    def test_validate_currency_non_unique_fonts():
        pass

    def test_calculate_print_output_1():
        #tuple
        pass

    def test_calculate_print_output_2():
        #dict
        pass

    def test_calculate_print_output_3():
        #str
        pass

if __name__ == '__main__':
    unittest.main()
