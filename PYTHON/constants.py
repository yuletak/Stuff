#!/usr/bin/env python2.7


### CONSTANTS COMMON TO MORE THAN ONE PYTHON SCRIPT ###
BB_CLI_HOST = 'localhost'
BB_CLI_PORT = 2000

##### START V1 INPUT CONSTANTS #####

# Required test case Parameters
TTYPE       = 'ttype'
COMPONENT   = 'component'
VALID       = 'valid'
BUGS        = 'bugs'
BUG_TITLE   = 'bug_title'
BUG_DESC    = 'bug_desc'
METHOD      = 'method'
SCRIPT      = 'script'
SEND_CTRLR  = 'send_ctrlr'
BB_PARAMS   = 'bb_params'
RYU_MOCK_PARAMS = 'ryu_mock_params'

# Openflow matching primitives
IN_PORT         = 'in_port'
AP_SRC          = 'ap_src'
AP_DST          = 'ap_dst'
DL_SRC          = 'dl_src'
DL_DST          = 'dl_dst'
DL_VLAN         = 'dl_vlan'
DL_VLAN_PCP     = 'dl_vlan_pcp'
DL_TYPE         = 'dl_type'
NW_SRC          = 'nw_src'
NW_SRC_N_WILD   = 'nw_src_n_wild'
NW_DST          = 'nw_dst'
NW_DST_N_WILD   = 'nw_dst_n_wild'
NW_PROTO        = 'nw_proto'
NW_TOS          = 'nw_tos'
TP_SRC          = 'tp_src'
TP_DST          = 'tp_dst'
GROUP_SRC       = 'group_src'
GROUP_DST       = 'group_dst'

N_TABLES        = 'n_tables'
N_BUFFERS       = 'n_bufs'
CAPABILITES     = 'caps'
ACTIONS         = 'actions'
PORTS           = 'ports'

PORT_NO         = 'port_no'
SPEED           = 'speed'
CONFIG          = 'config'
STATE           = 'state'
CURR            = 'curr'
ADVERTISED      = 'advertised'
SUPPORTED       = 'supported'
PEER            = 'peer'
HW_ADDR         = 'hw_addr'

OF_TABLE        = 'of_table'

# Openflow actions
OUTPUT          = 'output'
MOD_DL_SRC      = 'mod_dl_src'
MOD_DL_DST      = 'mod_dl_dst'
MOD_DL_VLAN     = 'mod_dl_vlan'
STRIP_VLAN      = 'strip_vlan'
MOD_NW_SRC      = 'mod_nw_src'
MOD_NW_DST      = 'mod_nw_dst'

# Nicira actions
SET_TUNNEL      = 'set_tunnel'
RESUBMIT        = 'resubmit'

# Operation methods
CLI = 'cli'
ZMQ = 'zmq'

OPERATION   = 'operation'

# Operations
ADDRULE        = 'addrule'
DELRULE        = 'delrule'
ACTIVATERULE   = 'activaterule'
DEACTIVATERULE = 'deactivaterule'
ADDBOFH        = 'addbofh'
DELBOFH        = 'delbofh'

# Operation parameters
ACTIVE              = 'active'
BOFH_ID             = 'bofh_id'
BOFH_NAME           = 'bofh_name'
BOFH_PARAM          = 'bofh_param'
DATAPATH_ID         = 'datapath_id'
OPENFLOW_ACTION     = 'openflow_action'
OPENFLOW_PRIMITIVE  = 'openflow_primitive'
PRIORITY            = 'priority'
RULE_ID             = 'rule_id'

# Scapy input constants
TC_ETHER = 'ether'
TC_DOT1Q = 'dot1q'
TC_IP = 'ip'
TC_ICMP = 'icmp'
SIFACE = 'siface'
RIFACE = 'riface'
COUNT = 'count'
SCAPYPKT = 'scapypkt'
SENDPKT = 'sendpkt'
RECVPKT = 'recvpkt'

validRequiredInput = [
    TTYPE,      VALID,      BUGS,
    METHOD,     SCRIPT,     SEND_CTRLR,
    ]

validOperationParam = [
    ACTIVE,     BOFH_ID,    BOFH_NAME,
    BOFH_PARAM, DATAPATH_ID, 
    OPENFLOW_ACTION,
    OPENFLOW_PRIMITIVE, OPERATION,
    PRIORITY,   RULE_ID,
    VALID, CLI, METHOD,
    ]

validMethod = [CLI, ZMQ]

validOperation = [
    ADDRULE,        DELRULE,
    ACTIVATERULE,   DEACTIVATERULE,
    ADDBOFH,        DELBOFH,
    ]

validOFPrimitive = [  
    IN_PORT,    AP_SRC,     AP_DST,
    DL_SRC,     DL_DST,     DL_VLAN,
    DL_VLAN_PCP,            DL_TYPE,
    NW_SRC,     NW_SRC_N_WILD,
    NW_DST,     NW_DST_N_WILD,
    NW_PROTO,   NW_TOS,     TP_SRC,
    TP_DST,     GROUP_SRC,  GROUP_DST,
    N_TABLES,   N_BUFFERS,
    CAPABILITES,            ACTIONS, 
    PORTS,      PORT_NO,    SPEED,
    CONFIG,     STATE,      CURR,
    ADVERTISED, SUPPORTED,  PEER,
    HW_ADDR,    OF_TABLE,      
    ]

validOFAction = [
    OUTPUT,
    MOD_DL_SRC,     MOD_DL_DST,     MOD_DL_VLAN,
    MOD_NW_SRC,     MOD_NW_DST,
    SET_TUNNEL,     RESUBMIT,
    ]

validBofhParam = [
    BOFH_ID, BOFH_NAME, BOFH_PARAM
    ]
##### END V1 INPUT CONSTANTS #####


##### START OF OVS CONSTANTS #####

# Openflow related constants
ARBITRARY_LARGE_PACKET_SIZE = 1500
OFPP_CONTROLLER = 0xfffd # openflow controller port.
NX_VENDOR_ID = 0x00002320 # Nicira's Vendor ID.

# Openflow Actions
OFPAT_OUTPUT = 0x0 # Output to switch port.
OFPAT_SET_VLAN_VID = 0x1 # Set the 802.1q VLAN id.
OFPAT_SET_VLAN_PCP = 0x2 # Set the 802.1q priority.
OFPAT_STRIP_VLAN = 0x3 # Strip the 802.1q header.
OFPAT_SET_DL_SRC = 0x4 # Ethernet source address.
OFPAT_SET_DL_DST = 0x5 # Ethernet destination address.
OFPAT_SET_NW_SRC = 0x6 # IP source address.
OFPAT_SET_NW_DST = 0x7 # IP destination address.
OFPAT_SET_NW_TOS = 0x8 # IP ToS (DSCP field = 0 6 bits).
OFPAT_SET_TP_SRC = 0x9 # TCP/UDP source port.
OFPAT_SET_TP_DST = 0xA # TCP/UDP destination port.
OFPAT_ENQUEUE = 0xB # Output to queue.
OFPAT_VENDOR = 0xffff

# Nicira extension's Action
NXAST_RESUBMIT = 0x1
NXAST_RESUBMIT_TABLE = 0xE
NXAST_SET_TUNNEL = 0x2

OFP_ACTIONS = {
    'output': OFPAT_OUTPUT,
    'mod_dl_src': OFPAT_SET_DL_SRC,
    'mod_dl_dst': OFPAT_SET_DL_DST,
    'mod_dl_vlan': OFPAT_SET_VLAN_VID,
    'strip_vlan': OFPAT_STRIP_VLAN,
    'mod_nw_src': OFPAT_SET_NW_SRC,
    'mod_nw_dst': OFPAT_SET_NW_DST,
}
NXM_ACTION = {
    'set_tunnel': NXAST_SET_TUNNEL,
    'resubmit': NXAST_RESUBMIT_TABLE,
}

### CONFIG FOR BGPS
BGPS_HOST = ROUTEM_HOST = R2_HOST = '216.69.72.55'

### CONFIG FOR OVS
RYU_HOST = 'localhost'
OFP_TCP_LISTEN_PORT = 6633 # "--ofp_tcp_listen_port <PORT>" from Ryu running command
CONTROLLER = 'tcp:{0}:{1}'.format(RYU_HOST,OFP_TCP_LISTEN_PORT)

# Change to match the bridge your bridge information.
DATAPATH_INFO = {
    '0000aabbccddeef1': {
             'mgmt_ip': '216.69.85.72',
             'port' : 22,
             'username': 'root',
             'password': 'xyz123',
             'bridge': 'br0',
    },
    '0000aabbccddeef4': {
             'mgmt_ip': '216.69.85.74',
             'port' : 22,
             'username': 'root',
             'password': 'xyz123',
             'bridge': 'br0',
    },
}
