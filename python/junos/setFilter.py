import sys
import os
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConnectError

try:
    host_name = sys.argv[1]
    user_name = sys.argv[2]
    passw_name = sys.argv[3]
    ipfile_name = sys.argv[4]
except IndexError:
    print("Usage: host username password")
    sys.exit(1)


def checkAddrMask(ipMask):
    if "/" in ipMask and len(ipMask.split("/")) and ipMask.split("/")[1].isdigit():
            if int(ipMask.split("/")[1])>=0 and int(ipMask.split("/")[1])<33:
                if "." in ipMask and len(ipMask.split("."))==4:
                    ipDigit = ipMask.split("/")[0].split(".")
                    for xTmp in ipDigit:
                        if not xTmp.isdigit():
                            return False
                        if int(xTmp) < 0 or int(xTmp) > 255:
                            return False
                    return True
    return False

def main():
    # open a connection with the device and start a NETCONF session
    try:
        dev = Device(host=host_name, user=user_name, password=passw_name)
        dev.open()
        dev.timeout = 300
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        return
    with Config(dev, mode='private') as cu:  
        addrList = {}
        with open(ipfile_name) as file:
            addrList = file.read().splitlines()
        for ipAddr in addrList:
            if checkAddrMask(ipAddr):
                cu.load('set firewall filter F-EGRESS term DENY-ATTACKERS from source-address '+ ipAddr, format='set')
        if cu.diff():
            cu.commit()
        cu.commit()
    dev.close()

if __name__ == "__main__":
    main()
