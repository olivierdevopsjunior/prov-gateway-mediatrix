#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2018-09-13

@author: Olivier
'''
from pysnmp.hlapi import CommunityData, ObjectType, ObjectIdentity, UdpTransportTarget
from pysnmp.hlapi import ContextData, setCmd
from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.hlapi import OctetString, Integer32
import socket
from pysnmp.entity import engine

'''corresponding integer/value for "protocol" paramter ::
    INTEGER { http(100) , https(200) , tftp(300) , ftp(400) , file(500) }
'''
def define_request(source, ip, community, snmp_version, fileconfname, pathfile, protocol, srvprovision, enableconfstart, urlfirmware, enablereboot):
    if snmp_version == '2c':
        communityData = CommunityData(community, mpModel=1)
    if snmp_version == '1':
        communityData = CommunityData(community, mpModel=0)
    if source:
        assd = AsynsockDispatcher()
        sock_transport = udp.UdpSocketTransport()
        sock_transport.socket.setsockopt(socket.SOL_SOCKET, 25, source + '\0')
        snmp_engine = engine.SnmpEngine()
        assd.registerTransport(udp.domainName, sock_transport)
        snmp_engine.registerTransportDispatcher(assd)
    else:
        snmp_engine = engine.SnmpEngine()
    varBind = []
    result = []
    for errorIndication, errorStatus, errorIndex, varBinds in setCmd(
                        snmp_engine,
                        communityData,
                        UdpTransportTarget((ip, 161)),
                        ContextData(),
                        ObjectType(ObjectIdentity('1.3.6.1.4.1.4935.1000.100.200.100.800.1.100.100.0'),  OctetString(fileconfname)),
                        ObjectType(ObjectIdentity('.1.3.6.1.4.1.4935.1000.100.200.100.800.1.100.300.0'),  OctetString(pathfile)),
                        ObjectType(ObjectIdentity('.1.3.6.1.4.1.4935.1000.100.200.100.800.1.100.400.100.0'),  Integer32(protocol)),
                        ObjectType(ObjectIdentity('.1.3.6.1.4.1.4935.1000.100.200.100.800.1.100.400.400.0'),  OctetString(srvprovision)),
                        ObjectType(ObjectIdentity('.1.3.6.1.4.1.4935.1000.100.200.100.800.1.100.500.100.0'),  Integer32(enableconfstart)),
                        ObjectType(ObjectIdentity('.1.3.6.1.4.1.4935.1000.100.200.100.1300.1.450.0'),  OctetString(urlfirmware)),
                        ObjectType(ObjectIdentity('.1.3.6.1.4.1.4935.1000.100.200.100.1300.1.500.0'),  Integer32(enablereboot))
                        ):
        varBind.append(varBinds)
        for i in varBinds:
            i = str(i)
            i = i.split('=')[1]
            result.append(i)
#             result.append(str(i))
#             varBind = varBind.split('=')[1]
#             result.append(varBind)
    return result


if __name__ == '__main__':
    print(define_request(source='IBCORP', ip='192.168.0.155', community='public', snmp_version='2c',fileconfname='testcfg', pathfile='testpath', protocol=100, srvprovision="192.168.0.140:80", enableconfstart=1, urlfirmware="http://192.168.0.144/dgw.bin", enablereboot=1 ))