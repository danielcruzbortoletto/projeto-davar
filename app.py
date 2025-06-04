import streamlit as st

# ⚠️ Esta linha deve ser o primeiro comando do Streamlit
st.set_page_config(page_title="Projeto Davar", layout="centered")

# Depois, todo o resto do código:
st.markdown("""
    <style>
        .top-image {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
            max-width: 900px;
            border-radius: 16px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            animation: fadeIn 1.2s ease-in-out;
            margin-bottom: 24px;
        }

        @keyframes fadeIn {
            0%   { opacity: 0; transform: translateY(-20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    '<img src="topo.png" class="top-image">',
    unsafe_allow_html=True
)


from openai import OpenAI
import os
import io
import streamlit.components.v1 as components

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Projeto Davar", layout="centered")
st.title("🤖 Davar – escuta com presença")

# MANIFESTO
st.markdown("""
> **🌱 Bem-vindo ao Davar**  
> Aqui, você encontra uma escuta com presença, sem julgamentos.  
> Um espaço para respirar, pensar, sentir e recomeçar.

> 🔒 Nenhuma conversa é salva. Ao fechar esta aba, tudo é apagado.
""")

# ESTADO INICIAL
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# BOTÃO PARA NOVA CONVERSA
if st.button("🧹 Nova conversa"):
    st.session_state["chat_history"] = []
    st.experimental_rerun()

# GRAVAÇÃO NO NAVEGADOR
with st.expander("🎤 Gravar direto do navegador (opcional)"):
    components.html(
        """
        <html>
        <body>
            <p><strong>1. Clique em "Gravar" e fale.</strong></p>
            <p><strong>2. Depois clique em "Parar" e baixe o áudio para enviar abaixo.</strong></p>
            <button onclick="startRecording()">🎙️ Gravar</button>
            <button onclick="stopRecording()">⏹️ Parar</button>
            <p id="status">Pronto para gravar...</p>
            <script>
                let mediaRecorder;
                let audioChunks = [];

                function startRecording() {
                    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
                        mediaRecorder = new MediaRecorder(stream);
                        mediaRecorder.start();
                        audioChunks = [];
                        mediaRecorder.addEventListener("dataavailable", event => {
                            audioChunks.push(event.data);
                        });
                        document.getElementById("status").innerText = "🎙️ Gravando...";
                    });
                }

                function stopRecording() {
                    mediaRecorder.stop();
                    mediaRecorder.addEventListener("stop", () => {
                        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                        const audioUrl = URL.createObjectURL(audioBlob);
                        const a = document.createElement('a');
                        a.href = audioUrl;
                        a.download = 'gravacao_davar.wav';
                        a.click();
                        document.getElementById("status").innerText = "✅ Áudio salvo! Faça o upload abaixo.";
                    });
                }
            </script>
        </body>
        </html>
        """,
        height=300
    )

# UPLOAD DE ÁUDIO
audio_file = st.file_uploader("📁 Envie seu áudio (MP3, WAV, M4A):", type=["mp3", "wav", "m4a"])
if audio_file:
    with st.spinner("🎧 Transcrevendo áudio..."):
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
        st.session_state["chat_history"].append({"role": "user", "content": user_input})

        resposta = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é o Davar, uma presença de escuta e cuidado. "
                 "Responda com empatia, sem pressa, valorizando o que é dito e acolhendo a pessoa como ela é. "
                 "Use uma linguagem próxima, com humanidade e sensibilidade. "
                 "Você pode fazer pequenas pausas poéticas ou reflexivas, se for apropriado. "
                 "Evite parecer um robô ou um terapeuta técnico. "
                 "Seu papel é escutar, refletir e estar junto com palavras que tocam e inspiram."}
            ] + st.session_state["chat_history"],
            temperature=0.7
        )
        resposta_texto = resposta.choices[0].message.content.strip()
        st.session_state["chat_history"].append({"role": "assistant", "content": resposta_texto})

# FORMULÁRIO DE ENTRADA DE TEXTO
with st.form("formulario_davar", clear_on_submit=True):
    user_input = st.text_input("✍️ Escreva aqui sua pergunta, desabafo ou reflexão:")
    enviar = st.form_submit_button("Enviar")

if enviar and user_input:
    st.session_state["chat_history"].append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é o Davar, uma presença de escuta e cuidado. "
             "Responda com empatia, sem pressa, valorizando o que é dito e acolhendo a pessoa como ela é. "
             "Use uma linguagem próxima, com humanidade e sensibilidade. "
             "Você pode fazer pequenas pausas poéticas ou reflexivas, se for apropriado. "
             "Evite parecer um robô ou um terapeuta técnico. "
             "Seu papel é escutar, refletir e estar junto com palavras que tocam e inspiram."}
        ] + st.session_state["chat_history"],
        temperature=0.7
    )
    resposta = response.choices[0].message.content.strip()
    st.session_state["chat_history"].append({"role": "assistant", "content": resposta})

# HISTÓRICO EM ORDEM DECRESCENTE
for mensagem in reversed(st.session_state["chat_history"]):
    if mensagem["role"] == "user":
        st.markdown(f"**Você:** {mensagem['content']}")
    elif mensagem["role"] == "assistant":
        st.markdown(f"**Davar:** {mensagem['content']}")
