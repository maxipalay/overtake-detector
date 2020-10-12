import serial
from time import sleep
class GPS():
    def get_connection(): # workaround
        return

    def __init__(self, attempts = 2):
        self.attempts = attempts # attempts to get gps data in a call to get_gps_data
        self.lat="0.0"
        self.lon="0.0"
        self.speed=""
        self.valido=1
        self.conn = None
        self.no_connection = True
        self.get_connection()
    
    def get_connection(self):
        try:
            self.conn = serial.Serial("/dev/gps0")
            self.no_connection = False
        except:
            print("cant connect to gps module")

    def get_gps_data(self):
        if self.conn:
            for i in range(1, self.attempts):
                line = self.conn.readline()
                data = line.split(",")
                if data[0] == "$GPRMC":
                    if data[2] == "A":
                        self.valido = 0
                    self.lat = (float(data[3]))/100
                    if data[4] == "S":
                        self.lat = -lat
                    lon = (float(data[5]))/100
                    if data[6]=="W":
                        self.lon = -lon
                    self.speed = float(data[7])*1.85
                    break
        else:
            self.get_connection()
            return None
        return self.valido,self.lat,self.lon,self.speed
    
#invalido=1/valido=0
