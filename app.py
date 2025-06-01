import streamlit as st
from openai import OpenAI
import os

# Inicializa o cliente da OpenAI com a chave da API do ambiente
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configuração da página
st.set_page_config(page_title="Projeto Davar", layout="wide")

# Inicializa o histórico na sessão se ainda não existir
if 'mensagens' not in st.session_state:
    st.session_state['mensagens'] = []

# Título do app
st.title("🤖 Projeto Davar – Escuta com Inteligência e Presença")

# Cria o layout com duas colunas: histórico (col1) e interação (col2)
col1, col2 = st.columns([2, 1])

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

    # Formulário com botão e envio por Enter (clear_on_submit limpa o campo)
    with st.form("pergunta_form", clear_on_submit=True):
        pergunta = st.text_input("Digite aqui sua pergunta")
        submitted = st.form_submit_button("Enviar")

    # Quando a pergunta for enviada
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

                # Adiciona ao histórico
                st.session_state['mensagens'].append({
                    "pergunta": pergunta,
                    "resposta": resposta
                })

                # Exibe a resposta imediatamente
                st.markdown(f"**Davar:** {resposta}")
            except Exception as e:
                st.error("Ocorreu um erro ao processar sua pergunta. Tente novamente.")
