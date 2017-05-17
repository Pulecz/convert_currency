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
    def test_get_currency_rates(self):
        "test if get_currency_rates(base) returns dict, base is default EUR"
        self.assertIsInstance(convert_currency.get_currency_rates('EUR'), dict)

    def test_default_run(self):
        'simulates default arguments, when convert_currency is run without any parameters, , should end with 0'
        #amount,input,output,raw,verbose, unittest
        with self.assertRaises(SystemExit) as cm:
            NoParamaters = Args_for_convert_currency(1, None, None, False, False, True)
            self.assertTrue(convert_currency.main(NoParamaters))
        self.assertEqual(cm.exception.code, 0)

    def test_default_run(self):
        'simulates input as unsupported currency, should end with 1'
        #amount,input,output,raw,verbose, unittest
        with self.assertRaises(SystemExit) as cm:
            NoParamaters = Args_for_convert_currency(1, 'nonsense', None, False, False, True)
            self.assertTrue(convert_currency.main(NoParamaters))
        self.assertEqual(cm.exception.code, 1)

    def test_non_unique_font_run(self):
        'simulates input as $ which is non unique font, should end with 2'
        #amount,input,output,raw,verbose, unittest
        with self.assertRaises(SystemExit) as cm:
            NoParamaters = Args_for_convert_currency(1, '$', None, False, False, True)
            self.assertTrue(convert_currency.main(NoParamaters))
        self.assertEqual(cm.exception.code, 2)

    def test_negative_amount_run(self):
        'simulates default arguments, with negative ammount, should end with 3'
        #amount,input,output,raw,verbose, unittest
        NegativeAmountParamaters = Args_for_convert_currency(-1, None, None, False, False, True)
        with self.assertRaises(SystemExit) as cm:
            convert_currency.main(NegativeAmountParamaters)
        self.assertEqual(cm.exception.code, 3)

    def test_same_input_and_input_case_1(self):
        'same input and output 1, same country codes, should end with 4'
        #amount,input,output,raw,verbose, unittest
        with self.assertRaises(SystemExit) as cm:
            convert_currency.main(Args_for_convert_currency(100, 'UsD', 'uSd', False, False, True))
        self.assertEqual(cm.exception.code, 4)

    def test_same_input_and_input_case_2(self):
        'same input and output 2, same fonts of countries with unique font, should end with 4'
        #amount,input,output,raw,verbose
        with self.assertRaises(SystemExit) as cm:
            convert_currency.main(Args_for_convert_currency(100, 'Kn', 'kN', False, False, True))
        self.assertEqual(cm.exception.code, 4)

    def test_same_input_and_input_case_3(self):
        'same input and output 3, input country code, output unique font, should end with 4'
        #amount,input,output,raw,verbose
        with self.assertRaises(SystemExit) as cm:
            convert_currency.main(Args_for_convert_currency(100, 'HuF', 'fT', False, False, True))
        self.assertEqual(cm.exception.code, 4)

    def test_same_input_and_input_case_4(self):
        'same input and output 3, input unique font, output country code, should end with 4'
        #amount,input,output,raw,verbose
        with self.assertRaises(SystemExit) as cm:
            convert_currency.main(Args_for_convert_currency(100, 'myr', 'rm', False, False, True))
        self.assertEqual(cm.exception.code, 4)

    def test_validate_currency(self):
        'validate every supported currency, pass True to not print warnings'
        for currency_code in supported_currencies:
            self.assertIsInstance(convert_currency.validate_currency(currency_code, True), str)

    def test_validate_currency_non_unique_fonts(self):
        '''validate every supported currency font
        can\'t test non_unique currency_fonts because of exit 2
        pass True to not print warnings'''
        for currency_data in supported_currencies.values():
            if currency_data['font'] is None: continue
            try:
                self.assertIsInstance(convert_currency.validate_currency(currency_data['font'], True), str)
            except SystemExit:
                print(currency_data['font'], 'is non unique')
                continue

    #TODO
    def test_calculate_print_output_1(self):
        #tuple
        pass

    def test_calculate_print_output_2(self):
        #dict
        pass

    def test_calculate_print_output_3(self):
        #str
        pass

if __name__ == '__main__':
    unittest.main()
