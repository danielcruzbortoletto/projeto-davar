import streamlit as st
import openai
import os

# Configurar chave da API da OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Projeto Davar", layout="wide")

# Inicializar estado da sessão
if 'mensagens' not in st.session_state:
    st.session_state['mensagens'] = []

# Título principal
st.title("🤖 Projeto Davar – Escuta com Inteligência e Presença")

# Layout em colunas: histórico (col1) e interação (col2)
col1, col2 = st.columns([1, 2])

# Coluna 1: Histórico da conversa
with col1:
    st.markdown("### 🗂️ Histórico da sessão")
    if st.session_state['mensagens']:
        for i, m in enumerate(st.session_state['mensagens']):
            st.markdown(f"**Você:** {m['pergunta']}")
            st.markdown(f"**Davar:** {m['resposta']}")
            st.markdown("---")
    else:
        st.info("Nenhuma pergunta feita ainda.")

# Coluna 2: Campo de pergunta e resposta atual
with col2:
    st.markdown("### 💬 Faça sua pergunta ao Davar")
    pergunta = st.text_input("Digite aqui sua pergunta", key="pergunta_input")
    
    if st.button("Enviar"):
        if pergunta.strip() != "":
            with st.spinner("Davar está refletindo..."):
                # Chamada à API da OpenAI
                resposta = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Você é o Davar, uma IA que escuta com empatia e responde com sabedoria."},
                        {"role": "user", "content": pergunta}
                    ]
                )["choices"][0]["message"]["content"]

                # Armazena no histórico da sessão
                st.session_state['mensagens'].append({
                    "pergunta": pergunta,
                    "resposta": resposta
                })

                # Mostra resposta imediatamente
                st.markdown(f"**Davar:** {resposta}")
        else:
            st.warning("Por favor, digite uma pergunta antes de enviar.")
