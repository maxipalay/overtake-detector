import base64
import sys
sys.path.append('..')
import config as cfg

import sys
sys.path.append('..')
import config as cfg
from cv2 import imencode

def save_infraction(image, date, time, gps_data):
    (lat, lon, vel) = gps_data
    plate = cfg.plate
    r,buf = imencode('.jpg',image)
    img_string = base64.b64encode(buf)
    record = " \"matricula\":\"{}\",\"fecha\":\"{}\",\"hora\":\"{}\",\"latitud\":{},\"longitud\":{},\"velocidad\":{},\"foto\":\"{}\"".format(cfg.plate, str(date), str(time), lat, lon, vel, img_string.decode('utf-8'))
    record = "{"+record+"},"
    with open(cfg.data_path, 'a') as record_file:
        record_file.write(record)
