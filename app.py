import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# Carrega a chave da API do arquivo .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Inicializa cliente OpenAI
client = OpenAI(api_key=api_key)

# Função de conversa com o Davar
def conversar_com_davar(entrada):
    mensagens = [
        {"role": "system", "content": "Você é Davar, um assistente com escuta profunda, espiritualidade não religiosa e acolhimento humano. Responda com cuidado, clareza e leveza, sempre incentivando a reflexão."},
        {"role": "user", "content": entrada}
    ]

    resposta = client.chat.completions.create(
        model="gpt-4o",
        messages=mensagens,
        temperature=0.7
    )

    return resposta.choices[0].message.content.strip()

# Interface Streamlit
st.title("🕊️ Projeto Davar – Escuta Viva")
st.write("Digite sua reflexão, pergunta ou pensamento. Davar responderá com escuta, cuidado e profundidade.")

entrada = st.text_area("Você deseja conversar sobre o quê?")

if st.button("Conversar com Davar"):
    if entrada.strip():
        resposta = conversar_com_davar(entrada)
        st.markdown("### Resposta do Davar")
        st.write(resposta)
    else:
        st.warning("Por favor, escreva algo antes de clicar.")
