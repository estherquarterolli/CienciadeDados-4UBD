# Monitoramento de desmatamento em Minas Gerais

Este projeto foi desenvolvido como um teste técnico de Ciência de Dados focado na análise geoespacial e socioeconômica para o combate ao desmatamento ilegal no estado de Minas Gerais. O objetivo principal é fornecer insights estratégicos para que gestores públicos possam alocar recursos de fiscalização de forma eficiente.

## Resumo

O projeto consistiu na criação de um pipeline completo de dados, desde a coleta automatizada até a visualização interativa:

1.  **Engenharia de Dados Geoespaciais:** Coleta automatizada da malha municipal de MG via API (`geobr`), padronização para a projeção **EPSG:31983** e cálculo de áreas.
2.  **Integração de Dados Reais:** Consumo da **API SIDRA do IBGE** para obter dados oficiais e atualizados de **População (Censo 2022)** e **PIB (2020)** para todos os 853 municípios mineiros.
3.  **Análise de Impacto:** Cruzamento espacial (*Spatial Join*) entre focos de desmatamento e limites municipais/biomas para identificar as áreas mais afetadas em hectares e km².
4.  **Análise de Correlação:** Estudo estatístico para entender a relação entre o desenvolvimento econômico (PIB/População) e a pressão ambiental (área desmatada).
5.  **Dashboard Executivo:** Desenvolvimento de visualizações claras e um **Mapa Interativo (Folium)** para permitir que o governador e gestores visualizem os "hotspots" de crime ambiental de forma intuitiva.

## Mock Data
Como os arquivos originais de desmatamento não foram fornecidos, foi desenvolvido um script de **Mock Data** que gera polígonos aleatórios e classificação de biomas dentro dos limites de Minas Gerais. Isso garante que todo o código e lógica de análise estejam prontos para processar dados reais instantaneamente.

## Estrutura do Repositório

* `01_preparacao_dados.py`: Script de automação para extração de dados (IBGE, geobr) e unificação de arquivos.
* `02_analise.ipynb`: Notebook com análise exploratória, cálculos de área e correlação.
* `03_visualizacao.ipynb`: Visualizações gráficas e mapa interativo para tomada de decisão.
* `dados/`: Diretório contendo os arquivos processados (.geojson, .csv) e o mapa interativo (.html).

## Tecnologias Utilizadas

* **Linguagem:** Python
* **Manipulação Espacial:** GeoPandas, Shapely, Pyogrio
* **Coleta de Dados:** geobr, Requests (API IBGE)
* **Análise e Visualização:** Pandas, Matplotlib, Seaborn, Folium