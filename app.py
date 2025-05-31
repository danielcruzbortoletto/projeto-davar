import streamlit as st
import openai
import os
from io import BytesIO
import base64

# Configuração da página
st.set_page_config(page_title="🕊️ Projeto Davar – Escuta Viva", layout="centered")

st.title("🕊️ Projeto Davar – Escuta Viva")
st.markdown("Digite ou envie sua reflexão. Davar responderá com escuta, cuidado e profundidade.")
st.markdown("🔒 Todas as conversas são privadas e não são armazenadas. Use com liberdade e respeito.")

# Chave da API
api_key = st.secrets.get("OPENAI_API_KEY") or st.text_input("Digite sua OpenAI API Key", type="password")

# Inicializa estados
if "historico" not in st.session_state:
    st.session_state.historico = []
if "resposta" not in st.session_state:
    st.session_state.resposta = ""
if "contador_respostas" not in st.session_state:
    st.session_state.contador_respostas = 0
if "mostrar_estatisticas" not in st.session_state:
    st.session_state.mostrar_estatisticas = False

# Limpa campo de entrada após envio
if "limpar_input" in st.session_state:
    st.session_state.entrada_temp = ""
    del st.session_state["limpar_input"]

# Função principal de conversa
def conversar_com_davar(historico):
    client = openai.OpenAI(api_key=api_key)

    mensagens = [{"role": "system", "content":
        "Você é Davar, uma presença atenta, cuidadosa e ética. Sua linguagem é humana, profunda e inspiradora."}] + historico

    resposta = client.chat.completions.create(
        model="gpt-4o",
        messages=mensagens,
        temperature=0.7
    )
    return resposta.choices[0].message.content.strip()

# Interface principal
with st.form("form_davar"):
    entrada = st.text_area("Digite aqui sua pergunta, reflexão ou pensamento:", key="entrada_temp")
    audio_file = st.file_uploader("Ou envie sua voz (MP3 ou WAV)", type=["mp3", "wav"])
    enviar = st.form_submit_button("Enviar")

# Processa envio
if enviar and api_key:
    try:
        if entrada.strip():
            st.session_state.historico.append({"role": "user", "content": entrada})
        elif audio_file:
            audio_bytes = audio_file.read()
            audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
            audio_prompt = f"[Áudio recebido: {audio_file.name}]"
            st.session_state.historico.append({"role": "user", "content": audio_prompt})
        else:
            st.warning("Por favor, digite uma pergunta ou envie um áudio.")
            st.stop()

        resposta = conversar_com_davar(st.session_state.historico)
        st.session_state.historico.append({"role": "assistant", "content": resposta})
        st.session_state.resposta = resposta
        st.session_state.contador_respostas += 1
        st.session_state.limpar_input = True
        st.rerun()

    except openai.AuthenticationError:
        st.error("API Key inválida. Verifique e tente novamente.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

# Exibe resposta
if st.session_state.resposta:
    st.markdown("**Resposta do Davar:**")
    st.write(st.session_state.resposta)

# Exibe histórico da sessão
if st.session_state.historico:
    st.markdown("---")
    st.markdown("### Histórico desta sessão:")
    for i in range(0, len(st.session_state.historico), 2):
        user_msg = st.session_state.historico[i]["content"]
        st.markdown(f"**Você:** {user_msg}")
        if i + 1 < len(st.session_state.historico):
            davar_msg = st.session_state.historico[i + 1]["content"]
            st.markdown(f"**Davar:** {davar_msg}")

# Botão para exibir estatísticas
with st.expander("📊 Ver estatísticas do Davar"):
    st.write(f"Total de respostas geradas nesta sessão: {st.session_state.contador_respostas}")
