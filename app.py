import streamlit as st
from openai import OpenAI
import os

# Inicializa cliente da API OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configura página
st.set_page_config(page_title="Projeto Davar", layout="centered")
st.title("🤖 Davar – escuta com presença")
st.markdown("🔒 Nenhuma conversa é salva. Ao fechar esta aba, tudo será apagado.")

# Inicializa histórico
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Botão para nova conversa
if st.button("🧹 Nova conversa"):
    st.session_state.chat_history = []
    st.experimental_rerun()

# Upload de áudio
audio_file = st.file_uploader("Ou envie sua fala como áudio (MP3, WAV, M4A):", type=["mp3", "wav", "m4a"])
user_input = ""

if audio_file:
    with st.spinner("Transcrevendo áudio..."):
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        user_input = transcript.text
        st.markdown(f"**Você disse (transcrito):** {user_input}")

else:
    # Entrada de texto
    user_input = st.text_input("Escreva aqui sua pergunta, desabafo ou reflexão:")

# Função para gerar resposta com histórico
def gerar_resposta_com_gpt(historico):
    messages = [{"role": "system", "content": "Você é o Davar, um parceiro de escuta. Responda com empatia, profundidade e presença."}]
    messages.extend(historico)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# Processa entrada
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    resposta = gerar_resposta_com_gpt(st.session_state.chat_history)
    st.session_state.chat_history.append({"role": "assistant", "content": resposta})

# Exibe histórico formatado
for mensagem in st.session_state.chat_history:
    if mensagem["role"] == "user":
        st.markdown(f"**Você:** {mensagem['content']}")
    elif mensagem["role"] == "assistant":
        st.markdown(f"**Davar:** {mensagem['content']}")
