import requests
with open('ejemplo_payload.txt', 'rb') as f:
    r = requests.put('http://localhost:3030/api/guardar', data={'ejemplo_payload': f})