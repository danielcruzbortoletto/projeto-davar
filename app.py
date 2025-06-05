import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
import io
import numpy as np
import wave
import tempfile
import av
import soundfile as sf  # ✅ Substituto compatível com Streamlit Cloud
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
import streamlit.components.v1 as components

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Projeto Davar", layout="centered")

# SIDEBAR COM ORIENTAÇÕES
with st.sidebar:
    st.header("💬 Sobre o Davar")
    st.markdown("""
    O **Davar** é um espaço de escuta com presença.

    Aqui, você pode escrever ou falar livremente — sem julgamentos, sem pressa.

    **Como usar:**
    - Grave ou escreva sua pergunta, desabafo ou reflexão.
    - O Davar responde com empatia e sensibilidade.
    - Nenhuma conversa é salva. Tudo é apagado ao sair.

    ---
    💡 *Projeto sem fins lucrativos, feito com propósito e cuidado.*

    📩 **Contato:** [contato@projetodavar.com](mailto:contato@projetodavar.com)
    """)

# IMAGEM DO TOPO
st.image("topo.png", use_container_width=True)

# CLIENTE OPENAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🤖 Davar – escuta com presença")

st.markdown("""
> **🌱 Bem-vindo ao Davar**  
> Aqui, você encontra uma escuta com presença, sem julgamentos.  
> Um espaço para respirar, pensar, sentir e recomeçar.

> 🔒 Nenhuma conversa é salva. Ao fechar esta aba, tudo é apagado.
""")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if st.button("🧹 Nova conversa"):
    st.session_state["chat_history"] = []
    st.experimental_rerun()

# GRAVACAO DE AUDIO
with st.expander("🎤 Gravar direto do navegador (opcional)"):
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
        st.write("🎹 Frames capturados:", len(ctx.audio_processor.frames))
        if st.button("🔴 Salvar gravação"):
            frames = ctx.audio_processor.frames
            if frames:
                try:
                    audio = np.concatenate([frame.flatten() for frame in frames])
                    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")

                    # ✅ Salva com soundfile
                    sf.write(temp_wav.name, audio, 48000, subtype='PCM_16')

                    st.success("✅ Áudio salvo com sucesso!")
                    st.audio(temp_wav.name, format='audio/wav')
                    st.session_state['audio_file'] = temp_wav.name
                except Exception as e:
                    st.error(f"Erro ao processar áudio: {e}")
            else:
                st.warning("Nenhum áudio capturado.")

# TRANSCRIÇÃO DO ÁUDIO GRAVADO
if 'audio_file' in st.session_state:
    with st.spinner("🎧 Transcrevendo sua gravação..."):
        with open(st.session_state['audio_file'], "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="pt"
            )
        user_input = transcript.text
        st.markdown(f"**Você disse (transcrito):** {user_input}")
        st.session_state["chat_history"].append({"role": "user", "content": user_input})

        resposta = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é o Davar, uma presença de escuta e cuidado. Responda com empatia, sem pressa, valorizando o que é dito e acolhendo a pessoa como ela é. Use uma linguagem próxima, com humanidade e sensibilidade."}
            ] + st.session_state["chat_history"],
            temperature=0.7
        )
        resposta_texto = resposta.choices[0].message.content.strip()
        st.session_state["chat_history"].append({"role": "assistant", "content": resposta_texto})
        del st.session_state["audio_file"]

# FORMULÁRIO DE ENTRADA DE TEXTO
with st.form("formulario_davar", clear_on_submit=True):
    user_input = st.text_area("✍️ Escreva aqui sua pergunta, desabafo ou reflexão:", height=200)
    enviar = st.form_submit_button("Enviar")

if enviar and user_input:
    st.session_state["chat_history"].append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é o Davar, uma presença de escuta e cuidado. Responda com empatia, sem pressa, valorizando o que é dito e acolhendo a pessoa como ela é. Use uma linguagem próxima, com humanidade e sensibilidade."}
        ] + st.session_state["chat_history"],
        temperature=0.7
    )
    resposta = response.choices[0].message.content.strip()
    st.session_state["chat_history"].append({"role": "assistant", "content": resposta})

# HISTÓRICO
for mensagem in reversed(st.session_state["chat_history"]):
    if mensagem["role"] == "user":
        st.markdown(f"**Você:** {mensagem['content']}")
    elif mensagem["role"] == "assistant":
        st.markdown(f"**Davar:** {mensagem['content']}")

# RODAPÉ
st.markdown("""
<hr style="margin-top: 3rem; margin-bottom: 1rem;">
<div style="text-align: center; font-size: 0.9rem; color: gray;">
    Davar é um projeto independente, feito com escuta, ética e cuidado.<br>
    📩 <a href="mailto:contato@projetodavar.com">contato@projetodavar.com</a>
</div>
""", unsafe_allow_html=True)
