import streamlit as st
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

# ESTADOS INICIAIS
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""
if "input_processed" not in st.session_state:
    st.session_state.input_processed = False

# BOTÃO NOVA CONVERSA
if st.button("🧹 Nova conversa"):
    st.session_state.chat_history = []
    st.experimental_rerun()

# MICROFONE NO NAVEGADOR (HTML/JS)
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
user_input = ""

if audio_file:
    with st.spinner("🎧 Transcrevendo áudio..."):
        audio_bytes = audio_file.read()
        audio_buffer = io.BytesIO(audio_bytes)
        audio_buffer.name = audio_file.name

        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_buffer,
            language="pt"  # ✅ Força transcrição em português
        )
        user_input = transcript.text
        st.markdown(f"**Você disse (transcrito):** {user_input}")
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        resposta = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é o Davar, uma presença de escuta e cuidado. "
                 "Responda com empatia, sem pressa, valorizando o que é dito e acolhendo a pessoa como ela é. "
                 "Use uma linguagem próxima, com humanidade e sensibilidade. "
                 "Você pode fazer pequenas pausas poéticas ou reflexivas, se for apropriado. "
                 "Evite parecer um robô ou um terapeuta técnico. "
                 "Seu papel é escutar, refletir e estar junto com palavras que tocam e inspiram."}
            ] + st.session_state.chat_history,
            temperature=0.7
        )
        resposta_texto = resposta.choices[0].message.content.strip()
        st.session_state.chat_history.append({"role": "assistant", "content": resposta_texto})

# ENTRADA DE TEXTO
user_input = st.text_input("✍️ Escreva aqui sua pergunta, desabafo ou reflexão:", key="user_input")

# PROCESSAMENTO DO TEXTO COM LIMPEZA SEGURA
if user_input and not st.session_state.input_processed:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é o Davar, uma presença de escuta e cuidado. "
             "Responda com empatia, sem pressa, valorizando o que é dito e acolhendo a pessoa como ela é. "
             "Use uma linguagem próxima, com humanidade e sensibilidade. "
             "Você pode fazer pequenas pausas poéticas ou reflexivas, se for apropriado. "
             "Evite parecer um robô ou um terapeuta técnico. "
             "Seu papel é escutar, refletir e estar junto com palavras que tocam e inspiram."}
        ] + st.session_state.chat_history,
        temperature=0.7
    )
    resposta = response.choices[0].message.content.strip()
    st.session_state.chat_history.append({"role": "assistant", "content": resposta})

    st.session_state["user_input"] = ""  # ✅ limpa o campo de forma segura
    st.session_state.input_processed = True
    st.experimental_rerun()
else:
    st.session_state.input_processed = False

# HISTÓRICO EM ORDEM DECRESCENTE
for mensagem in reversed(st.session_state.chat_history):
    if mensagem["role"] == "user":
        st.markdown(f"**Você:** {mensagem['content']}")
    elif mensagem["role"] == "assistant":
        st.markdown(f"**Davar:** {mensagem['content']}")
