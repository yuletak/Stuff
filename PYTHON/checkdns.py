#!/bin/env /usr/bin/python

"""
check_ipconfig.py
This script checks the network configuration of converter hosts, i.e. Win7

How it works:
      - Run winexe from the linux command line to execute commands
      on remote Win7 host
      - Verify the output and log results

Usage:
    - ** to be done **

Need list of Win7 servers 
Need dictionary of each Win7 info
Need interface name, e.g. 'Local Area Connection' 
Need DNS server addresses
Need GW - ?
Need domain name of server - ?

"""

import subprocess
import os
import re
import time

# Regular expression patterns
reEther = re.compile('Ethernet adapter Local Area Connection')
reTun = re.compile('Tunnel adapter')
reDns = re.compile('DNS Servers')
DNS1 = '172.17.3.131'
DNS2 = '172.17.3.132'
reComment = re.compile('^#.*$')
# empty line
reWhitespace = re.compile('^\s*$')
reDns1 = re.compile(DNS1)
reDns2 = re.compile(DNS2)
reLocalhost = re.compile('127\.0\.0\.1[ \t]+localhost')
reMail = re.compile('192\.168\.7\.159[ \t]+' +\
    'mail.boardvantage.com[ \t]+mail.boardvantage.net')
reIface = re.compile('"Local Area Connection[ ]?\d*"')

# Default values
DEFUSER = 'administrator'
DEFPWD = 'boardvantage'
DEFDOMAIN = 'boardvantage'
user = ''
host = ''
pwd = ''

def gen_server_list(group, idHost=1, ipNet='192.168.0', ipHost=1, noServers=0, \
            attr='all', user='Administrator', pwd='xyz123', domain='WORKGROUP'):
    """ Generate list of servers 
        
        Generate list of servers and return to caller
        group is the group name, e.g. 'TW'
        ipNet is the network portion of address, assuming /24
        ipHost is the starting address of the hosts
        noServers is total range of servers, e.g. 10 servers from tw1~tw10
        attr is defined as even, odd, or all servers based on host name

    """
    list = []
    i = 0
    if attr == 'odd':
        modulo = 1
    elif attr == 'even':
        modulo = 0 
    while i < noServers:
        server = {}
        if ((int(idHost+i)%2) == modulo) or (attr=='all'):
            server['host'] = group+str(idHost+i)
            server['ip'] = ipNet+'.'+str(ipHost+i)
            server['user'] = user
            server['pwd'] = pwd
            server['domain'] = domain
            list.append(server)
        i += 1
    return list 

servers = gen_server_list('tw', 1, '192.168.11', 221, 10, 'even')
#for i in range(len(servers)):
#    print 'servers[{0}]:  {1}\n'.format(i, servers[i])

def exec_winexe(domain, user, pwd, ip, cmd):
    """ Execute the winexe command and get output/error
        
        QUOTATION MARKS for cmd:
            To remain consistent, the first set of quotes for winexe parameters
            should be of the single variety and the inner should be of the 
            double variety.  There may be other to-be-discovered cases due
            to weird Windows syntax.

            Examples:
                'cmd /C more c:\Windows\System32\drivers\etc\hosts'
                'netsh interface ipv4 show config "Local Area Connection"'

    """
    WINEXE = '/usr/bin/winexe '
    cred = '-U \'{0}\{1}%{2}\' //{3} '.format(domain, user, pwd, ip)
    paramWinexe = '--interactive=0 --uninstall ' + cred 
    params = WINEXE + paramWinexe + cmd
    p = subprocess.Popen(params, shell=True, stdout=subprocess.PIPE)
    oput, err = p.communicate()
    return oput, err

# Verification file setup
sumLogName = 'TW-Verification-Summary.'
ext = '.log'
DELIMIT = '####################################################'
timestamp = time.strftime('%Y%m%d-%H:%M:%S')
sumLogName = sumLogName + timestamp + ext

# Create the log file
sumLog = open(sumLogName, 'w')
 
for server in servers:
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
    ip = '{0}'.format(server['ip'])
    iface = ''

    # Windows command
    cmdHosts = '\'cmd /C more c:\Windows\System32\drivers\etc\hosts\''
    oputHosts, errHosts = exec_winexe(domain, user, pwd, ip, cmdHosts)

    cmdIface = '\'netsh interface ipv4 show config\''
    oputIface, errIface = exec_winexe(domain, user, pwd, ip, cmdIface)
    match = reIface.search(oputIface)
    iface = match.group(0)
#    print 'iface:  {0}\n'.format(iface)

    cmdNetsh = '\'netsh interface ipv4 show config ' + iface + '\''

    oputNetsh, errNetsh = exec_winexe(domain, user, pwd, ip, cmdNetsh)
    
    # Host log file setup
    hostLogName = 'TW-Verification.'+host+'.'
    timestamp = time.strftime('%Y%m%d-%H:%M:%S')
    hostLogName = hostLogName + timestamp + ext
    hostLog = open(hostLogName, 'w')
    hostLog.write(oputHosts)
    hostLog.close()
    
    sumLog.write(DELIMIT+'\n')
    sumLog.write('# HOST:  {0}\n'.format(host))
    sumLog.write('# IP:  {0}\n'.format(ip))

    # check hosts file output first
    if errHosts != None:
        sumLog.write('Error code - hosts subprocess.Popen:  {0}'.format(errHosts))

    hostLog = open(hostLogName, 'r+')
    hostsCheck = 0
    if errHosts == None:
        result = ''
        for line in hostLog:
            """ Match for one of three things:
            1) localhost setting
            2) mail setting
            3) empty line
            """
            # no '\n' at the end of file writes because 'line' includes it
            if reLocalhost.match(line) != None:
                sumLog.write('Found hosts file localhost setting:  {0}'\
                    .format(line))
                hostsCheck += 1 
            elif reMail.match(line) != None:
                sumLog.write('Found hosts file mail setting:  {0}'\
                    .format(line))
                hostsCheck += 1 
            elif ((reWhitespace.match(line) == None) and
                    (reComment.match(line) == None)):
                sumLog.write('Found non-expected line in hosts file: {0}'\
                    .format(line))
                
                hostsCheck = 0 
                break
        if hostsCheck == 2:
            sumLog.write('***** PASS:  hosts file *****\n')
            
        else:
            sumLog.write('***** FAIL:  Error in hosts file *****\n')
    else:
        sumLog.write('ERROR in winexe hosts: {0}\n'.format(errHosts))
            
    dnsCheck = 0
    if errNetsh == None:
        hostLog.write(oputNetsh)
        if reDns1.search(oputNetsh) != None:
           sumLog.write('Found DNS server {0}\n'.format(DNS1))
           dnsCheck += 1
        else:
           sumLog.write('Error: Did not find DNS server {0}\n'.format(DNS1))
        if reDns2.search(oputNetsh) != None:
           sumLog.write('Found DNS server {0}\n'.format(DNS2))    
           dnsCheck += 1
        else:
           sumLog.write('Error: Did not find DNS server {0}\n'.format(DNS2))
        if dnsCheck == 2:
            sumLog.write('***** PASS:  DNS setting *****\n')
        else:
            sumLog.write('***** FAIL:  DNS setting *****\n')
    else:
        sumLog.write('ERROR winexe netsh:  {0}\n'.format(errNetsh))

    hostLog.close()

sumLog.close()
