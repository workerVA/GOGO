import sys
import os
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import LockError
from jnpr.junos.exception import UnlockError
from jnpr.junos.exception import ConfigLoadError
from jnpr.junos.exception import CommitError
try:
    host_name = sys.argv[1]
    user_name = sys.argv[2]
    passw_name = sys.argv[3]
    conf_name = sys.argv[4]
except IndexError:
    print("Usage: filename hourdelta minutdelta separate")
    sys.exit(1)


conf_file = conf_name

def main():
    # open a connection with the device and start a NETCONF session
    try:
        dev = Device(host=host_name, user=user_name, password=passw_name)
        dev.open()
        dev.timeout = 300
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        return

    dev.bind(cu=Config)

    # Lock the configuration, load configuration changes, and commit
    print ("Locking the configuration")
    try:
        dev.cu.lock()
    except LockError as err:
        print ("Unable to lock configuration: {0}".format(err))
        dev.close()
        return

    print ("Loading configuration changes")
    try:
        dev.cu.load(path=conf_file, merge=True,overwrite=True)
    except (ConfigLoadError, Exception) as err:
        print ("Unable to load configuration changes: {0}".format(err))
        print ("Unlocking the configuration")
        try:
                dev.cu.unlock()
        except UnlockError:
            print ("Unable to unlock configuration: {0}".format(err))
        dev.close()
        return

    print ("Committing the configuration")
    try:
        dev.cu.commit(comment='Loaded by example.',timeout=360)
    except CommitError as err:
        print ("Unable to commit configuration: {0}".format(err))
        print ("Unlocking the configuration")
        try:
           dev.cu.unlock()
        except UnlockError as err:
            print ("Unable to unlock configuration: {0}".format(err))
        dev.close()
        return

    print ("Unlocking the configuration")
    try:
        dev.cu.unlock()
    except UnlockError as err:
        print ("Unable to unlock configuration: {0}".format(err))

    # End the NETCONF session and close the connection
    dev.close()

if __name__ == "__main__":
    main()
