import streamlit as st
import openai
import base64

# Título e descrição
st.set_page_config(page_title="🕊️ Projeto Davar – Escuta Viva", layout="centered")
st.title("🕊️ Projeto Davar – Escuta Viva")
st.markdown("Digite ou envie sua reflexão. Davar responderá com escuta, cuidado e profundidade.")
st.markdown("🔒 Todas as conversas são privadas e não são armazenadas. Use com liberdade e respeito.")

# Limpa flag de rerun logo no início
if "limpar_input" in st.session_state:
    st.session_state.pop("limpar_input")

# Inicializa variáveis de sessão
st.session_state.setdefault("historico", [])
st.session_state.setdefault("resposta", "")
st.session_state.setdefault("contador_respostas", 0)

# Chave da API
api_key = st.secrets.get("OPENAI_API_KEY") or st.text_input("Digite sua OpenAI API Key", type="password")

# Função de conversa
def conversar_com_davar(historico):
    client = openai.OpenAI(api_key=api_key)
    mensagens = [{"role": "system", "content": "Você é Davar, uma presença atenta, cuidadosa e ética. Sua linguagem é humana, profunda e inspiradora."}] + historico

    resposta = client.chat.completions.create(
        model="gpt-4o",
        messages=mensagens,
        temperature=0.7
    )
    return resposta.choices[0].message.content.strip()

# Formulário
with st.form("form_davar"):
    entrada = st.text_area("Digite aqui sua pergunta, reflexão ou pensamento:", key="entrada_temp")
    audio_file = st.file_uploader("Ou envie sua voz (MP3 ou WAV)", type=["mp3", "wav"])
    enviar = st.form_submit_button("Enviar")

# Processamento
if enviar and api_key:
    try:
        texto = entrada
        if audio_file:
            audio_bytes = audio_file.read()
            encoded = base64.b64encode(audio_bytes).decode("utf-8")
            audio_input = {
                "model": "whisper-1",
                "file": audio_bytes,
                "filename": audio_file.name
            }
            transcript = openai.Audio.transcriptions.create(model="whisper-1", file=audio_file)
            texto = transcript.text

        if texto.strip():
            st.session_state.historico.append({"role": "user", "content": texto})
            resposta = conversar_com_davar(st.session_state.historico)
            st.session_state.historico.append({"role": "assistant", "content": resposta})
            st.session_state.resposta = resposta
            st.session_state.contador_respostas += 1
            st.session_state.limpar_input = True
            st.rerun()

    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

# Exibição da resposta
if st.session_state.resposta:
    st.markdown("**Resposta do Davar:**")
    st.write(st.session_state.resposta)

# Histórico da sessão
if st.session_state.historico:
    st.markdown("### Histórico desta sessão:")
    for i in range(0, len(st.session_state.historico), 2):
        user = st.session_state.historico[i]["content"]
        st.markdown(f"**Você:** {user}")
        if i + 1 < len(st.session_state.historico):
            bot = st.session_state.historico[i + 1]["content"]
            st.markdown(f"**Davar:** {bot}")

# Estatísticas
with st.expander("📊 Ver estatísticas do Davar"):
    st.markdown(f"Total de respostas geradas nesta sessão: {st.session_state.contador_respostas}")
