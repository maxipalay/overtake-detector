import base64
from cv2 import imencode

class Infraction():
    def __init__(self, plate, dat, tim, gps_data, img):
        self.plate = plate
        self.dat = dat
        self.tim = tim
        (self.lat, self.lon, self.vel) = gps_data
        r,buf = imencode('.jpg',img)
        img_string = base64.b64encode(buf)
        self.img = img_string.decode('utf-8')



