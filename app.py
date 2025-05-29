import streamlit as st
import openai
import os

st.set_page_config(page_title="🕊️ Projeto Davar – Escuta Viva", layout="centered")

st.title("🕊️ Projeto Davar – Escuta Viva")
st.markdown("Digite sua reflexão, pergunta ou pensamento. Davar responderá com escuta, cuidado e profundidade.")

# Inicializa estado se não existir
if "resposta" not in st.session_state:
    st.session_state["resposta"] = ""
if "entrada_texto" not in st.session_state:
    st.session_state["entrada_texto"] = ""

# Campo para digitar a chave da API (em produção deixe como st.secrets["api_key"])
api_key = st.secrets["api_key"] if "api_key" in st.secrets else st.text_input("Digite sua OpenAI API Key", type="password")

# Função principal
def conversar_com_davar(mensagem):
    client = openai.OpenAI(api_key=api_key)
    mensagens = [
        {"role": "system", "content": "Você é Davar, uma presença atenta, cuidadosa e ética. Sua linguagem é humana, profunda e inspiradora."},
        {"role": "user", "content": mensagem}
    ]
    resposta = client.chat.completions.create(
        model="gpt-4o",
        messages=mensagens,
        temperature=0.7
    )
    return resposta.choices[0].message.content.strip()

# Interface
with st.form("form_davar"):
    entrada = st.text_area("Você deseja conversar sobre o quê?", value=st.session_state["entrada_texto"], key="entrada_texto_area")
    enviar = st.form_submit_button("Enviar")

# Execução
if enviar and api_key:
    try:
        st.session_state["resposta"] = conversar_com_davar(entrada)
        st.session_state["entrada_texto"] = ""  # reseta o estado para a próxima vez

    except openai.AuthenticationError:
        st.error("API Key inválida. Verifique e tente novamente.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

# Mostra resposta (mesmo fora do bloco do form)
if st.session_state["resposta"]:
    st.markdown("**Resposta do Davar:**")
    st.write(st.session_state["resposta"])
