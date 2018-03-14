# -*- coding: utf-8 -*-

print "Start";

import requests;
import argparse;
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description='Connects to CME IM API.');
parser.add_argument('--login', type=str, required=True);
parser.add_argument('--password', type=str, required=True);
args = parser.parse_args();
print 'Login: '+args.login;
print 'Password: '+args.password;


baseURL = 'https://cmecorenr.cmegroup.com/MarginServiceApi';
headers = {"Content-type": "application/xml",
		"Accept": "application/xml",
		"username": args.login,
		"password": args.password};

print 'List portfolios'
ret = requests.get(baseURL+'/portfolios', headers=headers);
#print ret.content;
root = ET.fromstring(ret.content);
for child in root:
	print child.tag, child.attrib['name'], child.attrib['id'];
#root = tree.getroot();
#print root;



#Add Interest Rate Swap
print 'Add Interest Rate Swap'
xmlBody = """<?xml version="1.1" encoding="UTF-8" standalone="yes"?>""";
xmlBody += """<ns2:transactionReq xmlns:ns2="http://cmegroup.com/schema/core/1.2" reqUserId="ak">""";
xmlBody += """<transaction portfolioId="8462179" type="TRADE" id="1">""";
xmlBody += """<payload encoding="STRING" format="CSV">""";
xmlBody += """<string>Firm ID,Account ID,Product Type ,Currency,Effective Date,Maturity Date,Notional,Direction,Fixed Rate\n""";
xmlBody += """TEST,1234,FRA,EUR,9/16/2018,12/16/2018,125000,R,0.05\n""";
xmlBody += """TEST,1234,OIS,GBP,11/21/2018,7/22/2022,1000000,P,0.05\n""";
xmlBody += """</string></payload></transaction></ns2:transactionReq>""";

print xmlBody;

ret = requests.post(baseURL+'/transactions', data=xmlBody, headers=headers)
print ret.status_code;
print ret.content;

print "Done";

#Update portfolios
'''
xmlBody = """<?xml version="1.1" encoding="UTF-8" standalone="yes"?>""";
xmlBody += """<ns2:portfolioReq xmlns:ns2="http://cmegroup.com/schema/core/1.2">""";
xmlBody += """<portfolio id="8462179" desc="Swap test portfolio" name="Swaps" rptCcy="USD">""";
xmlBody += """<entities clrMbrFirmId="Finastra" custAcctId="1"/>""";
xmlBody += """</portfolio></ns2:portfolioReq>""";

ret = requests.put(baseURL+'/portfolios/8462179', data=xmlBody, headers=headers)
print ret.status_code;
print ret.content;
#List portfolios again
ret = requests.get(baseURL+'/portfolios', headers=headers);
print ret.content;
'''

#Add portfolio
'''
xmlBody = """<?xml version="1.1" encoding="UTF-8" standalone="yes"?>""";
xmlBody += """<ns2:portfolioReq xmlns:ns2="http://cmegroup.com/schema/core/1.2">""";
xmlBody += """<portfolio desc="Swaption test portfolio" name="Swaptions" rptCcy="USD">""";
xmlBody += """<entities clrMbrFirmId="Finastra" custAcctId="2"/>""";
xmlBody += """</portfolio></ns2:portfolioReq>""";

ret = requests.post(baseURL+'/portfolios', data=xmlBody, headers=headers)
print ret.status_code;
print ret.content;
#List portfolios again
ret = requests.get(baseURL+'/portfolios', headers=headers);
print ret.content;
'''