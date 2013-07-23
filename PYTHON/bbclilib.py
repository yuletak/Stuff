#!/usr/bin/env python2.7

import telnetlib
import re
from constants import *
from bbreqlib import BBReq

SPACE = ' '
EQUAL = '='
TIMEOUT = 3
VALID_BB_RESP = 'OK:'
INVALID_BB_RESP = 'ERR:'
PROMPT = 'BB >> '
HOST_BB = '216.69.85.74'
PORT_BB = 2000
Q_BLOCK = True
Q_TIMEOUT = 3
ID = 'id'

class BBReqCli(BBReq):
    """ A class for Big Boss CLI commands
    
    All error checking for valid input parameters should be handled
    by BBReq's error checking methods and __init__.  Leaving them
    in BBReqCli's methods for now, but they are redundant.

    """
    def __init__(self, params):
        BBReq.__init__(self, params)
        self.response = []
        self.bbRequest = ''
        self.bbPass = None
        self.bbMsg = ''
        self.form_request()

    def form_addrule_oper(self):
        """ Form addrule request """

        self.bbRequest = self.operation + SPACE
        if self.priority:
            self.bbRequest = self.bbRequest + SPACE + \
                    str(self.priority) + SPACE

        if self.active:
            self.bbRequest = self.bbRequest + SPACE + \
                    ACTIVE + EQUAL + str(self.active) + SPACE

        if self.dpId:
            self.bbRequest = self.bbRequest + SPACE + \
                    DATAPATH_ID + EQUAL + str(self.dpId) + SPACE

        if self.ofPrimitives:
            for item in self.ofPrimitives:
                self.bbRequest = self.bbRequest + SPACE + item 
#            for key in self.ofPrimitives.keys():
#                self.bbRequest = self.bbRequest + SPACE + key + EQUAL \
#                    + str(self.ofPrimitives[key]) + SPACE

        if self.ofActions:
            for item in self.ofActions:
                self.bbRequest = self.bbRequest + SPACE + item 
#            for key in self.ofActions.keys():
#                if key == STRIP_VLAN:
#                    self.bbRequest = self.bbRequest + key + SPACE
#                else:
#                    self.bbRequest = self.bbRequest + SPACE + key + EQUAL \
#                    + str(self.ofActions[key]) + SPACE

        if self.bofhId:
            self.bbRequest = self.bbRequest + SPACE + \
                    BOFH_ID + EQUAL + str(self.bofhId) + SPACE

    def form_delrule_oper(self):
        """ Form delrule request """

        self.bbRequest = self.operation + SPACE + ID + EQUAL + str(self.ruleId)

    def form_activaterule_oper(self):
        """ Form activaterule request """

        self.bbRequest = self.operation + SPACE + str(self.ruleId)

    def form_deactivaterule_oper(self):
        """ Form deactivaterule request """

        self.bbRequest = self.operation + SPACE + str(self.ruleId)

    def form_addbofh_oper(self):
        """ Form addbofh request """

        self.bbRequest = self.operation + SPACE + self.reqParam[BOFH_NAME]

    def form_request(self):
        """ Form the request to send

        1) Take inputs from VersionOne (or other platform)
        2) Form CLI request
        3) Save into self.bbRequest
        """
        
        if self.operation == ADDRULE:
            self.form_addrule_oper()
        elif self.operation == DELRULE:
            self.form_delrule_oper()
        elif self.operation == ACTIVATERULE:
            self.form_activaterule_oper()
        elif self.operation == DEACTIVATERULE:
            self.form_deactivaterule_oper()
        else:
            # this is for testing invalid inputs/operations
            # should just form invalid request
            pass

        print 'Here is the request:  {0}'.format(self.bbRequest)

    def execute(self, serverIP, serverPort):
        """ Connect to server and execute this test case 
        
        """
        # Make sure bbRequest != ''
        if self.bbRequest == '':
            raise ValueError('Invalid bbRequest:  {0}'.format(self.bbRequest))

        bb = telnetlib.Telnet(serverIP, serverPort)
        bb.read_until(PROMPT)
        bb.write(self.bbRequest + '\n')
        self.response = bb.expect(['BB >> .*\nBB >>'], TIMEOUT)
        bb.write('quit\n')

    def get_response(self):
        """ Process response(s) received after sending request

        1) Process response from Big Boss
        2) Process mock OF controller response

        TODO:  handle database checking

        """
        status = re.split('\n', self.response[2])

        # Big Boss says OK! :)
        if VALID_BB_RESP in status[0]:
            #print 'Big Boss says OK!'
            # If this is an addrule operation, then get the rule id
            if self.operation == ADDRULE:
                cliResp = re.split(SPACE, status[0])
                self.ruleId = int(cliResp[4])
                #print 'Retrieved rule id:  {0}'.format(self.ruleId)
            self.bbPass = True
            self.bbMsg = self.response[2]
           
        # Big Boss says ERROR! :( 
        if INVALID_BB_RESP in status[0]:

            #print 'Big Boss says ERROR!'
            # Get the actual error message from Big Boss' return
            # TBD from consultation with KK, for now, print it
            self.bbPass = False
            self.bbMsg = self.response[2]
            #print 'self.response[2]:  '
            #print self.response[2]

        # Return Pass/Fail, msgs, and ruleId
        return (self.bbPass, self.bbMsg, self.ruleId)
