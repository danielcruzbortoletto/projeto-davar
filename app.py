import streamlit as st
import openai
import os

# Configuração da chave da OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Projeto Davar", layout="wide")

# Inicializar o histórico da sessão se ainda não existir
if 'mensagens' not in st.session_state:
    st.session_state['mensagens'] = []

# Título principal
st.title("🤖 Projeto Davar – Escuta com Inteligência e Presença")

# Criar duas colunas: histórico (esquerda) e interação (direita)
col1, col2 = st.columns([1, 2])

# Coluna da esquerda: histórico da sessão com aviso de privacidade
with col1:
    st.markdown("### 🗂️ Histórico da sessão")

    st.info("🔒 **Privacidade garantida:** suas perguntas não são salvas após fechar esta janela. Nenhum dado é armazenado em servidor. Esta é uma escuta segura e efêmera — como uma boa conversa deve ser.")

    if st.session_state['mensagens']:
        for i, m in enumerate(st.session_state['mensagens']):
            st.markdown(f"**Você:** {m['pergunta']}")
            st.markdown(f"**Davar:** {m['resposta']}")
            st.markdown("---")
    else:
        st.info("Nenhuma pergunta feita ainda.")

# Coluna da direita: interação com o Davar
with col2:
    st.markdown("### 💬 Faça sua pergunta ao Davar")
    pergunta = st.text_input("Digite aqui sua pergunta", key="pergunta_input")

    if st.button("Enviar"):
        if pergunta.strip() != "":
            with st.spinner("Davar está refletindo..."):
                resposta = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Você é o Davar, uma IA que escuta com empatia e responde com sabedoria."},
                        {"role": "user", "content": pergunta}
                    ]
                )["choices"][0]["message"]["content"]

                st.session_state['mensagens'].append({
                    "pergunta": pergunta,
                    "resposta": resposta
                })

                st.markdown(f"**Davar:** {resposta}")
        else:
            st.warning("Por favor, digite uma pergunta antes de enviar.")
