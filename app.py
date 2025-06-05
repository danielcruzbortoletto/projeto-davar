import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
import numpy as np
import wave
import tempfile
import av
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
from scipy.io.wavfile import write

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Projeto Davar", layout="centered")

# SIDEBAR
with st.sidebar:
    st.header("💬 Sobre o Davar")
    st.markdown("""
    O **Davar** é um espaço de escuta com presença.

    Grave ou escreva sua pergunta, desabafo ou reflexão. 
    O Davar responde com empatia e sensibilidade.

    **Nada é salvo. Tudo é apagado ao sair.**

    ---
    💡 *Projeto sem fins lucrativos, feito com cuidado.*

    📩 **contato@projetodavar.com**
    """)

# CLIENTE OPENAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🤖 Davar – escuta com presença")

st.markdown("""
> Aqui você encontra uma escuta com presença, sem julgamentos. 
> Um espaço para respirar, pensar, sentir e recomeçar.
> 
> 🔐 Nada é salvo. Ao fechar esta aba, tudo é apagado.
""")

# HISTÓRICO
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if st.button("🧹 Nova conversa"):
    st.session_state["chat_history"] = []
    st.experimental_rerun()

# GRAVAÇÃO DE ÁUDIO
with st.expander("🎤 Gravar sua voz (opcional)"):
    class AudioRecorder(AudioProcessorBase):
        def __init__(self):
            self.frames = []

        def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
            audio = frame.to_ndarray()
            self.frames.append(audio)
            return frame

    ctx = webrtc_streamer(
        key="audio-recorder",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=256,
        audio_processor_factory=AudioRecorder,
        async_processing=True,
    )

    if ctx and ctx.audio_processor:
        st.write("Frames capturados:", len(ctx.audio_processor.frames))
        if st.button("🔴 Salvar gravação"):
            frames = ctx.audio_processor.frames
            if frames:
                try:
                    audio = np.concatenate([frame.flatten() for frame in frames])
                    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                    write(temp_wav.name, 48000, audio.astype(np.int16))
                    st.success("✅ Áudio salvo com sucesso!")
                    st.audio(temp_wav.name, format='audio/wav')
                    st.session_state['audio_file'] = temp_wav.name
                except Exception as e:
                    st.error(f"Erro ao processar áudio: {e}")
            else:
                st.warning("Nenhum áudio capturado.")

# TRANSCRIÇÃO DO ÁUDIO
if 'audio_file' in st.session_state:
    with st.spinner("🎧 Transcrevendo sua gravação..."):
        with open(st.session_state['audio_file'], "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="pt"
            )
        user_input = transcript.text
        st.markdown(f"**Você disse:** {user_input}")
        st.session_state["chat_history"].append({"role": "user", "content": user_input})

# ENTRADA DE TEXTO
with st.form("formulario_davar", clear_on_submit=True):
    user_input = st.text_area("✍️ Escreva aqui sua pergunta, desabafo ou reflexão:", height=200)
    enviar = st.form_submit_button("Enviar")

if enviar and user_input:
    st.session_state["chat_history"].append({"role": "user", "content": user_input})

# RESPOSTA DO DAVAR
if st.session_state["chat_history"] and st.session_state["chat_history"][-1]["role"] == "user":
    resposta = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é o Davar, uma presença de escuta e cuidado. Responda com empatia, sem pressa, acolhendo com humanidade."}
        ] + st.session_state["chat_history"],
        temperature=0.7
    )
    texto = resposta.choices[0].message.content.strip()
    st.session_state["chat_history"].append({"role": "assistant", "content": texto})

# EXIBIR HISTÓRICO
for msg in reversed(st.session_state["chat_history"]):
    if msg["role"] == "user":
        st.markdown(f"**Você:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**Davar:** {msg['content']}")
