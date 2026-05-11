import os
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import numpy as np

# Instala as bibliotecas se estiver no Colab (descomente a linha abaixo se precisar)
# !pip install geopandas shapely

# Cria a pasta dados
os.makedirs('dados', exist_ok=True)

# Limites geográficos aproximados de Minas Gerais
lon_min, lon_max = -51.0, -39.0
lat_min, lat_max = -22.0, -14.0

def gerar_mock_desmatamento(nome_arquivo, qtd_focos):
    print(f"Gerando dados simulados para {nome_arquivo}...")

    # Gera coordenadas aleatórias dentro de MG
    lons = np.random.uniform(lon_min, lon_max, qtd_focos)
    lats = np.random.uniform(lat_min, lat_max, qtd_focos)

    # Cria polígonos (buffer em volta do ponto simula a área desmatada)
    # O tamanho do buffer varia aleatoriamente
    geometrias = [Point(lon, lat).buffer(np.random.uniform(0.01, 0.05)) for lon, lat in zip(lons, lats)]

    # Sorteia os biomas de MG
    biomas = np.random.choice(['Cerrado', 'Mata Atlântica', 'Caatinga'], qtd_focos, p=[0.55, 0.40, 0.05])

    # Cria o GeoDataFrame (em WGS84 - EPSG:4326, que é o padrão de GPS)
    gdf = gpd.GeoDataFrame({'bioma': biomas}, geometry=geometrias, crs="EPSG:4326")

    # Salva como GeoPackage (.gpkg)
    gdf.to_file(f'dados/{nome_arquivo}', driver="GPKG")
    print(f"✅ {nome_arquivo} criado com sucesso!")

# Gera 150 focos para agosto e 200 para setembro
gerar_mock_desmatamento('desmatamento_ago22.gpkg', 150)
gerar_mock_desmatamento('desmatamento_set_22.gpkg', 200)