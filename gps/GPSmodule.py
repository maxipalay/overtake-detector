import serial
def datosGPS():
    gps= serial.Serial("/dev/gps0",baudrate=9600)
    lat="0.0"
    long="0.0"
    speed=""
    date=""
    time=""
    valido=0
    while True:
        line=gps.readline()
        data = line.split(",")
        if data[0] =="$GPRMC":
            if data[2]=="A":
                valido=1
            lat = (float(data[3]))/100
            if data[4]=="S":
                lat=-lat
            long= (float(data[5]))/100
            if data[6]=="W":
                    long=-long
            speed=float(data[7])*1.85
            break
    return valido,lat,long,speed
