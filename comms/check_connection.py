import sys
sys.path.append('..')
import config as cfg
from time import sleep
from comms.ping import ping

def check_connection(event):
    while True:
        result = ping(cfg.server_ip)
        if result:
            print("connection established")
            event.set()
        else:
            print("no connection")
            event.clear()
        
        sleep(cfg.check_conn_period)

