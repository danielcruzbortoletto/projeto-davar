import streamlit as st
import soundfile as sf
import tempfile
import os
from openai import OpenAI
from dotenv import load_dotenv

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Projeto Davar", layout="centered")

# CARREGAR VARIÁVEIS DE AMBIENTE
load_dotenv()
client = OpenAI()

# SIDEBAR COM ORIENTAÇÕES
with st.sidebar:
    st.header("💬 Sobre o Davar")
    st.markdown("""
    O **Davar** é um espaço de escuta com presença.

    Aqui, você pode escrever ou gravar livremente — sem julgamentos, sem pressa.

    **Como usar:**
    - Grave ou escreva sua pergunta, desabafo ou reflexão.
    - O Davar responde com empatia e sensibilidade.
    - Nenhuma conversa é salva. Tudo é apagado ao sair.

    ---
    💡 *Projeto sem fins lucrativos, feito com propósito e cuidado.*

    📩 **Contato:** [contato@projetodavar.com](mailto:contato@projetodavar.com)
    """)

st.image("Davar_imagem_top_de_tela_04_06_2025.png")

st.markdown("""<style>footer {visibility: visible;} footer:after {content:'💜 Davar é um projeto de escuta com propósito e presença. Nenhum dado é salvo.'; display: block; text-align: center; padding: 10px;} </style>""", unsafe_allow_html=True)

st.title("🧠 Projeto Davar")
st.markdown("Envie uma reflexão ou pergunta. Pode ser por texto ou por áudio.")

# INPUT DE TEXTO
text_input = st.text_area("Digite aqui (opcional):")

# INPUT DE ÁUDIO
uploaded_file = st.file_uploader("Ou envie um áudio em .wav", type=["wav"])

user_input = text_input.strip()

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        tmpfile.write(uploaded_file.read())
        tmpfile_path = tmpfile.name

    # TRANSCRIÇÃO COM WHISPER
    with st.spinner("Transcrevendo áudio..."):
        try:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=open(tmpfile_path, "rb")
            )
            user_input = transcript.text
            st.success("Transcrição concluída:")
            st.write(user_input)
        except Exception as e:
            st.error("Erro ao transcrever o áudio.")
            st.stop()

if user_input:
    with st.spinner("Gerando resposta do Davar..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Você é o Davar, um espaço de escuta com presença. Responda com empatia, leveza e profundidade, mesmo a perguntas difíceis."},
                    {"role": "user", "content": user_input}
                ]
            )
            output = response.choices[0].message.content
            st.markdown("### 🧾 Resposta do Davar:")
            st.write(output)
        except Exception as e:
            st.error("Erro ao gerar resposta:")
            st.error(str(e))
else:
    st.info("Envie uma pergunta, reflexão ou desabafo.")


