import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Título do app
st.title("🕊️ Projeto Davar – Escuta Viva")
st.markdown("Digite sua reflexão, pergunta ou pensamento. Davar responderá com escuta, cuidado e profundidade.")

# Inicializa o histórico na sessão, se ainda não existir
if "historico" not in st.session_state:
    st.session_state.historico = [
        {"role": "system", "content": "Você é o Davar, um assistente que escuta com cuidado, profundidade e ética. Sua linguagem é afetuosa, reflexiva e humana. Você ajuda a elaborar pensamentos e acolher emoções."}
    ]

# Caixa de entrada do usuário
entrada = st.text_input("Você deseja conversar sobre o quê?")

# Quando o usuário envia uma nova entrada
if entrada:
    st.session_state.historico.append({"role": "user", "content": entrada})
    
    try:
        resposta = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.historico,
            temperature=0.7
        )
        mensagem = resposta.choices[0].message.content
        st.session_state.historico.append({"role": "assistant", "content": mensagem})
        st.markdown(f"**Davar:** {mensagem}")
    
    except Exception as e:
        st.error(f"Ocorreu um erro: {str(e)}")
