import streamlit as st
import openai
import tempfile
import os

# Mensagem de boas-vindas e privacidade
st.set_page_config(page_title="🕊️ Projeto Davar – Escuta Viva", layout="centered")
st.title("🕊️ Projeto Davar – Escuta Viva")
st.markdown("Digite ou grave sua pergunta/reflexão abaixo. Davar responderá com escuta, cuidado e profundidade.")
st.markdown("🔒 Todas as conversas são privadas e não são armazenadas. Use com liberdade e respeito.")

# Configurar chave da API OpenAI
openai.api_key = st.secrets.get("openai_api_key", "SUA_CHAVE_AQUI")

# Entrada de texto como alternativa à voz
text_input = st.text_input("Digite aqui sua pergunta, reflexão ou pensamento:")

# Upload de áudio (opcional)
audio_file = st.file_uploader("Ou grave sua voz (MP3/WAV)", type=["mp3", "wav"])

# Transcrição de áudio com Whisper
transcribed_text = ""
if audio_file is not None and st.button("Transcrever áudio"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.read())
        tmp_path = tmp.name
    with open(tmp_path, "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f, language="pt")
        transcribed_text = transcript["text"]
        st.success(f"🗣️ Transcrição: {transcribed_text}")
        os.remove(tmp_path)

# Escolher qual texto usar como input final
final_input = transcribed_text if transcribed_text else text_input

# Enviar para o Davar (modelo GPT)
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
