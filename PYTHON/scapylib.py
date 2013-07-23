#! /usr/bin/env python

import socket
import select
import time
start = time.time() 
tic = lambda: 'at %1.1f seconds' % (time.time() - start)
import sys
from types import IntType, StringType
from scapy.all import sendp, Ether, IP, ICMP, sniff
from constants import *
import socket
#import gevent
#from gevent import monkey
#monkey.patch_all()
ETH_P_ALL = 3

def valid_req_param(reqParam):
    """ Check validity of parameters
    
    Accepts a dictionary of parameters
    
    """
    if reqParam == None:
        return None

    for key in reqParam.keys():
        # check for valid parameter keywords
        if key not in validReqParam:
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

class Scapy:
    """ A class for sending packets via Scapy

    Attributes:
        self.packets - list of packets to send

    Methods:
        def __init__ - constructor, does basic checking, e.g. whether
        the input parameter keywords match specs
    
    """

    def __init__(self, inputPkts):
        """ Initialize list of packets to send

        inputPkts - a list of networking header information dictionaries used
            to craft packets; OF parameters are reused in addition to other
            information such as interface to send out of and interface to
            listen on
        
        """
        # Not all parameters may be used by the request object
        # Other parameters are dependent on the type of request
        # and are created/assigned using get_param

        self.tcPackets = []
        for eachPkt in inputPkts:
            tcPacket = {} 
            keysPkt = eachPkt.keys()
            scapyPkt = Ether()
            sendPkt = eachPkt[SENDPKT]
            keysSendPkt = sendPkt.keys()
            if TC_ETHER in keysSendPkt:
                # handle basic L2
                etherInput = sendPkt[TC_ETHER]
                keysEther = etherInput.keys()
                if DL_SRC in keysEther:
                    scapyPkt[Ether].src = etherInput[DL_SRC]
                if DL_DST in keysEther:
                    scapyPkt[Ether].dst = etherInput[DL_DST]
                if DL_TYPE in keysEther:
                    scapyPkt[Ether].type = etherInput[DL_TYPE]
            if TC_DOT1Q in keysSendPkt:
                # handle VLAN tagging
                scapyPkt = scapyPkt/Dot1Q()
                dot1qInput = sendPkt[TC_DOT1Q]
                keysDot1q = dot1qInput.keys()
                if DL_VLAN in keysDot1q:
                    scapyPkt[Dot1Q].vlan = dot1qInput[DL_VLAN]
            if TC_IP in keysSendPkt:
                # handle IP
                scapyPkt = scapyPkt/IP()
                ipInput = sendPkt[TC_IP]
                keysIP = ipInput.keys()
                if NW_SRC in keysIP:
                    scapyPkt[IP].src = ipInput[NW_SRC]
                if NW_DST in keysIP:
                    scapyPkt[IP].dst = ipInput[NW_DST]
            tcPacket[SENDPKT] = scapyPkt 
            try:
                tcPacket[RECVPKT] = eachPkt[RECVPKT]
            except KeyError:
                print 'Expected packet information not found'
                raise
            try:
                tcPacket[COUNT] = eachPkt[COUNT]
            except KeyError:
                print 'Packet count not found'
                raise
            try:
                tcPacket[SIFACE] = eachPkt[SIFACE]
            except KeyError:
                print 'Sending interface not found'
                raise
            try:
                tcPacket[RIFACE] = eachPkt[RIFACE]
            except KeyError:
                print 'Receiving interface not found'
                raise
               
            self.tcPackets.append(tcPacket)

    def execute(self):
        """ Send packets

        Send COUNT times and check for output

        """
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, \
                socket.htons(ETH_P_ALL))
        for tcPacket in self.tcPackets:
            count = 0
            s.bind((tcPacket[RIFACE], ETH_P_ALL))
            for i in range(tcPacket[COUNT]):
                sendp(tcPacket[SENDPKT], iface = tcPacket[SIFACE])
                r,w,e = select.select([s], [], [], 1)
                if r:
                    # for now, we just assume there is no noise in the OVS
                    # hence we just check for one packet at a time
                    # TODO:  If there is noise in the OVS, then this algo
                    # will not work because noise packets must be filtered
                    # out.  Also, need to take performance into account as 
                    # this isn't done so for now.
                    packet = s.recv(65535)
                    p = Ether(packet)
                    print 'got packet:'
                    print 'packet L2 type:  {0}'.format(hex(p[Ether].type))
                    print 'packet L2 SRC:  {0} | DST:  {1}'.format(p[Ether].src, p[Ether].dst)
                    print 'packet L3 SRC:  {0} | DST:  {1}'.format(p[IP].src, p[IP].dst)
                    if self.pkt_match(p, tcPacket[RECVPKT]):
                        count += 1
                        print 'packet matches:'
                    else:
                        print 'packet does not match:'
    
            print 'packets received:  {0}'.format(count)
            if count == tcPacket[COUNT]:
                print 'PASS:  expected {0} packets, got {1} packets'.\
                        format(tcPacket[COUNT], count)
            if count < tcPacket[COUNT]:
                print 'FAIL:  expected {0} packets, got {1} packets'.\
                        format(tcPacket[COUNT], count)
        s.close()

    def send(self):
        for tcPacket in self.tcPackets:
            for i in range(tcPacket[COUNT]):
                print 'sending packet {0} now on iface {1} at time {2}'.\
                   format(i, tcPacket[SIFACE], tic())
                sendp(tcPacket[SENDPKT], iface = tcPacket[SIFACE])

    def recv(self):
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, \
                socket.htons(ETH_P_ALL))
        s.bind((IFACE, ETH_P_ALL))
        count = 0
        for tcPacket in self.tcPackets:
           print 'sniffing {0} packets now on iface {1} at time {2}'.\
                   format(tcPacket[COUNT], tcPacket[RIFACE], tic())
           packets = sniff(iface = tcPacket[RIFACE], count=tcPacket[COUNT], timeout=1)
           print format(packets)
        while 1:
            r,w,e = select.select([s], [], [], 1)
            if r:
                packet = s.recv(65535)
                p = Ether(packet)
                print 'packet received:  {0}'.format(p)
                print 'packet L2 type:  {0}'.format(hex(p[Ether].type))
                print 'packet L2 SRC:  {0}'.format(p[Ether].src)
                print 'packet L2 DST:  {0}'.format(p[Ether].dst)
                print 'packet L3 SRC:  {0}'.format(p[IP].src)
                print 'packet L3 DST:  {0}'.format(p[IP].dst)
    
        s.close()

    def gsendrecv(self):
        gevent.joinall([
            gevent.spawn(self.recv),
            gevent.spawn(self.send)
        ])

    def pkt_match(self, packet, matchPkt):
        ''' Match received packet against match fields
    
        '''
        keysMatchPkt = matchPkt.keys()
        if TC_ETHER in keysMatchPkt:
            # handle basic L2
            etherInput = matchPkt[TC_ETHER]
            keysEther = etherInput.keys()
            if DL_SRC in keysEther:
                if packet[Ether].src != etherInput[DL_SRC]:
                    return False
            if DL_DST in keysEther:
                if packet[Ether].dst != etherInput[DL_DST]:
                    return False
            if DL_TYPE in keysEther:
                if packet[Ether].type != etherInput[DL_TYPE]:
                    return False
        if TC_DOT1Q in keysMatchPkt:
            # handle VLAN tagging
            dot1qInput = matchPkt[TC_DOT1Q]
            keysDot1q = dot1qInput.keys()
            if DL_VLAN in keysDot1q:
                if packet[Dot1Q].vlan != dot1qInput[DL_VLAN]:
                    return False
        if TC_IP in keysMatchPkt:
            # handle IP
            ipInput = matchPkt[TC_IP]
            keysIP = ipInput.keys()
            if NW_SRC in keysIP:
                if packet[IP].src != ipInput[NW_SRC]:
                    return False
            if NW_DST in keysIP:
                if packet[IP].dst != ipInput[NW_DST]:
                    return False
        return True 
