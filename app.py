import streamlit as st
import openai
from typing import List

# Configuração da página
st.set_page_config(page_title="🕊️ Projeto Davar – Escuta Viva", layout="centered")

# Título e descrição
st.title("🕊️ Projeto Davar – Escuta Viva")
st.markdown("Digite ou envie sua reflexão. Davar responderá com escuta, cuidado e profundidade.")
st.markdown("🔒 Todas as conversas são privadas e não são armazenadas. Use com liberdade e respeito.")

# Chave da API
api_key = st.secrets.get("OPENAI_API_KEY") or st.text_input("Digite sua OpenAI API Key", type="password")

# Inicialização do estado da sessão
if "historico" not in st.session_state:
    st.session_state.historico = []
if "resposta" not in st.session_state:
    st.session_state.resposta = ""
if "entrada_temp" not in st.session_state:
    st.session_state.entrada_temp = ""
if "contador" not in st.session_state:
    st.session_state.contador = 0

# Função de conversa com Davar
def conversar_com_davar(historico: List[dict]) -> str:
    client = openai.OpenAI(api_key=api_key)
    mensagens = [{"role": "system", "content":
                  "Você é Davar, uma presença ética, atenta, sensível e profunda. Responda com linguagem humana e acolhedora."}] + historico

    resposta = client.chat.completions.create(
        model="gpt-4o",
        messages=mensagens,
        temperature=0.7
    )
    return resposta.choices[0].message.content.strip()

# Formulário principal
with st.form("form_davar"):
    entrada = st.text_area("Digite aqui sua pergunta, reflexão ou pensamento:", key="entrada_temp")
    audio = st.file_uploader("Ou envie sua voz (MP3 ou WAV)", type=["mp3", "wav"])
    enviar = st.form_submit_button("Enviar")

# Processamento da entrada
if enviar and api_key:
    if audio:
        st.warning("Reconhecimento de voz ainda não está ativado. Por enquanto, envie texto manualmente.")
    if st.session_state.entrada_temp.strip():
        entrada = st.session_state.entrada_temp.strip()
        st.session_state.historico.append({"role": "user", "content": entrada})
        try:
            resposta = conversar_com_davar(st.session_state.historico)
            st.session_state.historico.append({"role": "assistant", "content": resposta})
            st.session_state.resposta = resposta
            st.session_state.contador += 1
            st.session_state.update({"entrada_temp": ""})  # limpa entrada com segurança
        except openai.AuthenticationError:
            st.error("API Key inválida. Verifique e tente novamente.")
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")

# Exibe resposta atual
if st.session_state.resposta:
    st.markdown("**Resposta do Davar:**")
    st.write(st.session_state.resposta)

# Histórico da sessão
if st.session_state.historico:
    st.markdown("---")
    st.markdown("### Histórico desta sessão:")
    for i, item in enumerate(st.session_state.historico):
        if item["role"] == "user":
            st.markdown(f"**Você:** {item['content']}")
        elif item["role"] == "assistant":
            st.markdown(f"**Davar:** {item['content']}")

# Estatísticas ocultas
with st.expander("📊 Ver estatísticas do Davar"):
    st.write(f"Total de respostas geradas nesta sessão: {st.session_state.contador}")
