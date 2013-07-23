from mock_http_server import Ryu_Mock

# Note:
# with bofh_id: must have dl_src, dl_dst
# without bofh_id: must have datapath_id

# addrule with bofh
#tc_params = {
#    'operation' : 'addrule',
#    'priority' : 50,
#    'active' : True,
#    'openflow_primitive': {
#        'in_port' : 9999,
#        'dl_type' : 0x800,
#        'nw_proto' : 1,
#        'dl_src' : '11:11:11:11:11:11',
#        'dl_dst' : '22:22:22:22:22:22'
#    },
#    'bofh_id' : 1,
#    'openflow_action': {
#        'output' : 888,
#    },
#    'send_ctrlr' : True,
#}
#addrule 50 in_port=9999 dl_type=0x800 nw_proto=1 dl_src=11:11:11:11:11:11 dl_dst=22:22:22:22:22:22 mod_dl_src=10:10:10:10:10:10 mod_dl_dst=20:20:20:20:20:20 output=888 active=True bofh_id=1

# addrule without bofh
#tc_params = {
#    'operation' : 'addrule',
#    'priority' : 50,
#    'active' : True,
#    'datapath_id' : '0000aabbccddeef1',
#    'openflow_primitive': {
#        'in_port' : 9999,
#        'dl_type' : 0x800,
#        'nw_proto' : 1,
#    },
#    'bofh_id' : 0,
#    'openflow_action': {
#        'output' : 888,
#    },
#    'send_ctrlr' : True,
#}
#addrule 50 datapath_id=0000aabbccddeef1 in_port=9999 dl_type=0x800 nw_proto=1 output=888 active=True

# addrule without bofh with all params
tc_params = {
    'operation' : 'addrule', 
    'priority' : 100,
    'active' : True,
    'datapath_id' : '0000aabbccddeef1',
    'openflow_primitive': {
        'of_table' : 2,
        'in_port' : 9999,
        'dl_vlan' : 3,
        'dl_vlan_pcp' : 4,
        'dl_type' : 0x800,
        'nw_tos' : 5,
        'nw_proto' : 1,
        'nw_src' : '1.1.1.1',
        'nw_dst' : '2.2.2.2',
        'tp_src' : '6',
        'tp_dst' : '7',
    },
    'bofh_id' : 0,
    'openflow_action': {
        'output' : 888,
        'mod_dl_src' : '10:10:10:10:10:10',
        'mod_dl_dst' : '20:20:20:20:20:20',
        'mod_dl_vlan' : '8',
        'strip_vlan' : None,
#        'mod_nw_src' : '3.3.3.3', # Not implemented yet in BB
#        'mod_nw_dst' : '4.4.4.4', # Not implemented yet in BB
        'set_tunnel' : '9',
        'resubmit' : '0,1'
    },
    'send_ctrlr' : True,
}
#addrule 100 datapath_id=0000aabbccddeef1 active=True of_table=2 in_port=9999 dl_vlan=3 dl_vlan_pcp=4 dl_type=0x800 nw_tos=5 nw_proto=1 nw_src=1.1.1.1 nw_dst=2.2.2.2 tp_src=6 tp_dst=7 output=888 mod_dl_vlan=8 strip_vlan set_tunnel=9 resubmit=0,1 mod_dl_src=10:10:10:10:10:10 mod_dl_dst=20:20:20:20:20:20 # mod_nw_src=3.3.3.3 mod_nw_dst=4.4.4.4  

import threading,Queue
from Queue import Empty


q = Queue.Queue()
http_server = Ryu_Mock(q,tc_params)
t = threading.Thread(target=http_server.start, args=())
t.start()
##http_server.stop() # Can stop server anytime
print 'Send BB request here'

(result, msg) = (None, '')
try:
    # Should block (wait) until timeout to get value put in queue earlier
    result,msg = q.get(block=True,timeout=3)
except Empty:
    result,msg = http_server.stop()
    if tc_params['send_ctrlr']:
        result = False
        msg += "\nFail:  Did not receive matching request from BB within time frame"
    else:
        result = True
        msg += "\nPass: Did not receive matching request from BB, which is expected"

print '\n\nReturned values:'
print (result, msg)


# =======================================

action = 'addrule'
tc_params = {'priority' : 50,
          'datapath_id' : '0000aabbccddeef1',
          'in_port' : 9999,
          'dl_type' : 0x800,
          'nw_proto' : 1,
          'active' : False,
          'output' : 888 
        }
send_ctrlr = tc_params['active']

# =======================================

action = 'activaterule'
tc_params = {'priority' : 50,
          'datapath_id' : '0000aabbccddeef1',
          'in_port' : 9999,
          'dl_type' : 0x800,
          'nw_proto' : 1,
          'output' : 888 
        }
send_ctrlr = True

# =======================================

action = 'deactivaterule'
tc_params = {'priority' : 50,
          'datapath_id' : '0000aabbccddeef1',
          'in_port' : 9999,
          'dl_type' : 0x800,
          'nw_proto' : 1,
          'output' : 888 
        }
send_ctrlr = True

# =======================================

action = 'delrule'
tc_params = {'priority' : 50,
          'datapath_id' : '0000aabbccddeef1',
          'in_port' : 9999,
          'dl_type' : 0x800,
          'nw_proto' : 1,
          'output' : 888 
        }
send_ctrlr = True

# =======================================
#addrule 50 datapath_id=0000aabbccddeef1 in_port=9999 dl_type=0x800 nw_proto=1 active=True output=888

#action = 'addrule'
#tc_params = {'priority' : 100,
#             'active' : True,
#             'datapath_id' : '0000aabbccddeef1',
#             'of_table' : 2,
#             'in_port' : 9999,
#             'dl_vlan' : 3,
#             'dl_vlan_pcp' : 4,
#             'dl_type' : 0x800,
#             'nw_tos' : 5,
#             'nw_proto' : 1,
#             'nw_src' : '1.1.1.1',
#             'nw_dst' : '2.2.2.2',
#             'tp_src' : '6',
#             'tp_dst' : '7',
#             'output' : 888,
#             'mod_dl_vlan' : '8',
#             'strip_vlan' : None,
#             'mod_nw_src' : '3.3.3.3',
#             'mod_nw_dst' : '4.4.4.4',
#             'set_tunnel' : '9',
#             'resubmit' : '(0,1)'
#            }
#addrule 100 datapath_id=0000aabbccddeef1 active=True of_table=2 in_port=9999 dl_vlan=3 dl_vlan_pcp=4 dl_type=0x800 nw_tos=5 nw_proto=1 nw_src=1.1.1.1 nw_dst=2.2.2.2 tp_src=6 tp_dst=7 output=888 mod_dl_vlan=8 strip_vlan mod_nw_src=3.3.3.3 mod_nw_dst=4.4.4.4 set_tunnel=9 resubmit=0,1
