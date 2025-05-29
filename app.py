import streamlit as st
import openai
import os

st.set_page_config(page_title="🕊️ Projeto Davar – Escuta Viva", layout="centered")
st.title("🕊️ Projeto Davar – Escuta Viva")
st.markdown("Digite sua reflexão, pergunta ou pensamento. Davar responderá com escuta, cuidado e profundidade.")

# Ler chave da API de forma segura
api_key = st.secrets["OPENAI_API_KEY"]

# Inicializar histórico se necessário
if "resposta" not in st.session_state:
    st.session_state["resposta"] = ""

# Campo de entrada (sem alterar diretamente session_state)
with st.form("form_davar"):
    entrada = st.text_area("Você deseja conversar sobre o quê?")
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
if enviar and entrada.strip():
    try:
        resposta = conversar_com_davar(entrada)
        st.session_state["resposta"] = resposta

        # Forçar limpeza do campo com rerun
        st.experimental_rerun()

    except openai.AuthenticationError:
        st.error("API Key inválida. Verifique e tente novamente.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

# Mostrar resposta, se houver
if st.session_state["resposta"]:
    st.markdown("**Resposta do Davar:**")
    st.write(st.session_state["resposta"])
