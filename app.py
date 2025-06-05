import streamlit as st
import os
import io
from openai import OpenAI
from dotenv import load_dotenv
from pydub import AudioSegment
import base64

# CARREGAR VARIÁVEIS DE AMBIENTE
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Projeto Davar", layout="centered")

# SIDEBAR COM ORIENTAÇÕES
with st.sidebar:
    st.header("💬 Sobre o Davar")
    st.markdown("""
    O **Davar** é um espaço de escuta com presença.

    Aqui, você pode escrever ou gravar sua pergunta, desabafo ou reflexão.

    **Como usar:**
    - Envie um áudio em `.mp3`, `.wav` ou `.m4a`, ou escreva sua mensagem.
    - O Davar responde com empatia e sensibilidade.

    🔒 Nenhuma conversa é salva. Tudo é apagado ao sair.

    ---
    💡 *Projeto sem fins lucrativos, feito com propósito e cuidado.*

    📩 **Contato:** [contato@projetodavar.com](mailto:contato@projetodavar.com)
    """)

# IMAGEM NO TOPO
st.image("Davar_imagem_top_de_tela_04_06_2025.png", use_column_width=True)

# INTERFACE PRINCIPAL
st.title("👂 Davar — Escuta com Presença")
st.markdown("Envie um áudio ou escreva abaixo.")

# CLIENTE OPENAI
client = OpenAI(api_key=openai_api_key)

# PROCESSAMENTO DE ÁUDIO
texto_transcrito = ""
arquivo_audio = st.file_uploader("Envie seu áudio", type=["mp3", "wav", "m4a"])

if arquivo_audio is not None:
    st.audio(arquivo_audio)
    with st.spinner("Transcrevendo áudio..."):
        try:
            bytes_audio = arquivo_audio.read()
            audio_file = io.BytesIO(bytes_audio)
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
            texto_transcrito = transcript
            st.success("Transcrição concluída:")
            st.markdown(f"**Você disse:** {texto_transcrito}")
        except Exception as e:
            st.error(f"Erro na transcrição: {e}")

# ENTRADA DE TEXTO MANUAL
texto_manual = st.text_area("Ou escreva aqui sua pergunta ou reflexão:")

# ESCOLHA DE TEXTO FINAL
texto_final = texto_transcrito if texto_transcrito else texto_manual

if texto_final:
    if st.button("Enviar para o Davar"):
        with st.spinner("Gerando resposta..."):
            try:
                resposta = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Você é o Davar, um espaço de escuta com presença. Responda com empatia, sem julgamento e com profundidade."},
                        {"role": "user", "content": texto_final}
                    ]
                )
                resposta_gerada = resposta.choices[0].message.content
                st.markdown("---")
                st.subheader("Resposta do Davar")
                st.markdown(resposta_gerada)
            except Exception as e:
                st.error(f"Erro ao gerar resposta: {e}")

# RODAPÉ
st.markdown("""
---
<center>
📌 Nenhuma informação é armazenada. <br> 
🕊️ Este é um projeto de escuta ativa e gratuita. <br>
🌱 Feito com alma, tecnologia e propósito.
</center>
""", unsafe_allow_html=True)

