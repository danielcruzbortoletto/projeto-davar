import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
import io

# Carrega variáveis do .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Configura página
st.set_page_config(page_title="Davar – escuta com presença", layout="centered")

# Estilo visual topo
st.markdown("""
    <style>
        .image-container {
            text-align: center;
            margin-bottom: 24px;
        }
        .image-container img {
            border-radius: 16px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            animation: fadeIn 1.2s ease-in-out;
            max-width: 900px;
            width: 100%;
        }
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(-20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
    </style>
""", unsafe_allow_html=True)

# Topo com imagem (certifique-se que 'topo.png' está no diretório)
st.markdown('<div class="image-container">', unsafe_allow_html=True)
st.image("topo.png", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Título
st.title("🧠 Davar: escuta com presença")
st.markdown("#### 📝 Escreva algo (ou envie um áudio abaixo):")

# Estado inicial do histórico
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Entrada de texto
user_input = st.text_area("Como você está hoje?", placeholder="Escreva aqui com calma...")

# Upload de áudio
st.markdown("#### 📢 Ou envie um áudio")
audio_file = st.file_uploader("Drag and drop file here", type=["mp3", "wav", "m4a", "ogg"])

# Geração de resposta
if st.button("Enviar"):
    if not user_input and not audio_file:
        st.warning("Por favor, escreva algo ou envie um áudio.")
    else:
        with st.spinner("Gerando resposta do Davar..."):

            if audio_file:
                audio_bytes = audio_file.read()
                audio_buffer = io.BytesIO(audio_bytes)
                audio_buffer.name = audio_file.name

                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_buffer,
                    language="pt"
                )
                user_input = transcript.text
                st.markdown(f"**Você disse (transcrito):** {user_input}")

            # Salva input no histórico
            st.session_state["chat_history"].append({"role": "user", "content": user_input})

            # Gera resposta
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Você é o Davar, uma presença de escuta e cuidado. "
                     "Responda com empatia, sem pressa, acolhendo com palavras sensíveis, poéticas e humanas. "
                     "Não use tom robótico ou técnico. Seu papel é escutar com presença."}
                ] + st.session_state["chat_history"],
                temperature=0.7
            )
            resposta = response.choices[0].message.content.strip()
            st.session_state["chat_history"].append({"role": "assistant", "content": resposta})

# Histórico de conversa
for mensagem in reversed(st.session_state["chat_history"]):
    if mensagem["role"] == "user":
        st.markdown(f"**Você:** {mensagem['content']}")
    elif mensagem["role"] == "assistant":
        st.markdown(f"**Davar:** {mensagem['content']}")

# Rodapé
st.markdown("""
<hr style="margin-top: 3rem; margin-bottom: 1rem;">

<div style="text-align: center; font-size: 0.9rem; color: gray;">
    Davar é um projeto independente, feito com escuta, ética e cuidado.<br>
    📩 <a href="mailto:contato@projetodavar.com">contato@projetodavar.com</a>
</div>
""", unsafe_allow_html=True)
