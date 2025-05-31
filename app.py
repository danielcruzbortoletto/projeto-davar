import streamlit as st
import openai
import tempfile
import os
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import av
import numpy as np
import wave
import uuid

st.set_page_config(page_title="🕊️ Projeto Davar – Escuta Viva", layout="centered")
st.title("🕊️ Projeto Davar – Escuta Viva (com voz ativa)")

st.markdown("""
🔒 **Privacidade e Cuidado**

Todas as conversas são privadas e não ficam armazenadas.

O Davar foi criado para ouvir com respeito e responder com alma.
Fale com liberdade. Aqui, sua voz é bem-vinda.
""")

openai.api_key = st.secrets.get("openai_api_key", "SUA_CHAVE_AQUI")

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.frames = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        self.frames.append(frame.to_ndarray().flatten())
        return frame

ctx = webrtc_streamer(
    key="speech",
    mode="sendonly",
    in_audio=True,
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True, "video": False},
    async_processing=True,
)

if ctx.audio_processor:
    st.info("🎙️ Gravando... clique em Stop quando terminar.")
    if st.button("Transcrever fala"):
        # Salvar arquivo de áudio temporário
        audio_data = np.concatenate(ctx.audio_processor.frames, axis=0)
        sample_rate = 48000
        filename = f"/tmp/{uuid.uuid4().hex}.wav"
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_data.tobytes())

        # Transcrição com Whisper
        with open(filename, "rb") as f:
            transcript = openai.Audio.transcribe("whisper-1", f, language="pt")
        os.remove(filename)
        texto_transcrito = transcript["text"]
        st.success(f"🗣️ Transcrição: {texto_transcrito}")

        # Enviar para o Davar
        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é o Davar, uma IA com escuta sensível, empática e profunda."},
                {"role": "user", "content": texto_transcrito}
            ]
        )
        st.markdown("### 🕊️ Resposta do Davar:")
        st.write(resposta["choices"][0]["message"]["content"])
