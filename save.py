import time
import requests
import ping as sd

url = 'https://179.27.99.46:3030/'

initial_time = time.time() #Store the time when request is sent
sd.ping("179.27.99.46")
ending_time = time.time() #Time when acknowledged the request
elapsed_time = (ending_time - initial_time)
print(elapsed_time)

if elapsed_time < 1.5:
    print("entra")
    try:
        myobj = {'somekey': 'somevalue'}
        x=requests.put(url,data = myobj)
        print(x.status_code)
    except requests.exceptions.ConnectionError:
        x.status_code = "Connection refused"
