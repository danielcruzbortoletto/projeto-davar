import streamlit as st
from openai import OpenAI
import os
import io

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Projeto Davar", layout="centered")
st.title("🤖 Davar – escuta com presença")

# MANIFESTO
st.markdown("""
> **🌱 Bem-vindo ao Davar**  
> Aqui, você encontra uma escuta com presença, sem julgamentos.  
> Um espaço para respirar, pensar, sentir e recomeçar.
>
> 🔒 Nenhuma conversa é salva. Ao fechar esta aba, tudo é apagado.
""")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.button("🧹 Nova conversa"):
    st.session_state.chat_history = []
    st.experimental_rerun()

audio_file = st.file_uploader("Ou envie sua fala como áudio (MP3, WAV, M4A):", type=["mp3", "wav", "m4a"])
user_input = ""

if audio_file:
    with st.spinner("Transcrevendo áudio..."):
        audio_bytes = audio_file.read()
        audio_buffer = io.BytesIO(audio_bytes)
        audio_buffer.name = audio_file.name

        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_buffer
        )
        user_input = transcript.text
        st.markdown(f"**Você disse (transcrito):** {user_input}")
else:
    user_input = st.text_input("Escreva aqui sua pergunta, desabafo ou reflexão:")

# NOVO PROMPT DO DAVAR
def gerar_resposta_com_gpt(historico):
    system_prompt = (
        "Você é o Davar, uma presença de escuta e cuidado. "
        "Responda com empatia, sem pressa, valorizando o que é dito e acolhendo a pessoa como ela é. "
        "Use uma linguagem próxima, com humanidade e sensibilidade. "
        "Você pode fazer pequenas pausas poéticas ou reflexivas, se for apropriado. "
        "Evite parecer um robô ou um terapeuta técnico. "
        "Seu papel é escutar, refletir e estar junto com palavras que tocam e inspiram."
    )
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(historico)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    resposta = gerar_resposta_com_gpt(st.session_state.chat_history)
    st.session_state.chat_history.append({"role": "assistant", "content": resposta})

for mensagem in st.session_state.chat_history:
    if mensagem["role"] == "user":
        st.markdown(f"**Você:** {mensagem['content']}")
    elif mensagem["role"] == "assistant":
        st.markdown(f"**Davar:** {mensagem['content']}")
