# -*- coding: utf-8 -*-

print "Start"

import requests;
import argparse;
import xml.etree.ElementTree as ET
import utils

# Command line
parser = argparse.ArgumentParser(description='Connects to CME IM API.')
parser.add_argument('--login', type=str, required=True)
parser.add_argument('--password', type=str, required=True)
args = parser.parse_args()
print 'Login: '+args.login
print 'Password: '+args.password

#Setup
baseURL = 'https://cmecorenr.cmegroup.com/MarginServiceApi'
headers = {"Content-type": "application/xml",
		"Accept": "application/xml",
		"username": args.login,
		"password": args.password}

#As this is just a sample to be later used in node-red we hardcode portfolio id
portfolioId = '8462179'

#utils.enableHTTPLogging()

utils.listPortfolios(baseURL=baseURL, headers=headers)

#utils.addTrades(baseURL=baseURL, headers=headers)

marginId = utils.requestMarginCalculation(portfolioId=portfolioId, baseURL=baseURL, headers=headers)

#Get Calculated Margin
[im, vm] = utils.getMargin(marginId=marginId, baseURL=baseURL, headers=headers)

marginId = utils.requestIncrementalMarginCalculation(portfolioId=portfolioId, baseURL=baseURL, headers=headers)

#Get Calculated Margin
[im, vm] = utils.getMargin(marginId=marginId, baseURL=baseURL, headers=headers, incremental=True)
                       
print "Done"
