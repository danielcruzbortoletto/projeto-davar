import streamlit as st
import openai

st.set_page_config(page_title="🕊️ Projeto Davar – Escuta Viva", layout="centered")

st.title("🕊️ Projeto Davar – Escuta Viva")
st.markdown("Digite sua reflexão, pergunta ou pensamento. Davar responderá com escuta, cuidado e profundidade.")

# Chave da API
api_key = st.secrets.get("OPENAI_API_KEY") or st.text_input("Digite sua OpenAI API Key", type="password")

# Inicializa sessão
if "historico" not in st.session_state:
    st.session_state.historico = []  # armazena múltiplas mensagens
if "resposta" not in st.session_state:
    st.session_state.resposta = ""
if "entrada_temp" not in st.session_state:
    st.session_state.entrada_temp = ""

# Função de conversa com histórico
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

# Formulário
with st.form("form_davar"):
    entrada = st.text_area("Você deseja conversar sobre o quê?", key="entrada_temp")
    enviar = st.form_submit_button("Enviar")

# Processa envio
if enviar and api_key:
    try:
        st.session_state.historico.append({"role": "user", "content": entrada})
        resposta = conversar_com_davar(st.session_state.historico)
        st.session_state.historico.append({"role": "assistant", "content": resposta})
        st.session_state.resposta = resposta
        st.session_state.entrada_temp = ""  # limpa campo

    except openai.AuthenticationError:
        st.error("API Key inválida. Verifique e tente novamente.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

# Exibe resposta
if st.session_state.resposta:
    st.markdown("**Resposta do Davar:**")
    st.write(st.session_state.resposta)
