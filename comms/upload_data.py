# quick workaround to import grandparent-directory
import sys
sys.path.append("..")
import config as cfg
from os import remove
import time
import requests
from comms.ping import ping

def upload_data():

    # ping server to check connection
    initial_time = time.time() #Store the time when request is sent
    ping(cfg.server_ip)
    ending_time = time.time() #Time when acknowledged the request
    elapsed_time = (ending_time - initial_time)

    if elapsed_time < cfg.ping_threshold:
        try:
            with open(cfg.data_path, 'rb') as f:
                r = requests.put(cfg.server_url+'api/guardar', data={'ejemplo_payload': f})
            print(r.status_code)
            if r.status_code == 200:
                print("upload to server successful")
                remove(cfg.data_path)
                return True # tendria que borrar el archivo si no se borra
            else:
                print("upload to server unsuccessful, status code != 200")
                return False
        except requests.exceptions.ConnectionError:
            print("upload to server unsuccessful, ConnectionError")
            #r.status_code = "Connection refused"
            return False
        except:
            print("nothing to upload to server")
            return True
    else:
        return False
