import requests
from getpass import getpass

api_url = "https://suap.ifrn.edu.br/api/"

password = getpass()
ano = str(input("digite o ano: "))
periodo = str(input("digite o ano: "))

data = {"username":"20191181110013","password":password}

response = requests.post(api_url+"v2/autenticacao/token/", json=data)
token = response.json()["access"]
print(response.json())

headers = {
    "Authorization": f'Bearer {token}'
}

response = requests.get(api_url+"v2/minhas-informacoes/boletim/"+ano+'/'+periodo, json=data, headers=headers)

print(response.text)
print(response)