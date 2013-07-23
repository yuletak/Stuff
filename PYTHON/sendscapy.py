#! /usr/bin/env python

import sys
from scapy.all import send,sendp,sr1,Ether,IP,ICMP,Dot1Q
from constants import *
from scapylib import Scapy

#pkt = Ether(src='aa:bb:cc:dd:ee:fe')/IP(proto=1)
#pkt.show()

#pkt1 = IP(src='192.168.0.1', proto=1)
#pkt1 = Dot1Q()/pkt1
#pkt1 = Ether()/pkt1
#pkt1.show()

count = 0
for i in range(0):
    sendp(pkt1, iface='veth1')


#p=sr1(IP(dst=sys.argv[1])/ICMP())
#if p:
#    p.show()

packets = [
        { COUNT:5, SIFACE:'veth1', RIFACE:'veth3',
            SENDPKT:{
                TC_ETHER:{
                    DL_SRC:'aa:bb:cc:dd:ee:f1',
                    DL_DST:'aa:bb:cc:dd:ee:f2',
                    DL_TYPE:0x800,
                    },
                TC_IP:{
                    NW_SRC:'192.168.0.1',
                    NW_DST:'192.168.0.2',
                    },
                },
            RECVPKT:{
                TC_ETHER:{
                    DL_SRC:'10:10:10:10:10:10',
                    DL_DST:'20:20:20:20:20:20',
                    DL_TYPE:0x800,
                    },
                TC_IP:{
                    NW_SRC:'192.168.0.1',
                    NW_DST:'192.168.0.2',
                    },
                },
            },
        { COUNT:0, SIFACE:'veth3', RIFACE:'veth1',
            SENDPKT:{
                TC_ETHER:{
                    DL_SRC:'aa:bb:cc:dd:ee:f3',
                    DL_DST:'aa:bb:cc:dd:ee:f4',
                    DL_TYPE:0x800,
                    },
                TC_IP:{
                    NW_SRC:'192.168.0.3',
                    NW_DST:'192.168.0.4',
                    },
                },
            RECVPKT:{
                TC_ETHER:{
                    DL_SRC:'aa:bb:cc:dd:ee:f3',
                    DL_DST:'aa:bb:cc:dd:ee:f4',
                    DL_TYPE:0x800,
                    },
                TC_IP:{
                    NW_SRC:'192.168.0.3',
                    NW_DST:'192.168.0.4',
                    },
                }
            }]
    
scapyPkts = Scapy(packets)
scapyPkts.execute()
