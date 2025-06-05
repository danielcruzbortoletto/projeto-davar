import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import tempfile
import soundfile as sf

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Projeto Davar", layout="centered")

# CARREGAR VARIÁVEIS DE AMBIENTE
load_dotenv()

# SIDEBAR COM ORIENTAÇÕES
with st.sidebar:
    st.header("💬 Sobre o Davar")
    st.markdown("""
    O **Davar** é um espaço de escuta com presença.

    Aqui, você pode escrever ou enviar um áudio — sem julgamentos, sem pressa.

    **Como usar:**
    - Escreva ou envie sua pergunta, desabafo ou reflexão.
    - O Davar responde com empatia e sensibilidade.
    - Nenhuma conversa é salva. Tudo é apagado ao sair.

    ---
    💡 *Projeto sem fins lucrativos, feito com propósito e cuidado.*

    📩 **Contato:** [contato@projetodavar.com](mailto:contato@projetodavar.com)
    """)

# TÍTULO E IMAGEM DE TOPO
st.markdown("<h1 style='text-align: center;'>Projeto Davar</h1>", unsafe_allow_html=True)

imagem_path = os.path.join(os.path.dirname(__file__), "topo.png")
if os.path.exists(imagem_path):
    st.image(imagem_path)

# OPÇÃO DE TEXTO
mensagem_usuario = st.text_area("Escreva aqui sua pergunta ou desabafo:")

# OPÇÃO DE ÁUDIO
audio_file = st.file_uploader("Ou envie um áudio (formato .wav ou .mp3)", type=["wav", "mp3"])

# BOTÃO DE ENVIO
if st.button("Enviar"):
    if mensagem_usuario.strip():
        prompt = mensagem_usuario.strip()
    elif audio_file:
        with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
            temp_audio.write(audio_file.read())
            temp_audio_path = temp_audio.name

        try:
            client = OpenAI()
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=open(temp_audio_path, "rb")
            )
            prompt = transcription.text
            st.success("Áudio transcrito com sucesso.")
            st.markdown(f"**Transcrição:** {prompt}")
        except Exception as e:
            st.error("Erro ao transcrever áudio: " + str(e))
            prompt = None
    else:
        st.warning("Por favor, escreva ou envie um áudio.")
        prompt = None

    if prompt:
        try:
            client = OpenAI()
            resposta = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Você é uma presença acolhedora e sensível."},
                    {"role": "user", "content": prompt}
                ]
            )
            st.markdown("### ✨ Resposta do Davar:")
            st.markdown(resposta.choices[0].message.content)
        except Exception as e:
            st.error("Erro ao gerar resposta: " + str(e))

# RODAPÉ
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: small;'>💡 Projeto sem fins lucrativos, feito com propósito e cuidado.</p>", unsafe_allow_html=True)



