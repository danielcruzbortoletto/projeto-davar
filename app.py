import streamlit as st
import openai
import os

# Configuração da página
st.set_page_config(page_title="🕊️ Projeto Davar – Escuta Viva", layout="centered")

st.title("🕊️ Projeto Davar – Escuta Viva")
st.markdown("Digite sua reflexão, pergunta ou pensamento. Davar responderá com escuta, cuidado e profundidade.")

# Obtendo API Key de forma segura
api_key = st.secrets.get("OPENAI_API_KEY", "")

if not api_key:
    api_key = st.text_input("Digite sua OpenAI API Key", type="password")

# Inicializa o campo de entrada no session_state
if "entrada_texto" not in st.session_state:
    st.session_state.entrada_texto = ""

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

# Interface do formulário
with st.form("form_davar"):
    entrada = st.text_area("Você deseja conversar sobre o quê?", value=st.session_state.entrada_texto, key="entrada_texto_form")
    enviar = st.form_submit_button("Enviar")

# Processamento
if enviar and api_key:
    try:
        resposta = conversar_com_davar(entrada)
        st.markdown("**Resposta do Davar:**")
        st.write(resposta)
        st.session_state.entrada_texto = ""  # Limpa o valor na session_state
        st.rerun()  # Recarrega a página para limpar o campo corretamente

    except openai.AuthenticationError:
        st.error("API Key inválida. Verifique e tente novamente.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
