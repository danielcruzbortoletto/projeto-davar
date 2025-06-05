import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Projeto Davar", layout="centered")

# CARREGAR VARIÁVEIS DE AMBIENTE
load_dotenv()

# INTERFACE
st.markdown("<h1 style='text-align: center;'>Projeto Davar</h1>", unsafe_allow_html=True)

# Exibir imagem de topo
imagem_path = os.path.join(os.path.dirname(__file__), "topo.png")
if os.path.exists(imagem_path):
    st.image(imagem_path)
else:
    st.warning("Imagem de topo não encontrada.")

# CAMPO DE TEXTO
mensagem_usuario = st.text_area("Escreva aqui sua pergunta ou desabafo:")

# BOTÃO ENVIAR
if st.button("Enviar"):
    if mensagem_usuario.strip():
        st.markdown("🔄 Gerando resposta, por favor aguarde...")
        try:
            client = OpenAI()
            resposta = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Você é uma presença acolhedora e sensível."},
                    {"role": "user", "content": mensagem_usuario}
                ]
            )
            st.markdown("### ✨ Resposta do Davar:")
            st.markdown(resposta.choices[0].message.content)
        except Exception as e:
            st.error("Erro ao gerar resposta: " + str(e))
    else:
        st.warning("Por favor, escreva algo antes de enviar.")

# RODAPÉ
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: small;'>💡 Projeto sem fins lucrativos, feito com propósito e cuidado.</p>", unsafe_allow_html=True)



