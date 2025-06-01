import streamlit as st
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Projeto Davar", layout="wide")

if 'mensagens' not in st.session_state:
    st.session_state['mensagens'] = []

st.title("🤖 Projeto Davar – Escuta com Inteligência e Presença")

# Agora a ordem é: interação (esquerda), histórico (direita)
col_interacao, col_historico = st.columns([2, 1])

# 🟢 Coluna da esquerda: interação com o Davar
with col_interacao:
    st.markdown("### 💬 Faça sua pergunta ao Davar")

    with st.form("pergunta_form", clear_on_submit=True):
        pergunta = st.text_input("Digite aqui sua pergunta")
        submitted = st.form_submit_button("Enviar")

    if submitted and pergunta.strip():
        with st.spinner("Davar está refletindo..."):
            try:
                resposta = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Você é o Davar, uma IA que escuta com empatia e responde com sabedoria."},
                        {"role": "user", "content": pergunta}
                    ]
                ).choices[0].message.content

                st.session_state['mensagens'].append({
                    "pergunta": pergunta,
                    "resposta": resposta
                })

                st.markdown(f"**Davar:** {resposta}")
            except Exception as e:
                st.error("Ocorreu um erro ao processar sua pergunta. Tente novamente.")

# 🟡 Coluna da direita: histórico da sessão
with col_historico:
    st.markdown("### 🗂️ Histórico da sessão")

    st.info("🔒 **Privacidade garantida:** suas perguntas não são salvas após fechar esta janela. Nenhum dado é armazenado em servidor. Esta é uma escuta segura e efêmera — como uma boa conversa deve ser.")

    if st.session_state['mensagens']:
        for i, m in enumerate(st.session_state['mensagens']):
            st.markdown(f"**Você:** {m['pergunta']}")
            st.markdown(f"**Davar:** {m['resposta']}")
            st.markdown("---")
    else:
        st.info("Nenhuma pergunta feita ainda.")

