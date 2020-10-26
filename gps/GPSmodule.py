import serial
import serial.tools.list_ports as lp

import sys
sys.path.append('..')
import config as cfg


class GPS():
    def get_connection(): # workaround
        return

    def __init__(self, attempts = 2):
        self.attempts = attempts # attempts to get gps data in a call to get_gps_data
        self.lat=-1
        self.lon=-1
        self.speed=-1
        #self.valido=1
        self.conn = None
        self.no_connection = True
        self.get_connection()
    
    def get_connection(self):
        ports = list(lp.comports(True))
        gps_port = None
        for p in ports:
            if cfg.gps_hwid in p.hwid:
                gps_port = p.device
        if gps_port is not None:
            try:
                self.conn = serial.Serial(gps_port)#gps0")
                self.no_connection = False
                print("connected to GPS module")
            except:
                print("cant connect to gps module")
        else:
            print("gps is not connected")

    def get_gps_data(self):
        if self.conn:
            for i in range(1, self.attempts):
                try:
                    line = self.conn.readline()
                except:
                    self.conn = None
                    break
                data = line.decode(encoding='us-ascii').split(',')
                if data[0] == "$GPRMC":
                    if data[2] != "A":
                        # dato no valido
                        return (-1,-1,-1)
                    self.lat = (float(data[3]))/100
                    if data[4] == "S":
                        self.lat = -self.lat
                    self.lon = (float(data[5]))/100
                    if data[6]=="W":
                        self.lon = -self.lon
                    self.speed = float(data[7])*1.85
                    break
        else:
            self.get_connection()
            return (-1, -1, -1)
        print(self.lat,self.lon,self.speed)
        return (self.lat,self.lon,self.speed)
    
#invalido=1/valido=0
