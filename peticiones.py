import requests
import time
url = "http://sistemic.udea.edu.co:4000/reto/autenticacion/oauth/token"
url2 = "http://sistemic.udea.edu.co:4000/seguridad/preprocesamiento/prueba"
url3 = "http://sistemic.udea.edu.co:4000/reto/usuarios/usuarios/listar/"

payload='username=admin&password=1234567890&grant_type=password'
headers = {
  'Authorization': 'Basic Zmx1dHRlci1yZXRvOnVkZWE=',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': 'color=rojo'
}

payload2={}
files2={}
headers2 = {
  'Cookie': 'color=rojo'
}
contador = 1
token = ''
headers3 = {}
while(True):
  if contador == 1:
    response = requests.request("POST", url, headers=headers, data=payload)
    token = response.json()["access_token"]
    headers3 = {'Authorization': 'Bearer '+token, 'Cookie': 'color=rojo'}
  elif contador == 2:
    response = requests.request("GET", url2, headers=headers2, data=payload2, files=files2)
  elif contador == 3:
    response = requests.request("GET", url3, headers=headers3, data=payload2)
  else:
    contador = 0
  contador += 1
  print(response)
  time.sleep(30)