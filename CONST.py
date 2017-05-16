# -*- coding: utf-8 -*-

supported_currencies = {
'AUD': {'country': 'Australia', 'currency': 'Dollar', 'font': '$'},
'BGN': {'country': 'Bulgaria', 'currency': 'Lev', 'font': 'лв'},
'BRL': {'country': 'Brazil', 'currency': 'Real', 'font': 'R$'},
'CAD': {'country': 'Canada', 'currency': 'Dollar', 'font': '$'},
'CHF': {'country': 'Switzerland', 'currency': 'Franc', 'font': 'CHF'},
'CNY': {'country': 'China', 'currency': 'Yuan Renminbi', 'font': '¥'},
'CZK': {'country': 'Czech Republic', 'currency': 'Koruna', 'font': 'Kč'},
'DKK': {'country': 'Denmark', 'currency': 'Krone', 'font': 'kr'},
'EUR': {'country': 'Euro Member Countries', 'currency': 'Euro', 'font': '€'},
'GBP': {'country': 'United Kingdom', 'currency': 'Pound', 'font': '£'},
'HKD': {'country': 'Hong Kong', 'currency': 'Dollar', 'font': '$'},
'HRK': {'country': 'Croatia', 'currency': 'Kuna', 'font': 'kn'},
'HUF': {'country': 'Hungary', 'currency': 'Forint', 'font': 'Ft'},
'IDR': {'country': 'Indonesia', 'currency': 'Rupiah', 'font': 'Rp'},
'ILS': {'country': 'Israel', 'currency': 'Shekel', 'font': '₪'},
'INR': {'country': 'India', 'currency': 'Rupee', 'font': None},
'JPY': {'country': 'Japan', 'currency': 'Yen', 'font': '¥'},
'KRW': {'country': 'Korea North\\South', 'currency': 'Won', 'font': '₩'},
'MXN': {'country': 'Mexico', 'currency': 'Peso', 'font': '$'},
'MYR': {'country': 'Malaysia', 'currency': 'Ringgit', 'font': 'RM'},
'NOK': {'country': 'Norway', 'currency': 'Krone', 'font': 'kr'},
'NZD': {'country': 'New Zealand', 'currency': 'Dollar', 'font': '$'},
'PHP': {'country': 'Philippines', 'currency': 'Peso', 'font': '$'},
'PLN': {'country': 'Poland', 'currency': 'Zloty', 'font': 'zł'},
'RON': {'country': 'Romania', 'currency': 'New Leu', 'font': 'lei'},
'RUB': {'country': 'Russia', 'currency': 'Ruble', 'font': '₽'},
'SEK': {'country': 'Sweden', 'currency': 'Krona', 'font': 'kr'},
'SGD': {'country': 'Singapore', 'currency': 'Dollar', 'font': '$'},
'THB': {'country': 'Thailand', 'currency': 'Baht', 'font': '฿'},
'TRY': {'country': 'Turkey', 'currency': 'Lira', 'font': None},
'USD': {'country': 'United States', 'currency': 'Dollar', 'font': '$'},
'ZAR': {'country': 'South Africa', 'currency': 'Rand', 'font': 'R'}}

#TODO have a function which will make all this based on supported_currencies
same_fonts={
"$" : ['Australia [AUD]', 'Canada [CAD]', 'Honk Kong [HKD]', 'Mexico [MXN]', 'New Zealand [NZD]', 'Philippines [PHP]', 'Singapore [SGD]', 'United States [USD]'],
"¥" : ['China [CNY]', 'Japan [JPY]'],
"kr" : ['Denmark [DKK]', 'Norway [NOK]', 'Sweden [SEK]']
}
