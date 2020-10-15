import base64
file_object = open('ejemplo_payload.txt', 'a')
mat="ABC1111"
fecha=20000101 #hhhhmmdd
hora=121212 #hhmmss
lat=0.1
lon=0.1
vel=0.1
foto=""
with open("my_image.jpg", "rb") as img_file:
    foto = base64.b64encode(img_file.read())
strin="{ \"matricula\":\""+str(mat)+"\",\"fecha\":\""+str(fecha)+ "\",\"hora\":\""+str(hora)+"\",\"latitud\":"+str(lat) +",\"longitud\":"+str(lon) +",\"velocidad\":"+str(vel) +",\"foto\":\""+foto+"\"},"

file_object.write(strin)
print("-------------------esctibio------------------")