import streamlit as st
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Projeto Davar", layout="centered")

if 'mensagens' not in st.session_state:
    st.session_state['mensagens'] = []

st.title("🤖 Projeto Davar – Escuta com Inteligência e Presença")

# 🔒 Aviso de privacidade
st.info("🔒 **Privacidade garantida:** suas perguntas não são salvas após fechar esta janela. Nenhum dado é armazenado em servidor. Esta é uma escuta segura e efêmera — como uma boa conversa deve ser.")

# 🗂️ Histórico da conversa em ordem decrescente (mais recente no topo)
if st.session_state['mensagens']:
    for m in reversed(st.session_state['mensagens']):
        st.markdown(f"**Você:** {m['pergunta']}")
        st.markdown(f"**Davar:** {m['resposta']}")
        st.markdown("---")
else:
    st.info("Nenhuma pergunta feita ainda.")

# 💬 Campo de entrada ao final da página
st.markdown("### ✍️ Escreva sua pergunta")

with st.form("form_chat", clear_on_submit=True):
    pergunta = st.text_input("Digite aqui sua pergunta", placeholder="Como você está hoje?", label_visibility="collapsed")
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
            st.error("⚠️ Ocorreu um erro ao processar sua pergunta. Tente novamente.")
