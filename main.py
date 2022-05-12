import pandas as pd
import geopandas
import streamlit as st
import folium
import plotly.express as px

from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

import os

st.set_page_config(layout='wide')

option = st.selectbox('Qual cidade você gostaria de exibir os dados?',
                      ('Rio de Janeiro', 'London', 'Los Angeles'), index=0)
if option == 'Rio de Janeiro':
    id_city = 'rj'
    title = 'Rio de Janeiro'
elif option == 'London':
    id_city = 'london'
    title = 'London'
else:
    id_city = 'los_angeles'
    title = 'Los Angeles'

base_path = os.path.dirname(os.path.realpath(__file__))

DATA_PATH = os.path.join(base_path, "data",
                         f"airbnb_{id_city}.csv")

GEOJSON_PATH = os.path.join(base_path, "data",
                            f"neighbourhoods_{id_city}.geojson")


@st.cache(allow_output_mutation=True)
def read_df(DATA_PATH: str) -> pd.DataFrame:
    """Faz a leitura do DataFrame com os dados
    coletados do Airbnb.

    Parameters
    ----------
    DATA_PATH : str
        Caminho onde está localizado o arquivo .csv

    Returns
    -------
    pd.DataFrame
        DataFrame com os dados do Airbnb.
    """
    data = pd.read_csv(DATA_PATH)
    return data


def get_geofile(GEOJSON_PATH: str) -> geopandas.GeoDataFrame:
    """Faz leitura do arquivo GeoJson

    Parameters
    ----------
    GEOJSON_PATH : str
        Caminho onde está localizado o arquivo GeoJson.

    Returns
    -------
    geopandas.GeoDataFrame
        DataFrame com os dados do GeoJson
    """
    geo = geopandas.read_file(GEOJSON_PATH)
    return geo


# Load data
df = read_df(DATA_PATH)
geo = get_geofile(GEOJSON_PATH)
rtype_label = df.room_type.unique().tolist()
neighbourhood_label = df.neighbourhood.sort_values().unique().tolist()

# Sidebar
info_sidebar = st.sidebar.empty()

price_filter = \
    int(st.sidebar.number_input('Escolha o valor máximo por noite.'))

st.sidebar.subheader("Tabela de Dados")
table = st.sidebar.empty()

room_type_filter = st.sidebar.multiselect(
    label="Escolha o tipo de lugar",
    options=rtype_label,
    default=rtype_label
)

filtered_df = df[(df.price <= price_filter) &
                 (df.room_type.isin(room_type_filter))]

tb = filtered_df[['name', 'host_name', 'neighbourhood',
                  'room_type', 'price', 'minimum_nights']]

tb.columns = ['Descrição', 'Anfitrião', 'Bairro',
              'Tipo de lugar', 'Valor', 'Mínimo de noites']

info_sidebar.info(f"{filtered_df.shape[0]} opções carregadas.")

# Main
st.title(f"Airbnb - {title}")
st.markdown(f"""
            Estão sendo exibidos os lugares
            de até **R${price_filter}** por noite""")

# Raw data
if table.checkbox("Exibir tabela de dados"):
    st.write(tb)

c1, c2 = st.columns((1, 1))

c1.header('Mapa das hospedagens')
marker_map = folium.Map(location=[filtered_df['latitude'].mean(),
                        filtered_df['longitude'].mean()],
                        tiles='cartodbpositron',
                        default_zoom_start=10)

marker_cluster = MarkerCluster().add_to(marker_map)
for name, row in filtered_df.iterrows():
    folium.Marker([row['latitude'], row['longitude']],
                  popup=f"Price: R${row['price']}"
                  ).add_to(marker_cluster)

with c1:
    folium_static(marker_map, width=550)

c2.header('Mapa de densidade de preço')


# Filtra os bairros que somente estão no geojson e no df
geo = geo[geo['neighbourhood'].isin(filtered_df['neighbourhood'].tolist())]

map_density = folium.Map(location=[filtered_df['latitude'].mean(),
                         filtered_df['longitude'].mean()],
                         tiles='cartodbpositron',
                         default_zoom_start=10)

folium.Choropleth(
    data=filtered_df,
    geo_data=geo,
    columns=[
        'neighbourhood',
        'price'],
    key_on='feature.properties.neighbourhood',
    fill_color='YlOrRd',
    fill_opacity=0.5,
    line_opacity=0.2,
    legend_name='Média de preço').add_to(map_density)


with c2:
    folium_static(map_density, width=550)

st.sidebar.subheader("Estatísticas")

# checkbox total por lugar
table_room_type = st.sidebar.empty()
if table_room_type.checkbox("Total por tipo de hospedagem"):
    fig = px.histogram(filtered_df, x='room_type',
                       labels={
                           'room_type': 'Tipo de hospedagem'
                       },
                       title='Tipo de hospedagem')
    st.plotly_chart(fig, use_container_width=True)

# checkbox bairros com mais hospedagem
table_neighborhood = st.sidebar.empty()
if table_neighborhood.checkbox("Hospedagem por bairro"):
    fig = px.histogram(filtered_df, x='neighbourhood',
                       labels={
                           'neighbourhood': 'Bairro'
                       },
                       title='Hospedagem por Bairro')
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
