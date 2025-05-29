import streamlit as st
import openai
import os

st.set_page_config(page_title="🕊️ Projeto Davar – Escuta Viva", layout="centered")

st.title("🕊️ Projeto Davar – Escuta Viva")
st.markdown("Digite sua reflexão, pergunta ou pensamento. Davar responderá com escuta, cuidado e profundidade.")

# Chave da API
api_key = st.secrets.get("OPENAI_API_KEY") or st.text_input("Digite sua OpenAI API Key", type="password")

# Inicializa o campo no session_state se ainda não existir
if "entrada_texto" not in st.session_state:
    st.session_state["entrada_texto"] = ""

# Função para conversar com Davar
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

# Interface do formulário
with st.form("form_davar"):
    entrada = st.text_area("Você deseja conversar sobre o quê?", value=st.session_state["entrada_texto"], key="entrada_texto")
    enviar = st.form_submit_button("Enviar")

# Execução após envio
if enviar and api_key:
    try:
        resposta = conversar_com_davar(st.session_state["entrada_texto"])
        st.markdown("**Resposta do Davar:**")
        st.write(resposta)

        # Limpa o campo na próxima execução
        st.session_state["entrada_texto"] = ""
        st.experimental_rerun()  # força rerenderização

    except openai.AuthenticationError:
        st.error("API Key inválida. Verifique e tente novamente.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
