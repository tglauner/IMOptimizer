# -*- coding: utf-8 -*-
import requests
import xml.etree.ElementTree as ET

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