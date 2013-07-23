from tornado import httpserver,ioloop
import httplib2
import json
import logging
import time
from datetime import datetime
from constants import *
from .log import logger as lg

empty_json = json.dumps({})

class Ryu_Mock():
    """ Ryu Mock (HTTP Server) object, used to receive request and send response
        to BB

    """
    def __init__(self):
        self.http_server = httpserver.HTTPServer(self.handle_request)
        self.http_server.bind(RYU_MOCK_LISTEN_PORT)
        self.http_server.start()
        self.reset_instance()
        ioloop.IOLoop.instance().start()
    
    def reset_instance(self):
        self.bb_ryu_mock = None
        self.result = []

    def send_response(self, request, status, header, response):
        """ Send response back to client (BB)
    
        """
        request.write("HTTP/1.1 {status} \r\n"\
                   "{header} \r\n"\
                   "Content-Length: {length}\r\n\r\n{response}"\
                       .format(status=status,
                               header=header,
                               length=len(response),
                               response=response)
                  )
        request.finish()

    def handle_request(self, request):
        """ Handle request sent from BB or Versionone

        """
        print request
        lg.info(request)
        if 'ryu_mock_send_test_case' in request.uri: 
            # This is request from versionone to instantiate BB_Ryu_Mock
            self.reset_instance()
            self.bb_ryu_mock = BB_Ryu_Mock(eval(request.body))
            # Response the result of instantiation
            self.send_response(request, 200, request.headers, 
                                str(self.bb_ryu_mock.result))
            return
        elif 'ryu_mock_get_result' in request.uri:
            # This is request from versionone to retrieve test result
            self.send_response(request, 200, request.headers, str(self.result))
            self.result = []
            return
        else:
            # This is request from BB
            # Forward to Ryu the request sent from BB
            ryu_req = httplib2.Http(".cache")
            ryu_url = '{0}://{1}:{2}{3}'.format(request.protocol,
                        RYU_HOST,RYU_WSAPI_PORT,request.uri)
            headers = request.headers
            headers['Host'] = '{0}:{1}'.format(headers['Host'].split(':')[0],
                                                RYU_WSAPI_PORT)
            ryu_response_headers,ryu_response_body = \
                ryu_req.request(ryu_url, request.method, headers=headers, 
                                body=request.body)
            # Forward to BB the response sent from Ryu
            self.send_response(request, ryu_response_headers['status'],
                                ryu_response_headers, ryu_response_body)
       
            if self.bb_ryu_mock:
                # check every request comming from BB and store its test result 
                self.bb_ryu_mock.handle_request(request)
                if self.bb_ryu_mock.result[0] != None:
                    self.result.append(self.bb_ryu_mock.result)
                    self.bb_ryu_mock.result = (None,'')

    def stop(self):
        """ Stop mock server.
            Put result into queue for later retrievement

        """
        self.http_server.stop()
        ioloop.IOLoop.instance().stop()

class BB_Ryu_Mock():
    """ BB Request object to work with Ryu Mock.
        Should be instantiated with these params passed:
            + operation: 'addrule/delrule/activaterule/deactivaterule' 
            + tc_pamras: dictionary of priority, active, datapath_id, 
                         openflow-matching-primitives, bofh_id,
                         openflow-actions
            + send_ctrlr: True/False

    """
    def __init__(self, tc_params):
        self.timestamp = time.mktime(datetime.now().timetuple())
        self.result = (None,'')
        self.tc_params = tc_params # For debug only
        self.tc_operation = ''
        self.tc_priority = ''
        self.tc_active = False
        self.tc_datapath_id = ''
        self.tc_openflow_primitive = []
        self.tc_bofh_id = ''
        self.tc_openflow_action = []
        self.tc_send_ctrlr = False
        
        if 'operation' in tc_params[BB_PARAMS].keys():
            self.tc_operation = tc_params[BB_PARAMS]['operation']
        else:
            self.result = (False,'Missing operation in this test case')

        if 'priority' in tc_params[BB_PARAMS].keys():
            self.tc_priority = tc_params[BB_PARAMS]['priority']
        else:
            self.result = (False,'Missing priority in this test case')

        self.tc_active = tc_params[BB_PARAMS]['active'] \
            if 'active' in tc_params[BB_PARAMS].keys() else False
        self.tc_datapath_id = tc_params[BB_PARAMS]['datapath_id'] \
            if 'datapath_id' in tc_params[BB_PARAMS].keys() else ''
        
        if 'openflow_primitive' in tc_params[BB_PARAMS].keys():
            self.tc_openflow_primitive = tc_params[BB_PARAMS]['openflow_primitive']
        else:
            self.result = (False,'Missing openflow_primitive in this test case')

        self.tc_bofh_id = tc_params[BB_PARAMS]['bofh_id'] \
            if 'bofh_id' in tc_params[BB_PARAMS].keys() else 0
        self.tc_openflow_action = tc_params[BB_PARAMS]['openflow_action'] \
            if 'openflow_action' in tc_params[BB_PARAMS].keys() else []
        self.tc_send_ctrlr = tc_params[RYU_MOCK_PARAMS]['send_ctrlr'] \
            if 'send_ctrlr' in tc_params[RYU_MOCK_PARAMS].keys() else False
    
    def check_request_uri(self, request, req_params):
        """ Check request received from BB against test case params.
            Return True if request matchs expected result within 3s,
            False if:
                + invalid operation
                    (not addrule/activaterule/deactivaterule/delrule)
                + invalid method for operation
                + not receive valid request from BB within 3s
                + receive valid request from BB while unexpected to receive

        """
        # First need to check operation makes correct request.method
        if self.tc_operation == 'addrule':
            if self.tc_active == True:
                if request.method != 'PUT':
                    msg = 'Unexpected {0} request for {1} with active={2}. '\
                          'PUT request is expected'\
                          .format(request.method, self.tc_operation,
                                  self.tc_active)
                    return (False, msg)
            else:
                if request.method == 'PUT' or request.method == 'DELETE':
                    msg = 'Unexpected {0} request for {1} with active={2}. '\
                          'No request is expected'\
                          .format(request.method, self.tc_operation,
                                  self.tc_active)
                    return (False, msg)

        elif self.tc_operation == 'activaterule':
            if request.method != 'PUT':
                msg = 'Unexpected {0} request for {1}. '\
                      'PUT request is expected'\
                       .format(request.method, self.tc_operation)
                return (False, msg)

        elif (self.tc_operation == 'delrule') or \
                (self.tc_operation == 'deactivaterule'):
            if request.method != 'DELETE':
                msg = 'Unexpected {0} request for {1}. '\
                      'DELETE request is expected'\
                      .format(request.method, self.tc_operation)
                return (False, msg)


        # This is a list of expected primitives to appear in the request URI
        # sent by BB to Ryu 
        expected_uri_params_tokens = []
        expected_uri_params_tokens.append('priority={0}'
                .format(self.tc_priority))
        for item in self.tc_openflow_primitive:
            k,v=item.split('=')
            if k in ['of_table',
                     'in_port',
                     'dl_src','dl_dst','dl_vlan','dl_vlan_pcp',
                     'nw_tos','nw_proto','nw_src','nw_dst',
                     'tp_src','tp_dst'
                    ]:
                expected_uri_params_tokens.append('{0}={1}'\
                    .format(k if k != 'of_table' else 'table',v))
            elif 'dl_type' == k:
                expected_uri_params_tokens.append('{0}={1}'\
                    .format(k,int(v,16)))
                
        
        # Check if datapath_id in URI
        uri_parts = request.uri.split('/flowtable/')
        if self.tc_datapath_id and \
           '/ws.v1/flexinet/datapath/{0}'.format(self.tc_datapath_id)\
            not in uri_parts[0]:
            msg = 'datapath_id {0} not found in URI'\
                    .format(self.tc_datapath_id)
            return (False, msg)
        
        # Check if URI has all tokens supposed to exist
        uri_params_tokens = uri_parts[1].split('&')
        for i in range(0, len(uri_params_tokens)):
            uri_params_tokens[i] = url_decoder(uri_params_tokens[i])
            if uri_params_tokens[i].startswith('nw_'):
                uri_params_tokens[i] = uri_params_tokens[i].split('/')[0]
        
        if len(expected_uri_params_tokens) != len(uri_params_tokens):
            msg = 'Mismatch URI length:\nExpected: {0}\nActual: {1}'\
                    .format(expected_uri_params_tokens, uri_params_tokens)
            return (False, msg)
        
        # Check if each expected uri param token exist in the received request
        for i in expected_uri_params_tokens:
            if i not in uri_params_tokens:
                msg = '{0} not found in URI'.format(i)
                return (False, msg)
       
        if self.tc_openflow_action and 'actions' in req_params.keys():
            return self.check_request_body(req_params) 

        return (True, 'Got correct request from BB')

    def check_request_body(self, req_params):
        expected_actions = []
        for item in self.tc_openflow_action:
            tokens = item.split('=')
            action,value =  tokens[0],None
            if len(tokens) > 1:
                value = tokens[1]
            if action == 'output':
                this_action = {
                    'type': OFP_ACTIONS[action],
                    'port': str(value),
                    'max_len': ARBITRARY_LARGE_PACKET_SIZE,
                }
            elif action == 'mod_dl_vlan':
                this_action = {
                    'type': OFP_ACTIONS[action],
                    'len': 8,
                    'vlan_vid': value,
                }
            elif action == 'strip_vlan':
                this_action = {
                    'type': OFP_ACTIONS[action],
                    'len': 8,
                }
            elif (action == 'mod_dl_src' or
                  action == 'mod_dl_dst'):
                this_action = {
                    'type': OFP_ACTIONS[action],
                    'len': 16,
                    'dl_addr': value,
                }
            elif action == 'strip_vlan':
                this_action = {
                    'type': OFP_ACTIONS[action],
                }
            elif (action == 'mod_nw_src' or
                  action == 'mod_nw_dst'):
                # Not yet implemented in BB
                # this_action = {
                # }
                continue
            elif action == 'resubmit':
                # XXX action should be of the for 'port,table'
                this_action = {
                    'type': OFPAT_VENDOR,
                    'len': 16,
                    'vendor': NX_VENDOR_ID,
                    'subtype': NXM_ACTION[action],
                    'in_port': value.split(',')[0],
                    'table': value.split(',')[1],
                }
            elif action == 'set_tunnel':
                this_action = {
                    'type': OFPAT_VENDOR,
                    'len': 16,
                    'vendor': NX_VENDOR_ID,
                    'subtype': NXM_ACTION[action],
                    'tun_id': value,
                }
            else:
                continue # This action won't include in request, so skip it
            
            expected_actions.append(this_action)
       
        req_actions = eval(req_params['actions'][0])
        if expected_actions == req_actions: # Strictly check elements 
                                            # and their order as well
            return (True, 'Got correct request from BB')
        else:
            return (False, 'ACTIONS MISMATCHED.\n'\
                           'MISMATCHED ACTIONS IN TEST CASE: {0}\n'\
                           'MISMATCHED ACTIONS IN BB REQUEST: {1}'\
                           .format(expected_actions,
                                    req_actions))

    def remove_common_tokens(self, ori_expected_tokens, ori_actual_tokens):
        expected_tokens = list(ori_expected_tokens)
        actual_tokens = list(ori_actual_tokens)
        for i in range(len(actual_tokens)-1, -1, -1):
            if actual_tokens[i] in expected_tokens:
                expected_tokens.remove(actual_tokens[i])
                actual_tokens.pop(i)
        
        return (expected_tokens,actual_tokens)

    def handle_request(self,request):
        """ Do the actual request handling. Only handle 'GET','PUT' 
            and 'DELETE' request from BB, ignore other request type
            Retrieve data from request, call check_request_uri and send_response

        """
        if request.method == 'GET':
            status = 200
            header = 'Content-Type: application/json'
            response = '[{"links": [], "seq": 0, "dpid": "", "ports":""}]'
            #self.send_response(request, status, header, response)
            return 0
        
        elif request.method == 'PUT' or request.method == 'DELETE':
            if '/flowtable/' not in request.uri:
                return 0 # Skip requests not generated by BB CLI

            req_params = url_parser(request.body)
            this_req = 'Req Method: {0}\nReq URI: {1}\nReq Body: {2}\n'\
                        .format(request.method,
                                url_decoder(request.uri),
                                req_params)
            header = 'Content-Type: application/json'
            response = empty_json
            
            if req_params is None:
                status = 400
                this_req += 'Result: Failed (Invalid non-URI parameters)'
                self.result = (False, this_req)
                #self.send_response(request, status, header, response)
                return 0

            for (name, values) in req_params.items():
                if len(values) > 1:
                    status = 400
                    this_req += 'Result: Failed (Parameter {0} has more than one value)'\
                                .format(name)
                    self.result = (False, this_req)
                    #self.send_response(request, status, header, response)
                    return 0
            
            (req_good, msg) = self.check_request_uri(request, req_params)
            if req_good and self.tc_send_ctrlr:
                status = 200
                this_req += 'Result: Passed ({0})\n'\
                            .format(msg)
                self.result = (True, this_req)
                #self.send_response(request, status, header, response)
                return 1
            
            else:
                # Still wait for correct uri until timeout
                status = 200
                this_req += 'Result: {0}\n'\
                            .format(msg)
                self.result = (False, this_req)
                #self.send_response(request, status, header, response)
                return 0

def main(argv=None):
    Ryu_Mock()

if __name__ == "__main__":
    sys.exit(main())
