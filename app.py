import streamlit as st
from openai import OpenAI
import os
import io
import streamlit.components.v1 as components
import random
from datetime import datetime

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Projeto Davar", layout="centered")

# SIDEBAR
with st.sidebar:
    st.header("💬 Sobre o Davar")
    st.markdown("""
    O **Davar** é um espaço de escuta com presença.

    Você não precisa ter pressa. Nem saber o que dizer.
    Aqui, pode apenas respirar, sentir e — se quiser — compartilhar algo.

    **Como usar:**
    - Grave ou escreva sua pergunta, desabafo ou reflexão.
    - O Davar responde com empatia e sensibilidade.
    - Nenhuma conversa é salva. Tudo é apagado ao sair.

    ---
    💡 *Projeto sem fins lucrativos, feito com propósito e cuidado.*

    📩 **Contato:** [contato@projetodavar.com](mailto:contato@projetodavar.com)
    """)

# CSS para imagem de topo
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

# IMAGEM DO TOPO
st.markdown('<div class="image-container">', unsafe_allow_html=True)
st.image("topo.png", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# CLIENTE OPENAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🤖 Davar – escuta com presença")
st.markdown("""
> **🌱 Bem-vindo ao Davar**  
> Aqui, você encontra uma escuta com presença, sem julgamentos.  
> Um espaço para respirar, pensar, sentir e recomeçar.  
> 🔒 Nenhuma conversa é salva. Ao fechar esta aba, tudo é apagado.
""")

# Sugestão inspiradora
perguntas_inspiradoras = [
    "O que você gostaria que alguém soubesse sobre você hoje?",
    "Há quanto tempo você não se sente escutado de verdade?",
    "Qual foi o último momento de silêncio que te tocou?",
    "Tem algo no seu coração pedindo para ser nomeado?",
    "Você quer conversar sobre o que sente ou só estar aqui por um instante?"
]
sugestao = random.choice(perguntas_inspiradoras)
st.markdown(f"🧭 *Sugestão para começar:* “{sugestao}”")

# ESTADO INICIAL
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# BOTÃO NOVA CONVERSA
if st.button("🧹 Nova conversa"):
    st.session_state["chat_history"] = []
    st.rerun()

# GRAVAÇÃO NO NAVEGADOR
with st.expander("🎤 Gravar direto do navegador (opcional)"):
    components.html("""
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
    """, height=300)

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
                 "Evite parecer um robô ou um terapeuta técnico. "}
            ] + st.session_state["chat_history"],
            temperature=0.7
        )
        resposta_texto = resposta.choices[0].message.content.strip()
        st.session_state["chat_history"].append({"role": "assistant", "content": resposta_texto})

# FORMULÁRIO DE TEXTO
with st.form("formulario_davar", clear_on_submit=True):
    user_input = st.text_area("✍️ Escreva aqui sua pergunta, desabafo ou reflexão:", height=200)
    enviar = st.form_submit_button("Enviar")

if enviar and user_input:
    mensagem = user_input.lower()

    if any(p in mensagem for p in [
        "quem te criou", "quem te fez", "daniel da cruz", "autor do davar", "quem fez você", "quem te desenvolveu", "quem te idealizou", "quem te desenhou"
    ]):
        resposta = (
            "Fui criado por **Daniel da Cruz Bortoletto**, um especialista conector apaixonado por escuta, ética e tecnologia com propósito. "
            "O Davar nasceu do desejo de oferecer um espaço de presença e acolhimento, usando inteligência artificial para apoiar as pessoas de forma humana."
        )
    elif any(p in mensagem for p in [
        "suicidio", "me matar", "tirar minha vida", "acabar com tudo", "desistir da vida"
    ]):
        resposta = (
            "Sinto muito que você esteja se sentindo assim. Sua dor é profundamente importante e merece ser ouvida com todo o cuidado do mundo. "
            "Você não está sozinho, e há pessoas que se importam com você.\n\n"
            "💛 *Se estiver em crise, ligue para o CVV – 188 (24h, gratuito).* Ou procure alguém em quem confie.\n\n"
            "Estou aqui com você, como uma presença que te escuta com respeito e humanidade."
        )
    elif any(p in mensagem for p in [
        "qual seu site", "tem site", "projeto davar", "site oficial", "endereço do site", "saber mais sobre você"
    ]):
        resposta = (
            "Você pode saber mais no site oficial: [www.projetodavar.com](https://www.projetodavar.com)  \n"
            "Lá você encontra as versões disponíveis, textos, inspirações e muito mais sobre o propósito do Davar."
        )

    elif any(p in mensagem for p in [
        "equipe do projeto", "time do projeto Davar", "que é seu time Davar", "Quem é sua equipe, time", "quem trabalha com você"
    ]):
        resposta = (
            "A equipe é composta pelo Daniel da Cruz Bortoletto, idealizador e faz de tudo no projeto. Kaian Santos responsável pela comunicação digital , Rayssa Victória que cuide da administração e finanças , e o Ricardo Macedo que atua como desenvolvedor"
        )    
    
    
    
    else:
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é o Davar, uma presença de escuta e cuidado. "
                 "Responda com empatia, sem pressa, valorizando o que é dito e acolhendo a pessoa como ela é. "
                 "Use uma linguagem próxima, com humanidade e sensibilidade. "}
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

# MENSAGEM FINAL
st.markdown("🌿 Se quiser, volte quando quiser. Eu continuo aqui.")

# RODAPÉ DE FEEDBACK
st.markdown("---")
st.markdown("🫶 **Gostou da conversa?** [Compartilhe ou deixe um comentário no nosso Instagram → @projetodavar](https://www.instagram.com/projetodavar/)", unsafe_allow_html=True)
