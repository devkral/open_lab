#! /usr/bin/env python3

from http import client
import sys
import ssl
import os.path as op

#as cert is real signed
certfile = None #op.dirname(sys.argv[0])+"/labctl.openlab-augsburg.de"
tokenfile = op.dirname(sys.argv[0])+"/token"

_token=""
if op.isfile(tokenfile):
    with open(tokenfile,"r") as e:
        _token = e.read()
#service_url = 'https://labctl.openlab-augsburg.de' #("labctl.ffa",443),
server_addresses=[('labctl.openlab-augsburg.de',443),("10.11.7.2",443),("10.11.8.107",443)]


def dostuff(action, server_count=0):
    used_address = None
    if action in ["open","close"]:
        evtoken="&token={}".format(_token)
    elif action in ["state",]:
        evtoken=""
    else:
        print("Invalid action")
        sys.exit(1)

    sslcontext=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    sslcontext.verify_mode = ssl.CERT_REQUIRED
    if bool(certfile)==True:
        sslcontext.load_verify_locations(certfile) #load_cert_chain(certfile)
    else:
        sslcontext.load_default_certs()

    workingcon=False
    for elem in server_addresses[server_count:]:
        try:
            con = client.HTTPSConnection(elem[0],elem[1],context=sslcontext, timeout=10)
            con.connect()
            workingcon=True
            used_address = elem
            break
        except Exception as e:
            print(e)

    if workingcon == True:
        con.request("GET", "/sphincter/?action={}{}".format(action,evtoken))
        resp = con.getresponse()
        if resp.status == 200 or len(server_addresses) == 0:
            return str(resp.read(),"utf8"), used_address
        else:
            print("Bad result. Retry...")
            return dostuff(action, server_count=server_count+1)
    else:
        print("Connection failed")
        return None, used_address

if __name__ == "__main__":
    if len(sys.argv)==1:
        _action="state"
    elif len(sys.argv)==2:
        _action=sys.argv[1]
    else:
        print("Too many parameters")
        sys.exit(1)
    ret = dostuff(_action)
    if ret[0]:
        print("Connection: {} successful".format(ret[1]))
        print(ret[0])
