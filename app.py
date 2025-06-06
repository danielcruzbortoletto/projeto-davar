
import streamlit as st
from openai import OpenAI
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
import av
import numpy as np
import tempfile
import os
import io

# CONFIG
st.set_page_config(page_title="Davar Acolhe", layout="centered")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# SIDEBAR
with st.sidebar:
    st.header("🧓 Sobre o Davar Acolhe")
    st.markdown("""
    O **Davar Acolhe** é uma presença amiga e acolhedora.

    Aqui, você pode falar e será ouvido com atenção e carinho.

    **Como usar:**
    - Clique em "Gravar", fale e depois clique em "Parar".
    - O Davar vai ouvir e responder com afeto.
    - Nenhuma conversa é salva. Tudo é apagado ao sair.

    📩 [contato@projetodavar.com](mailto:contato@projetodavar.com)
    """)

# TÍTULO
st.title("🤖 Davar Acolhe")

st.markdown("**Clique em gravar, fale com calma, depois clique em parar.**")

# ÁUDIO CAPTURA
class AudioRecorder(AudioProcessorBase):
    def __init__(self):
        self.frames = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray()
        self.frames.append(audio)
        return frame

ctx = webrtc_streamer(
    key="audio",
    mode=WebRtcMode.SENDONLY,
    audio_receiver_size=256,
    audio_processor_factory=AudioRecorder,
    async_processing=false,
)

if ctx and ctx.audio_processor:
    st.write("🎙️ Áudio capturado:", len(ctx.audio_processor.frames))

    if st.button("✅ Enviar áudio"):
        frames = ctx.audio_processor.frames
        if frames:
            audio = np.concatenate([f.flatten() for f in frames])
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            audio.astype(np.int16).tofile(temp_audio.name)

            with open(temp_audio.name, "rb") as f:
                audio_buffer = io.BytesIO(f.read())
                audio_buffer.name = "voz.wav"

            with st.spinner("🔍 Transcrevendo..."):
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_buffer,
                    language="pt"
                )
                user_input = transcript.text
                st.markdown(f"**Você disse:** {user_input}")

                resposta = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Você é uma presença amiga, acolhedora, que responde com carinho, atenção e simplicidade."},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.6
                )
                st.markdown(f"**Davar responde:** {resposta.choices[0].message.content.strip()}")
        else:
            st.warning("Nenhum áudio detectado ainda.")
