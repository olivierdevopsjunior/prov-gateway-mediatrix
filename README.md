# prov-gateway-mediatrix



This application designed for change some parameters on the Mediatrix S724 with Dgw 42.3.986 firmware.

It use Pysnmp library for the snmp requests.

It do several snmpset requests for change value on the gateway.

The differents OID mentioned in the code are essential for the proper functioning of the solution.

The objective is :

When the gateway boot, it download the configuration and firmware file at a HTTP server.
