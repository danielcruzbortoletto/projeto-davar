import streamlit as st
import numpy as np
import wave
import tempfile
import av
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode

st.set_page_config(page_title="Teste de Áudio", layout="centered")
st.title("🎤 Teste de Gravação de Microfone")

class AudioRecorder(AudioProcessorBase):
    def __init__(self):
        self.frames = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray()
        self.frames.append(audio)
        return frame

ctx = webrtc_streamer(
    key="audio-test",
    mode=WebRtcMode.SENDONLY,
    audio_receiver_size=256,
    audio_processor_factory=AudioRecorder,
    async_processing=True,
)

from pydub import AudioSegment

if ctx and ctx.audio_processor:
    st.write("🎙️ Frames capturados:", len(ctx.audio_processor.frames))
    if st.button("🔴 Salvar gravação"):
        frames = ctx.audio_processor.frames
        if frames:
            audio = np.concatenate([frame.flatten() for frame in frames])
            temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")

            # Grava WAV cru
            with wave.open(temp_wav.name, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(48000)
                wf.writeframes(audio.tobytes())

            # Reabre com pydub para normalizar
            audio_seg = AudioSegment.from_wav(temp_wav.name)
            audio_seg = audio_seg.normalize()

            # Salva novamente
            audio_seg.export(temp_wav.name, format="wav")

            st.success("✅ Áudio salvo com sucesso!")
            st.audio(temp_wav.name, format='audio/wav')
            st.session_state['audio_file'] = temp_wav.name
        else:
            st.warning("Nenhum áudio capturado.")
