import streamlit as st
import openai
import tempfile
import os

st.set_page_config(page_title="🕊️ Projeto Davar – Escuta Viva", layout="centered")
st.title("🕊️ Projeto Davar – Escuta Viva")

st.markdown("""
🔒 **Privacidade e Cuidado**

Todas as conversas são privadas e não ficam armazenadas.

O Davar foi criado para ouvir com respeito e responder com alma.
Fale com liberdade. Aqui, sua voz é bem-vinda.
""")

# Configurar chave da API
openai.api_key = st.secrets.get("openai_api_key", "SUA_CHAVE_AQUI")

# Entrada de texto
text_input = st.text_input("Digite aqui sua pergunta, reflexão ou pensamento:")

# Upload de áudio
audio_file = st.file_uploader("Ou envie sua voz (MP3/WAV)", type=["mp3", "wav"])

# Transcrição com Whisper
transcribed_text = ""
if audio_file is not None and st.button("Transcrever áudio"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.read())
        tmp_path = tmp.name
    with open(tmp_path, "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f, language="pt")
    os.remove(tmp_path)
    transcribed_text = transcript["text"]
    st.success(f"🗣️ Transcrição: {transcribed_text}")

# Escolher o input final
final_input = transcribed_text if transcribed_text else text_input

# Enviar para o Davar
if final_input and st.button("Perguntar ao Davar"):
    with st.spinner("Davar está escutando..."):
        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é o Davar, uma IA com escuta sensível, empática e profunda."},
                {"role": "user", "content": final_input}
            ]
        )
        st.markdown("### 🕊️ Resposta do Davar:")
        st.write(resposta["choices"][0]["message"]["content"])
