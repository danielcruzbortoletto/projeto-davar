import streamlit as st
import openai
import os

st.set_page_config(page_title="🕊️ Projeto Davar – Escuta Viva", layout="centered")

st.title("🕊️ Projeto Davar – Escuta Viva")
st.markdown("Digite sua reflexão, pergunta ou pensamento. Davar responderá com escuta, cuidado e profundidade.")

# Campo para digitar a chave da API (deixe em branco no deploy na nuvem)
api_key = st.secrets["api_key"] if "api_key" in st.secrets else st.text_input("Digite sua OpenAI API Key", type="password")

# Interface
with st.form("form_davar"):
    entrada = st.text_area("Você deseja conversar sobre o quê?", key="entrada_texto")
    enviar = st.form_submit_button("Enviar")

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

# Execução
if enviar and api_key:
    try:
        resposta = conversar_com_davar(entrada)
        st.markdown("**Resposta do Davar:**")
        st.write(resposta)

        # 🧠 Aqui limpamos o campo de entrada após o envio
        st.session_state["entrada_texto"] = ""

    except openai.AuthenticationError:
        st.error("API Key inválida. Verifique e tente novamente.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
