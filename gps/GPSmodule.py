import serial
def datosGPS():
   
    lat="0.0"
    long="0.0"
    speed=""
    date=""
    time=""
    valido=1
    
    var=false 
    try:
        gps= serial.Serial("/dev/gps0",baudrate=9600)
        var = true
    except:
        print("No se encuentra GPS")
    while var:
        line=gps.readline()
        data = line.split(",")
        if data[0] =="$GPRMC":
            if data[2]=="A":
                valido=0
            lat = (float(data[3]))/100
            if data[4]=="S":
                lat=-lat
            long= (float(data[5]))/100
            if data[6]=="W":
                    long=-long
            speed=float(data[7])*1.85
            break
    return valido,lat,long,speed
#invalido=1/valido=0
