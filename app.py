import streamlit as st
import openai
import os

# Configuração da página
st.set_page_config(page_title="🕊️ Projeto Davar – Escuta Viva", layout="centered")

st.title("🕊️ Projeto Davar – Escuta Viva")
st.markdown("Digite sua reflexão, pergunta ou pensamento. Davar responderá com escuta, cuidado e profundidade.")

# Recupera a chave da API
api_key = st.secrets.get("OPENAI_API_KEY")

# Inicializa o campo no session_state, se ainda não existir
if "entrada_texto" not in st.session_state:
    st.session_state.entrada_texto = ""

# Interface do formulário
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

# Execução da conversa
if enviar and api_key:
    try:
        resposta = conversar_com_davar(entrada)
        st.markdown("**Resposta do Davar:**")
        st.write(resposta)

        # Limpa o campo de entrada
        st.session_state.entrada_texto = ""

    except openai.AuthenticationError:
        st.error("API Key inválida. Verifique e tente novamente.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
