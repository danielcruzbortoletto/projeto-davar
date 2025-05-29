import streamlit as st
import openai
import os

# Configuração da página
st.set_page_config(page_title="🕊️ Projeto Davar – Escuta Viva", layout="centered")

st.title("🕊️ Projeto Davar – Escuta Viva")
st.markdown("Digite sua reflexão, pergunta ou pensamento. Davar responderá com escuta, cuidado e profundidade.")

# Chave da API
api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else st.text_input("Digite sua OpenAI API Key", type="password")

# Interface com formulário
with st.form("form_davar"):
    entrada = st.text_area("Você deseja conversar sobre o quê?", key="entrada_texto")
    enviar = st.form_submit_button("Enviar")

# Função principal de conversa
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

# Execução ao enviar
if enviar and api_key:
    try:
        resposta = conversar_com_davar(entrada)
        st.session_state["ultima_resposta"] = resposta
        st.session_state["entrada_texto"] = ""
        st.rerun()

    except openai.AuthenticationError:
        st.error("API Key inválida. Verifique e tente novamente.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

# Exibe a última resposta
if "ultima_resposta" in st.session_state:
    st.markdown("**Resposta do Davar:**")
    st.write(st.session_state["ultima_resposta"])
