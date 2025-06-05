import streamlit as st
import openai
import tempfile
import os
from dotenv import load_dotenv
import soundfile as sf
import io

# CONFIGURAÇÕES INICIAIS
st.set_page_config(page_title="Davar", layout="centered")
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# SIDEBAR COM ORIENTAÇÕES
with st.sidebar:
    st.header("💬 Sobre o Davar")
    st.markdown("""
    O **Davar** é um espaço de escuta com presença.

    Aqui, você pode escrever ou enviar um áudio — sem julgamentos, sem pressa.

    **Como usar:**
    - Digite sua mensagem ou envie um áudio (formato .wav, .mp3, etc.).
    - O Davar responde com empatia e sensibilidade.
    - Nenhuma conversa é salva. Tudo é apagado ao sair.

    ---
    💡 *Projeto sem fins lucrativos, feito com propósito e cuidado.*

    📩 **Contato:** contato@projetodavar.com
    """)

st.title("🧠 Davar: escuta com presença")

# Função para transcrever o áudio com Whisper
def transcrever_audio(audio_bytes):
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "audio.wav"
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript["text"]

# Função para gerar resposta com GPT
def gerar_resposta(mensagem):
    resposta = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é uma presença acolhedora que escuta com empatia e responde com sensibilidade."},
            {"role": "user", "content": mensagem},
        ]
    )
    return resposta["choices"][0]["message"]["content"]

# INPUT DO USUÁRIO
entrada_texto = st.text_area("✍️ Escreva algo (ou envie um áudio abaixo):", placeholder="Como você está hoje?")

arquivo_audio = st.file_uploader("📢 Ou envie um áudio", type=["wav", "mp3", "m4a", "ogg"])

mensagem = None

if arquivo_audio is not None:
    audio_bytes = arquivo_audio.read()
    with st.spinner("Transcrevendo o áudio..."):
        try:
            mensagem = transcrever_audio(audio_bytes)
            st.success("Transcrição: " + mensagem)
        except Exception as e:
            st.error(f"Erro na transcrição do áudio: {str(e)}")

elif entrada_texto.strip():
    mensagem = entrada_texto.strip()

# GERAÇÃO DE RESPOSTA
if mensagem:
    with st.spinner("Davar está escutando..."):
        try:
            resposta = gerar_resposta(mensagem)
            st.markdown("**🗣️ Davar responde:**")
            st.markdown(resposta)
        except Exception as e:
            st.error(f"Erro ao gerar resposta: {str(e)}")
