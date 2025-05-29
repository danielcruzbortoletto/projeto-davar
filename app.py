import streamlit as st
import openai

# Configuração da página
st.set_page_config(page_title="🕊️ Projeto Davar – Escuta Viva", layout="centered")

st.title("🕊️ Projeto Davar – Escuta Viva")
st.markdown("Digite sua reflexão, pergunta ou pensamento. Davar responderá com escuta, cuidado e profundidade.")

# Carregar a chave da API
api_key = st.secrets.get("OPENAI_API_KEY", "")

if not api_key:
    api_key = st.text_input("Digite sua OpenAI API Key", type="password")

# Inicializa estados se ainda não existirem
if "entrada_texto" not in st.session_state:
    st.session_state.entrada_texto = ""

if "resposta_davar" not in st.session_state:
    st.session_state.resposta_davar = ""

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

# Formulário de envio
with st.form("form_davar"):
    entrada = st.text_area("Você deseja conversar sobre o quê?", value=st.session_state.entrada_texto, key="entrada_texto")
    enviar = st.form_submit_button("Enviar")

# Processa o envio
if enviar and api_key and entrada.strip():
    try:
        resposta = conversar_com_davar(entrada)
        st.session_state.resposta_davar = resposta
        st.session_state.entrada_texto = ""  # limpa visualmente o campo
    except openai.AuthenticationError:
        st.error("API Key inválida. Verifique e tente novamente.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

# Exibe a resposta (se houver)
if st.session_state.resposta_davar:
    st.markdown("**Resposta do Davar:**")
    st.write(st.session_state.resposta_davar)
