# convert_currency
Convert currency using fixer.io

- when no parameters are provided script returns exchange rates for 1 EUR
- when no output parameter is provided, script returns all supported exchange rates

Please note that for example currency symbol "$" is used in many countries and in such cases script will want from you to provide specific country code.

Requires [requests module](http://docs.python-requests.org/en/master/) for sane working with HTTP.

# usage

  usage: convert_currency.py [-h] [-A AMOUNT] [-I INPUT] [-O OUTPUT] [-R] [-v]

  optional arguments:

    -h, --help            show this help message and exit
    -A AMOUNT, --amount AMOUNT
                          amount of money to convert
    -I INPUT, --input INPUT
                          input currency - 3 letters name or currency symbol
    -O OUTPUT, --output OUTPUT
                          output currency - 3 letters name or currency symbol
    -R, --raw             returns raw Python dict instead of formatted JSON
    -v, --verbose         prints out unimportant stuff, opposite of silent

# supported currencies

*$Currency Code - $Country and Currency - [$Font]
* AUD - Australia Dollar - [$]
* BGN - Bulgaria Lev - [лв]
* BRL - Brazil Real - [R$]
* CAD - Canada Dollar - [$]
* CHF - Switzerland Franc - [CHF]
* CNY - China Yuan Renminbi - [¥]
* CZK - Czech Republic Koruna - [Kč]
* DKK - Denmark Krone - [kr]
* EUR - Euro Member Countries - [€]
* GBP - United Kingdom Pound - [£]
* HKD - Hong Kong Dollar - [$]
* HRK - Croatia Kuna - [kn]
* HUF - Hungary Forint - [Ft]
* IDR - Indonesia Rupiah -[Rp]
* ILS - Israel Shekel -[₪]
* INR - India Rupee - [N\A]; Introduced July 2010 - no font information available at this time.
* JPY - Japan Yen - [¥]
* KRW - Korea (North\South) Won - [₩]
* MXN - Mexico Peso - [$]
* MYR - Malaysia Ringgit - [RM]
* NOK - Norway Krone - [kr]
* NZD - New Zealand Dollar - [$]
* PHP - Philippines Peso - [₱]
* PLN - Poland Zloty - [zł]
* RON - Romania New Leu - [lei]
* RUB - Russia Ruble - [₽]
* SEK - Sweden Krona - [kr]
* SGD - Singapore Dollar - [$]
* THB - Thailand Baht - [฿]
* TRY - Turkey Lira - [N\A]; Introduced March 2012 - no font information available at this time.
* USD - United States Dollar - [$]
* ZAR - South Africa Rand - [R]
