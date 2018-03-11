# -*- coding: utf-8 -*-

print "Start";

import requests;
import argparse;

parser = argparse.ArgumentParser(description='Connects to CME IM API.');
parser.add_argument('--login', type=str, required=True);
parser.add_argument('--password', type=str, required=True);
args = parser.parse_args();
print 'Login: '+args.login;
print 'Password: '+args.password;


url = 'https://cmecorenr.cmegroup.com/MarginServiceApi'
head = {"Content-type": "application/json",
		"Accept": "application/json",
		"username": args.login,
		"password": args.password};

#Basic HTTP authentication
ret = requests.get(url+'/transactions', headers=head);
print ret.status_code;

print "Done";
