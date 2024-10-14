import streamlit as st
import requests

# Configurações da NewsAPI
API_KEY = 's'
BASE_URL = 'https://newsapi.org/v2/top-headlines'

# Função para buscar notícias
def buscar_noticias(pais='pt', categoria='technology'):
    parametros = {
        'apiKey': API_KEY,
        'country': pais,
        'category': categoria,
    }
    resposta = requests.get(BASE_URL, params=parametros)
    if resposta.status_code == 200:
        return resposta.json().get('articles', [])
    else:
        st.error("Erro ao buscar notícias!")
        return []

# Configuração do Streamlit
st.title("Notícias Atualizadas")
st.sidebar.header("Filtros")

# Filtros
pais = st.sidebar.selectbox(
    "Escolha o País", 
    options=["pt", "us", "gb", "ca", "de", "fr"], 
    index=0
)
categoria = st.sidebar.selectbox(
    "Escolha a Categoria", 
    options=["business", "entertainment", "general", "health", "science", "sports", "technology"],
    index=6
)

# Botão para buscar notícias
if st.sidebar.button("Buscar"):
    noticias = buscar_noticias(pais, categoria)
    if noticias:
        for noticia in noticias:
            st.subheader(noticia['title'])
            st.write(f"Fonte: {noticia['source']['name']}")
            st.write(noticia['description'])
            if noticia['urlToImage']:
                st.image(noticia['urlToImage'])
            st.markdown(f"[Leia mais]({noticia['url']})")
            st.write("---")
    else:
        st.write("Nenhuma notícia encontrada.")

