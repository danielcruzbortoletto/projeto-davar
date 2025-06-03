import streamlit as st
import openai
import os

# Configuração da API
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Projeto Davar", layout="centered")

# Aviso de privacidade
st.markdown("🔒 As conversas não são salvas. Ao fechar esta aba, tudo será apagado.")

# Inicializa o histórico se ainda não existir
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Título do app
st.title("🤖 Davar – escuta com presença")

# Campo de entrada de texto
user_input = st.text_input("Digite sua pergunta ou reflexão:")

# Função para gerar resposta com histórico
def gerar_resposta_com_gpt(historico):
    resposta = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é o Davar, um parceiro de escuta. Responda com empatia, profundidade e respeito."},
            *historico
        ],
        temperature=0.7
    )
    return resposta.choices[0].message.content

# Se o usuário enviar uma pergunta
if user_input:
    # Adiciona pergunta ao histórico
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Gera resposta com histórico
    resposta = gerar_resposta_com_gpt(st.session_state.chat_history)

    # Adiciona resposta ao histórico
    st.session_state.chat_history.append({"role": "assistant", "content": resposta})

# Exibe a conversa
for mensagem in st.session_state.chat_history:
    if mensagem["role"] == "user":
        st.markdown(f"**Você:** {mensagem['content']}")
    elif mensagem["role"] == "assistant":
        st.markdown(f"**Davar:** {mensagem['content']}")
