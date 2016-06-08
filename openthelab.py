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


def dostuff(action):
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
    for elem in server_addresses:
        try:
            con=client.HTTPSConnection(elem[0],elem[1],context=sslcontext)
            workingcon=True
            
            break
        except Exception as e:
            print(e)

    if workingcon==True:
        con.request("GET", "/sphincter/?action={}{}".format(action,evtoken))
        return str(con.getresponse().read(),"utf8")
    else:
        print("Connection failed")
        return None

if __name__ == "__main__":
    if len(sys.argv)==1:
        _action="state"
    elif len(sys.argv)==2:
        _action=sys.argv[1]
    else:
        print("Too many parameters")
        sys.exit(1)
    ret = dostuff(_action)
    if ret:
        print("Connection: {} successful".format(elem))
        print(ret)
