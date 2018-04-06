# -*- coding: utf-8 -*-
import requests
import xml.etree.ElementTree as ET

def addTrades(baseURL, headers):
	""" Adds 2 sample trades to prtfolio 1234 """
	print '\n*** Add Interest Rate Swap to portfolio ***'
	
	xmlBody = """<?xml version="1.1" encoding="UTF-8" standalone="yes"?>""";
	xmlBody += """<ns2:transactionReq xmlns:ns2="http://cmegroup.com/schema/core/1.2" reqUserId="ak">""";
	xmlBody += """<transaction portfolioId="8462179" type="TRADE" id="1">""";
	xmlBody += """<payload encoding="STRING" format="CSV">""";
	xmlBody += """<string>Firm ID,Account ID,Product Type ,Currency,Effective Date,Maturity Date,Notional,Direction,Fixed Rate\n""";
	xmlBody += """TEST,1234,FRA,EUR,9/16/2018,12/16/2018,125000,R,0.05\n""";
	xmlBody += """TEST,1234,OIS,GBP,11/21/2018,7/22/2022,1000000,P,0.05\n""";
	xmlBody += """</string></payload></transaction></ns2:transactionReq>""";

	ret = requests.post(baseURL+'/transactions', data=xmlBody, headers=headers)
	#print ret.content;

def requestMarginCalculation(portfolioId, baseURL, headers):
	""" Requests margin calc for portfolio and returns margin id """
	print '\n*** Request Calculation of Margin for Portfolio '+portfolioId+' ***';

	xmlBody = """<?xml version="1.1" encoding="UTF-8"?>""";
	xmlBody += """<core:marginReq xmlns:core="http://cmegroup.com/schema/core/1.2">""";
	xmlBody += "<margin portfolioId=\"" + portfolioId + "\">";
	xmlBody += """<amounts ccy="USD" conc="0.0" init="0.0" maint="0.0" nonOptVal="0.0" optVal="0.0"/>""";
	xmlBody += """</margin></core:marginReq>""";

	#if security error arises then set verify=False. Don't kno wwhy but may fix temporary issue
	ret = requests.post(baseURL+'/margins', data=xmlBody, headers=headers)
#	print ret.content;
	root = ET.fromstring(ret.content);
	print "Status: ", root.attrib['status'];
	print "Margin Id: ", root[0].attrib['id']

	return root[0].attrib['id'];

def requestIncrementalMarginCalculation(portfolioId, baseURL, headers):
	""" Adds one trade to portfolio and requests incremental margin """
	print '\n*** Request Incremental Margin ***'

	xmlBody = """<?xml version="1.0" encoding="UTF-8"?>"""
	xmlBody += """<core:marginReq xmlns:core="http://cmegroup.com/schema/core/1.2">"""
	xmlBody += """<margin portfolioId=\"""" + portfolioId + "\">"
	xmlBody += """<transactions><transaction type="TRADE" id="0" status="INSERTED">"""
	xmlBody += """<payload encoding="STRING" format="CSV">"""
	xmlBody += """<string>Firm ID,Account ID,Product Type ,Currency,Effective Date,Maturity Date,Notional,Direction,Fixed Rate\n"""
	xmlBody += """TEST,1234,FRA,EUR,9/16/2018,12/16/2018,125000,R,0.05\n"""
	xmlBody += """</string></payload></transaction></transactions>"""
	xmlBody += """<amounts ccy="USD" conc="0.0" init="0.0" maint="0.0" nonOptVal="0.0" optVal="0.0"/></margin></core:marginReq>"""

	ret = requests.post(baseURL+'/margins', data=xmlBody, headers=headers)
	print ret.content
	root = ET.fromstring(ret.content);
	print "Status: ", root.attrib['status'];
	print "Margin Id: ", root[0].attrib['id']

	return root[0].attrib['id'];

def getMargin(marginId, baseURL, headers, incremental=False):
	""" Gets margin and returns [im, vm] or [incIM, incVM] if incremental mode
	Assumes POST /margins was called prior 
	incremental - True/False """
	print '\n*** Get Margin for Margin Id ', marginId, '***'

	import time
	delay = 2
	print 'Waiting ', delay, 'seconds'
	time.sleep(delay)
	ret = requests.get(baseURL+'/margins/'+marginId, headers=headers)
	print ret.content
	root = ET.fromstring(ret.content)
	print "Status: ", root.attrib['status'];
	print "Margin Id: ", root[0].attrib['id']
	print "Initial: ", root[0][0].attrib['init']
	print "Maintenance: ", root[0][0].attrib['maint']
	if incremental:
		print "Incremental Initial: ", root[0][0][0].attrib['initDiffAmt']
		print "Incremental Maintenance: ", root[0][0][0].attrib['maintDiffAmt']
		return root[0][0][0].attrib['initDiffAmt'], root[0][0][0].attrib['maintDiffAmt']
	return [root[0][0].attrib['init'], root[0][0].attrib['maint']]

def enableHTTPLogging():
	import logging
	import httplib as http_client
	print '\n*** HTTP Logging enabled ***'
	http_client.HTTPConnection.debuglevel = 1
	logging.basicConfig()
	logging.getLogger().setLevel(logging.DEBUG)
	requests_log = logging.getLogger("requests.packages.urllib3")
	requests_log.setLevel(logging.DEBUG)
	requests_log.propagate = True

def listPortfolios(baseURL, headers):
	""" Lists all portfolios on CME """
	print '\n*** List Portfolios ***'

	ret = requests.get(baseURL+'/portfolios', headers=headers);
	#print ret.content
	root = ET.fromstring(ret.content);
	for child in root:
		print child.tag, child.attrib['name'], child.attrib['id'];


'''
def incremtal

<?xml version="1.0" encoding="UTF-8"?>
<core:marginReq xmlns:core="http://cmegroup.com/schema/core/1.2" reqUserId="YourUserId">
<margin portfolioId="123456">
<transactions>
<transaction type="TRADE" id="0" status="INSERTED">
<payload encoding="STRING" format="CSV">
<string>
Firm ID,Position Account ID,ClearedTradeId,Currency,Effective Date,Maturity Date,Notional,Direction,Fixed Rate,FloatingIndex,FloatingIndexTenor,FixedPayFrequency
Test,1234,3M PLN,USD,09/06/2011,09/06/2021,"10,000,000",P,0.03123,USD-LIBOR-BBA,6M,6M
Test,1234,1M PLN,USD,09/06/2011,09/06/2021,"10,000,000",P,0.03123,USD-LIBOR-BBA,6M,6M
Test,1234,6M PLN,USD,09/06/2011,09/06/2021,"10,000,000",P,0.03123,USD-LIBOR-BBA,6M,6M
</string>
</payload>
</transaction>
</transactions>
<amounts ccy="AUD" conc="0.0" init="0.0" maint="0.0" nonOptVal="0.0" optVal="0.0"/></margin></core:marginReq>
'''

