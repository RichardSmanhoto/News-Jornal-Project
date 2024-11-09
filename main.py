import streamlit as st
import requests
from googletrans import Translator  # Importa o Google Translator

categorias = {
    "Geral": "general",
    "Negócios": "business",
    "Entretenimento": "entertainment",
    "Ciência": "science",
    "Esportes": "sports",
    "Tecnologia": "technology"
}

# Configurações da NewsAPI
API_KEY = 'd4b29949d7514a2f8a5128eb2a8bf8e7'
BASE_URL = 'https://newsapi.org/v2/top-headlines'

# Inicializa o tradutor
translator = Translator()

# Função para buscar notícias
def buscar_noticias(categoria='general'):
    parametros = {
        'apiKey': API_KEY,
        'country': 'us',
        'category': categoria,
        'pageSize': 10
    }
    resposta = requests.get(BASE_URL, params=parametros)
    if resposta.status_code == 200:
        return resposta.json().get('articles', [])
    else:
        st.error("Erro ao buscar notícias!")
        return []


st.markdown(
    """
    <style>
    .header {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 40px;
        font-weight: bold;
        color: #8B4513;
        padding: 20px;
        background-color: #F5F5DC;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="header">
        Hora de Café
    </div>
    """,
    unsafe_allow_html=True
)


# Configuração do Streamlit
st.title("Notícias Atualizadas")
st.sidebar.header("Filtros")

# Filtros
categoria_filtro = st.sidebar.selectbox(
    "Escolha a Categoria", 
    options=list(categorias.keys()),  # Opções em português
    index=0
)

categoria = categorias[categoria_filtro]

# Botão para buscar notícias
if st.sidebar.button("Buscar"):
    noticias = buscar_noticias(categoria)
    if noticias:
        for noticia in noticias:
            try:
                # Tenta traduzir o título e o parágrafo da notícia para português
                titulo_traduzido = translator.translate(noticia['title'], dest='pt').text
            except Exception as e:
                titulo_traduzido = "Título indisponível"

            try:
                descricao_traduzida = translator.translate(noticia['description'], dest='pt').text if noticia['description'] else "Sem descrição disponível"
            except Exception as e:
                descricao_traduzida = "Descrição indisponível"
                
            
            st.subheader(titulo_traduzido)  # Exibe o título traduzido
            st.write(f"Fonte: {noticia['source']['name']}")
            st.write(descricao_traduzida)  # Exibe a descrição traduzida
            st.markdown(f"[Leia mais]({noticia['url']})")
        
            if noticia['urlToImage']:
                st.image(noticia['urlToImage'])
            st.write("---")
    else:
        st.write("Nenhuma notícia encontrada.")
