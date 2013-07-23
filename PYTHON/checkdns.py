#!/bin/env /usr/bin/python

"""
check_ipconfig.py
This script checks the network configuration of converter hosts, i.e. Win7

How it works:
      - Run winexe from the linux command line to execute ipconfig
      on remote Win7 host
      - Verify the output from ipconfig and log results

Usage:
      - In hosts dictionary, enter all the hosts that need to be verified
        along with the IP addresses
      - a configuration file, 

Need dictionary of Win7 hosts
Need interface name - 'Ethernet adapter Local Area Connection' 
Need DNS server addresses
Need GW - ?
Need domain name of server - ?

"""

import subprocess
import os
import re
import time

# Regular expression patterns
reEther = re.compile('Ethernet adapater Local Area Connection')
reTun = re.compile('Tunnel adapter')
reDns = re.compile('DNS Servers')
DNS1 = '172.17.3.131'
DNS2 = '172.17.3.132'

reDNS1 = re.compile(DNS1)
reDNS2 = re.compile(DNS2)

# Default values
DEFUSER = 'administrator'
DEFPWD = 'boardvantage'
DEFDOMAIN = 'boardvantage'
WINEXE = '/usr/bin/winexe'
user = ''
host = ''
pwd = ''

ServerList = [
    {   
        'host': 'twdev1',
        'ip' : '192.168.2.211',
        'iface' : 'Ethernet adapter Local Area Connection',
        'user' : 'dev-tw',
        'pwd' : 'boardvantage',
        'domain' : 'boardvantage',
    },
    {   
        'host': 'twdev2',
        'ip' : '192.168.2.212',
        'iface' : 'Ethernet adapter Local Area Connection',
        'user' : 'dev-tw',
        'pwd' : 'boardvantage',
        'domain' : 'boardvantage',
    },
]

# Verification file setup
sumLogName = 'TW-Verification-Summary.'
ext = '.log'
DELIMIT = '####################################################'
timestamp = time.strftime('%Y%m%d-%H:%M:%S')
sumLogName = sumLogName + timestamp + ext

# Create the log file
sumLog = open(sumLogName, 'w')
 
for server in ServerList:
    keys = server.keys()
    if 'user' in keys:
        user = server['user']
    else:
        user = DEFUSER
    if 'pwd' in keys:
        pwd = server['pwd']
    else:
        pwd = DEFPWD
    if 'domain' in keys:
        domain = server['domain']
    else:
        domain = DEFDOMAIN
    host = server['host']
    login = '"{0}\{1}%{2}"'.format(domain, user, pwd)
    ip = '//{0}'.format(server['ip'])

    # Windows command
    wcmd = 'ipconfig /all'
    params = '--uninstall -U "{0}\{1}%{2}" //{3} "' + wcmd + '"' \
        .format(domain, user, pwd, server['ip'])

    cmd = WINEXE + ' ' + params
    # Host log file setup
    hostLog = 'TW-Verification.'+host+'.'
    ext = '.log'
    timestamp = time.strftime('%Y%m%d-%H:%M:%S')
    hostLog = hostLog + timestamp + ext

    p = subprocess.Popen(cmd, bufsize=1, shell=True, stdout=subprocess.PIPE)
    output, err = p.communicate()
    print 'error:  {0}\n'.format(err)
    sumLog.write(DELIMIT+'\n')
    sumLog.write('# HOST:  {0}\n'.format(host))
    sumLog.write('# IP:  {0}\n'.format(ip))

    if err == None:
        # Create the log file and write output from 'ipconfig /all'
        hostLogF = open(hostLog, 'w')
        hostLogF.write(output)
        hostLogF.close()
        
        hostLogF = open(hostLog, 'r')
        foundDns = 0
        for line in hostLogF:
            if reTun.match(line) != None:
                break
            if reDns1.search(line) != None:
                sumLog.write('Found DNS server 1:  {0}\n'.format(DNS1))
                foundDns += 1
            if reDns2.search(line) != None:
                sumLog.write('Found DNS server 2:  {0}\n'.format(DNS2))    
                foundDns += 1
            print 'line:  {0}'.format(line)
    
        if foundDns < 2:
            sumLog.write('ERROR:  found {0} DNS servers\n'.format(foundDns))
            sumLog.write('        check log file for {0}\n'.format(host))
        else:
            sumLog.write('***** PASS:  Host {0} *****\n'.format(host))
    
        hostLogF.close()
    else:
        sumLog.write('# ERROR, could not execute remote request\n')
        sumLog.write('# Error code:  {0}\n'.format(err))

sumLog.close()
