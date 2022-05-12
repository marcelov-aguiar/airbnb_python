# Sobre o projeto
O objetivo desse projeto é visualizar os locais de hospedagem do aplicativo Airbnb nas seguintes cidades: Rio de Janeiro, Los Angeles e Londres. Para desenvolver a aplicação foi usada a linguagem de programação Python e as seguintes bibliotecas:
- Pandas
- Geopandas
- Streamlit
- Folium
- Plotly

A partir das informações fornecidas pela aplicação, será possível visualizar os locais de hospedagem conforme o filtro de preço. Além disso, a aplicação conta com dois mapas, sendo eles:
- Mapa das hospedagens: Exibe a localização e o preço das hospedagem em cada bairro da cidade selecionada.
- Mapa de densidade de preço: Exibe a densidade de preço (média dos preços) das hospedagens por bairro.

O projeto foi inteiramente baseado no projeto de Anderson Monteiro (https://github.com/andmonteiro/streamlit-airbnb), apenas com algumas atualizações e modificações.

![Aplicação](img/airbnb.gif)

# Dados
Os dados dos locais de hospedagem foram baixados do site oficial do Airbnb, e pode ser encontrado no seguinte link: http://insideairbnb.com/get-the-data/

Foram usados o dataset `listings.csv` e o GeoJSON `neighbourhoods.geojson` que possui a delimitação dos bairros da cidade escolhida.

Foi realizado um simples tratamento no dataset, e o código deste tratamento pode ser encontrado no seguinte Jupyter Notebook: `processing.ipynb`.

OBS: Os dados utilizados estão no diretório `/data`.

# Execução do projeto
Para executar a aplicação será necessário instalar a versão >=3 da linguagem de programação Python. Link para download: https://www.python.org/downloads/

Após a sua instalação será necessário instalar os pacotes descritos no `requirements.txt` pelo seguinte comando no terminal:
```
pip install -r requirements.txt
```

Em seguida será possível executar o projeto no terminal pelo comando:
```
streamlit run app.py
```

# Referências
- https://github.com/andmonteiro/streamlit-airbnb
- https://www.python.org/downloads/
- http://insideairbnb.com/get-the-data/
