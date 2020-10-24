import base64
import sys
sys.path.append('..')
import config as cfg
import json
import sys
sys.path.append('..')
import config as cfg
from cv2 import imencode
import os

def save_infraction(infr):
    file_exists = os.path.isfile(cfg.data_path)
    with open(cfg.data_path, 'a') as record_file:
        if file_exists: # if file already exists append object with comma
            fileline = ","+json.dumps(infr.__dict__)
        else:   # if file doesnt exist, just write the first object
            fileline = json.dumps(infr.__dict__)
        record_file.write(fileline)

