#!/usr/bin/env python2.7

from types import IntType, StringType
from constants import *

def valid_req_method(reqMeth):
    """ Check validity of request method """
    if reqMeth not in validReqMethod:
        raise ValueError('"{0}" is not a valid request method!'
            .format(reqMeth))

def valid_req_operation(reqOp):
    """ Check validity of request operation type """

    if reqOp not in validOperation:
         raise ValueError('"{0}" is not a valid operation type!'
            .format(reqOp))

def valid_req_param(operParam):
    """ Check validity of parameters
    
    Accepts a dictionary of parameters
    
    """
    if operParam == None:
        return None

    for key in operParam.keys():
        # check for valid parameter keywords
        if key not in validOperationParam:
            raise ValueError('"{0}" is not a valid request parameter!'
                .format(key))

def valid_of_match(OFMatch):
    """ Check validity of OF matches
    
    Accepts a dictionary of OF primitives
    
    """
    if OFMatch == None:
        return None

    for key in OFMatch.keys():
        if key not in validOFPrimitive:
            raise ValueError('"{0}" is not a valid Openflow primitive!'
                .format(key))

def valid_of_action(OFAction):
    """ Check validity of OF actions
    
    Accepts a dictionary of OF actions
    
    """
    if OFAction == None:
        return None

    for key in OFAction.keys():
        if key not in validOFAction:
            raise ValueError('"{0}" is not a valid Openflow action!'
                .format(key))

class BBReq:
    """ A general class for Big Boss request objects

    Attributes:
        self.valid
        self.method
        self.operation
        self.priority
        self.ofPrimitives
        self.ofActions
        self.active
        self.dpId
        self.bofhId
        self.ruleId
        self.bofhName
        self.bofhParam

    Methods:
        def __init__ - constructor, does basic checking, e.g. whether
        the input parameter keywords match specs
    
        def execute - form the request and send it off to the Big Boss, will
        vary depending on METHOD type (see classes derived from BBReq)
    
        def validate - for validating data, i.e. NW_SRC/NW_DST is an IP address,
        DL_SRC/DL_DST is a valid MAC address; this method is called by code
        utilizing this class

    """

    def __init__(self, params):

        """ Initialize BBReq object

        Input:  dictionary of input parameters from VersionOne

        """
        # Not all parameters may be used by the request object
        # Other parameters are dependent on the type of request
        # and are created/assigned using get_param
        # V1 input keywords MUST be correct, so check for validity
        self.operParams = params
        paramKeys = params.keys()
        for key in paramKeys:
            if key not in validOperationParam:
                raise ValueError('Input parameter keyword "{0}" is not valid.'
                        .format(key))

        # Required parameters for executing the test case
        try:
            self.valid = params[VALID]
            self.operation = params[OPERATION]
        except KeyError:
            print 'Required parameter not found.'
            raise

        # Get parameters for the operation, e.g. BB CLI command
        # Validity of the parameters is NOT checked here
        # If a non-supported operation is requested, then the test
        # should fail at BB, i.e. the rest of the operation is ignored
        # Invalid values can be inserted in the input parameters after
        # the operation type

        if self.operation == ADDRULE:
            if PRIORITY in paramKeys:
                self.priority = params[PRIORITY]
            else:
                self.priority = None
            if OPENFLOW_PRIMITIVE in paramKeys:
                self.ofPrimitives = params[OPENFLOW_PRIMITIVE]
            else:
                self.ofPrimitives = None
            if OPENFLOW_ACTION in paramKeys:
                self.ofActions = params[OPENFLOW_ACTION]
            else:
                self.ofActions = None
            if ACTIVE in paramKeys:
                self.active = params[ACTIVE]
            else:
                self.active = None
            if DATAPATH_ID in paramKeys:
                self.dpId = params[DATAPATH_ID]
            else:
                self.dpId = None
            if BOFH_ID in paramKeys:
                self.bofhId = params[BOFH_ID]
            else:
                self.bofhId = None
        if self.operation in [ADDRULE, ACTIVATERULE, DEACTIVATERULE, DELRULE]:
            if RULE_ID in paramKeys:
                self.ruleId = params[RULE_ID]
            else:
                self.ruleId = None
        if self.operation == ADDBOFH:
            if BOFH_NAME in paramKeys:
                self.bofhName = params[BOFH_NAME]
            else:
                self.bofhName = None
            if BOFH_PARAM in paramKeys:
                self.bofhParam = params[BOFH_PARAM]
            else:
                self.bofhParam = None

        # If this request tests valid data, then check data
        #
        # TODO:  CHECK SEMANTICS, E.G. WHEN DELETING RULE, INCLUDE RULE_ID ONLY

    def execute(self):
        """ Execute the test case """
        pass   

    def validate(self):
        """ Validate input parameters """
        valid_req_operation(self.operation)
        valid_oper_param(self.operParam)
        valid_of_match(self.ofPrimitives)
        valid_of_action(self.ofActions)


