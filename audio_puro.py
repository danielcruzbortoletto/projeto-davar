import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
import av
import numpy as np
import tempfile
from scipy.io.wavfile import write

st.set_page_config(page_title="Áudio Teste Puro", layout="centered")
st.title("🎙️ Teste de Gravação Isolado")

class Recorder(AudioProcessorBase):
    def __init__(self):
        self.frames = []

    def recv_audio(self, frame: av.AudioFrame) -> av.AudioFrame:
        self.frames.append(frame.to_ndarray())
        return frame

ctx = webrtc_streamer(
    key="test-audio",
    mode=WebRtcMode.SENDONLY,
    audio_receiver_size=256,
    audio_processor_factory=Recorder,
    async_processing=True,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},


)

if ctx and ctx.audio_processor:
    st.write("🎛️ Frames:", len(ctx.audio_processor.frames))
    if st.button("Salvar gravação"):
        frames = ctx.audio_processor.frames
        if frames:
            audio = np.concatenate([f.flatten() for f in frames])
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            write(temp_file.name, 48000, audio.astype(np.int16))
            st.success("✅ Áudio salvo!")
            st.audio(temp_file.name)
        else:
            st.warning("Nenhum frame de áudio detectado.")
