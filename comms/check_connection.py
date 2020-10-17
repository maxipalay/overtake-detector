import sys
sys.path.append('..')
import config as cfg
from time import sleep
from comms.ping import ping

def check_connection(queue):
    while True:
        result = ping(cfg.server_ip)
        if result:
            print("connection established")
        else:
            print("no connection")
        if not queue.full():
            queue.put(result);
        
        sleep(cfg.check_conn_period)

