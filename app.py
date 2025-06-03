import streamlit as st
import openai
import os

# Config da API
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Projeto Davar", layout="centered")

st.title("🤖 Davar – escuta com presença")
st.markdown("🔒 Nenhuma conversa é salva. Ao fechar esta aba, tudo será apagado.")

# Inicializa histórico
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Botão para limpar conversa
if st.button("🧹 Nova conversa"):
    st.session_state.chat_history = []
    st.experimental_rerun()

# Entrada do usuário
user_input = st.text_input("Escreva aqui sua pergunta, desabafo ou reflexão:")

# Função para gerar resposta com histórico
def gerar_resposta_com_gpt(historico):
    messages = [{"role": "system", "content": "Você é o Davar, um parceiro de escuta. Responda com empatia, profundidade e presença."}]
    messages.extend(historico)
    resposta = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.7
    )
    return resposta.choices[0].message.content.strip()

# Processa entrada do usuário
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    resposta = gerar_resposta_com_gpt(st.session_state.chat_history)
    st.session_state.chat_history.append({"role": "assistant", "content": resposta})

# Exibe histórico formatado
for mensagem in st.session_state.chat_history:
    if mensagem["role"] == "user":
        st.markdown(f"**Você:** {mensagem['content']}")
    elif mensagem["role"] == "assistant":
        st.markdown(f"**Davar:** {mensagem['content']}")
