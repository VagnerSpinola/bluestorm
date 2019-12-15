import requests

url = 'http://127.0.0.1:5000/import'

token = input('Token: ')

headers = {
    'x-access-token' : token
}

with open('csv/medicamentos.csv', 'rb') as f:
    r = requests.post(url, headers=headers, files={'file': ('medicamentos.csv', f, 'text/csv', {'Expires': '0'})})
    print(r.text)