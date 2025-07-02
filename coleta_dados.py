import requests
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone

load_dotenv()  # Carrega as variáveis do .env
api_key = os.getenv("API_KEY")

headers = {
    "X-API-Key": api_key
}
coordinates_copacabana = "-22.9719,-43.1843" #Coordenadas de Copacabana, pode ser alterado para outras localidades
radius_meters = 25000  # Raio em metros

# Datas para filtro 
data_fim = datetime.now(timezone.utc)
data_inicio = data_fim - timedelta(days=7)

# Busca as localizações dentro do raio especificado
print(f"Buscando localizações dentro do raio de {radius_meters/1000} km de {coordinates_copacabana} (Copacabana)...")
locations_url = "https://api.openaq.org/v3/locations" # Endpoint para buscar localizações
locations_params = {
    "coordinates": coordinates_copacabana,
    "radius": radius_meters,
    "limit": 1000 
}

response_locations = requests.get(locations_url, headers=headers, params=locations_params)

if response_locations.status_code != 200:
    print(f"Erro ao buscar localizações por ponto e raio: {response_locations.status_code}")
    print(response_locations.text)
    exit() 

locations_data = response_locations.json()
all_sensor_ids = []
found_locations_count = 0

for loc in locations_data.get('results', []):
    found_locations_count += 1
    if 'sensors' in loc and isinstance(loc['sensors'], list):
        for sensor in loc['sensors']:
            if 'id' in sensor:
                all_sensor_ids.append(sensor['id'])

if not all_sensor_ids:
    print(f"Nenhuma localização ou sensor encontrado dentro do raio de {radius_meters/1000} km de {coordinates_copacabana}.")
    exit()

print(f"Encontradas {found_locations_count} localizações com um total de {len(all_sensor_ids)} sensores dentro do raio.")
print(f"IDs dos sensores coletados: {all_sensor_ids}")

# Obter as medições dos sensores encontrados
all_results = []
url_measurements_base = "https://api.openaq.org/v3/sensors/{sensor_id}/measurements"

for sensor_id in all_sensor_ids:
    print(f"Buscando medições para o sensor ID: {sensor_id}...")
    params_measurements = {
        "date_from": data_inicio.isoformat(timespec='seconds') + 'Z',
        "date_to": data_fim.isoformat(timespec='seconds') + 'Z',
        "limit": 1000,
        "page": 1,
    }

    while True:
        current_measurements_url = url_measurements_base.format(sensor_id=sensor_id)
        response = requests.get(current_measurements_url, headers=headers, params=params_measurements)

        if response.status_code != 200:
            print(f"Erro na requisição para sensor {sensor_id}: {response.status_code}")
            print(response.text)
            break # Pula para o próximo sensor em caso de erro

        data = response.json()
        results = data.get("results", [])
        if not results:
            break

        all_results.extend(results)

        meta = data.get("meta", {})
        current_page = meta.get("page")
        total_pages = meta.get("pages")

        if total_pages is None or current_page is None or current_page >= total_pages:
            break

        params_measurements["page"] += 1

if all_results:
    df = pd.DataFrame(all_results)

    # Conversão de colunas de data 
    if 'utc' in df.columns:
        df['utc'] = pd.to_datetime(df['utc'])
    if 'local' in df.columns:
        df['local'] = pd.to_datetime(df['local'])
    if 'date' in df.columns and isinstance(df['date'].iloc[0], dict):
        df['utc_time'] = pd.to_datetime(df['date'].apply(lambda x: x.get('utc')))
        df['local_time'] = pd.to_datetime(df['date'].apply(lambda x: x.get('local')))
        df = df.drop(columns=['date']) 

    contagem_poluentes = df["parameter"].value_counts()
    print("Quantidade de medições por poluente nos últimos 7 dias:")
    print(contagem_poluentes)
    df.to_csv("medicoes_copacabana_7dias_raio.csv", index=False, encoding="utf-8-sig")
    print("CSV salvo como 'medicoes_copacabana_7dias_raio.csv'.")
else:
    print("Nenhuma medição encontrada.")

