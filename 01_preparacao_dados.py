import pandas as pd
import geopandas as gpd
from geobr import read_municipality
import requests
import warnings
import os

warnings.filterwarnings('ignore')
os.makedirs('dados', exist_ok=True)

# 1. Baixar malha de MG
print("Baixando dados dos municípios de MG...")
mg = read_municipality(code_muni="MG", year=2020)
mg = mg.to_crs(epsg=31983)
mg['area_km2'] = mg.geometry.area / (10**6)
mg.to_file('dados/municipios-mg.geojson', driver='GeoJSON')
print("'municipios-mg.geojson' salvo!")

# 2. Buscar Dados REAIS de População e PIB via API do IBGE
print("Baixando dados REAIS de População e PIB via API do IBGE...")
try:
    # População (Censo 2022) - Agregado 6579 IBGE
    url_pop = "https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/2022/variaveis/93?localidades=N6[N3[31]]"
    req_pop = requests.get(url_pop).json()
    series_pop = req_pop[0]['resultados'][0]['series']
    
    df_pop = pd.DataFrame([
        {'municipio': item['localidade']['nome'].replace(' - MG', ''),
         'populacao_2022': int(item['serie']['2022'])}
        for item in series_pop
    ])

    # PIB (2020) - Agregado 5938 IBGE
    url_pib = "https://servicodados.ibge.gov.br/api/v3/agregados/5938/periodos/2020/variaveis/37?localidades=N6[N3[31]]"
    req_pib = requests.get(url_pib).json()
    series_pib = req_pib[0]['resultados'][0]['series']
    
    df_pib = pd.DataFrame([
        {'municipio': item['localidade']['nome'].replace(' - MG', ''),
         'pib_mil_reais': float(item['serie']['2020'])}
        for item in series_pib
    ])

    # Cruzar os dados (Merge) e salvar o CSV
    df_ibge = pd.merge(df_pop, df_pib, on='municipio', how='inner')
    df_ibge.to_csv('dados/populacao-pib-municipios-mg.csv', index=False)
    print(" 'populacao-pib-municipios-mg.csv' salvo com sucesso (Dados Reais)!")

except Exception as e:
    print(f"Erro ao buscar dados na API do IBGE: {e}")

# 3. Unificar os focos de desmatamento
print("Unificando focos de desmatamento...")
ago = gpd.read_file('dados/desmatamento_ago22.gpkg')
setem = gpd.read_file('dados/desmatamento_set_22.gpkg')
ago['mes'] = 'Agosto'
setem['mes'] = 'Setembro'

focos = pd.concat([ago, setem], ignore_index=True)
focos = gpd.GeoDataFrame(focos, geometry='geometry', crs="EPSG:4326")
focos = focos.to_crs(epsg=31983)
focos.to_file('dados/focos-desmatamento-mg.geojson', driver='GeoJSON')
print(" 'focos-desmatamento-mg.geojson' salvo!")