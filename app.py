import streamlit as st
import openai
import tempfile
import os

st.set_page_config(page_title="🕊️ Projeto Davar – Escuta Viva", layout="centered")

st.title("🕊️ Projeto Davar – Escuta Viva")
st.markdown("Digite ou envie sua reflexão. Davar responderá com escuta, cuidado e profundidade.")
st.markdown("🔒 Todas as conversas são privadas e não são armazenadas. Use com liberdade e respeito.")

# API Key
api_key = st.secrets.get("OPENAI_API_KEY") or st.text_input("Digite sua OpenAI API Key", type="password")

# Inicializa estados
if "historico" not in st.session_state:
    st.session_state.historico = []
if "resposta" not in st.session_state:
    st.session_state.resposta = ""

# Função para conversar com o Davar
def conversar_com_davar(mensagem):
    client = openai.OpenAI(api_key=api_key)

    mensagens = [
        {"role": "system", "content": "Você é Davar, uma presença atenta, cuidadosa e ética. Sua linguagem é humana, profunda e inspiradora."},
    ] + st.session_state.historico + [
        {"role": "user", "content": mensagem}
    ]

    resposta = client.chat.completions.create(
        model="gpt-4o",
        messages=mensagens,
        temperature=0.7
    )
    return resposta.choices[0].message.content.strip()

# Função para transcrição de áudio (caso enviada)
def transcrever_audio(arquivo):
    client = openai.OpenAI(api_key=api_key)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(arquivo.read())
        tmp_path = tmp.name
    with open(tmp_path, "rb") as f:
        transcript = client.audio.transcriptions.create(model="whisper-1", file=f)
    os.remove(tmp_path)
    return transcript.text

# Formulário
with st.form("form_davar"):
    entrada_texto = st.text_area("Digite aqui sua pergunta, reflexão ou pensamento:", placeholder="Ex: Sinto que estou em transição, mas não sei para onde...", height=150)
    arquivo_audio = st.file_uploader("Ou envie sua voz (MP3 ou WAV)", type=["mp3", "wav"])
    enviar = st.form_submit_button("Enviar")

if enviar:
    if not api_key:
        st.error("API Key não informada.")
    elif not entrada_texto.strip():
        st.warning("Por favor, escreva sua pergunta ou reflexão.")
    else:
        mensagem_completa = entrada_texto.strip()

        # Tenta transcrever se houver áudio
        if arquivo_audio:
            try:
                texto_audio = transcrever_audio(arquivo_audio)
                mensagem_completa += f"\n\n[Transcrição complementar da voz enviada: {texto_audio}]"
            except Exception as e:
                st.warning(f"Erro ao transcrever o áudio. Continuando apenas com o texto. Erro: {e}")

        resposta = conversar_com_davar(mensagem_completa)
        st.session_state.historico.append({"role": "user", "content": mensagem_completa})
        st.session_state.historico.append({"role": "assistant", "content": resposta})
        st.session_state.resposta = resposta

# Exibe resposta
if st.session_state.resposta:
    st.markdown("**Resposta do Davar:**")
    st.write(st.session_state.resposta)

