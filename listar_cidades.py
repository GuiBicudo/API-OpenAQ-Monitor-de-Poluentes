import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Carrega as variáveis do .env
api_key = os.getenv("API_KEY")

url = "https://api.openaq.org/v3/locations"
params = {
    "limit": 100,  # Ajuste o limite conforme necessário. Aqui serão listadas as cidades com o ID de cada uma em frente a elas.
}
headers = {
    "X-API-Key": api_key
}

response = requests.get(url, headers=headers, params=params)
data = response.json()
for loc in data['results']:
    print(loc['id'], "-", loc['name'])
