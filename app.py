import streamlit as st
import openai
import os

st.set_page_config(page_title="🕊️ Projeto Davar – Escuta Viva", layout="centered")

st.title("🕊️ Projeto Davar – Escuta Viva")
st.markdown("Digite sua reflexão, pergunta ou pensamento. Davar responderá com escuta, cuidado e profundidade.")

# Carrega a chave da API da OpenAI de forma segura
api_key = st.secrets["api_key"] if "api_key" in st.secrets else st.text_input("Digite sua OpenAI API Key", type="password")

# Campo de entrada fora do formulário, com controle por session_state
entrada = st.text_area("Você deseja conversar sobre o quê?", key="entrada_texto")

# Função principal de chamada à OpenAI
def conversar_com_davar(mensagem):
    client = openai.OpenAI(api_key=api_key)
    mensagens = [
        {
            "role": "system",
            "content": (
                "Você é Davar, uma presença atenta, cuidadosa e ética. "
                "Sua linguagem é humana, profunda e inspiradora. Responda com escuta ativa e sensibilidade."
            )
        },
        {"role": "user", "content": mensagem}
    ]
    resposta = client.chat.completions.create(
        model="gpt-4o",
        messages=mensagens,
        temperature=0.7
    )
    return resposta.choices[0].message.content.strip()

# Quando o botão for clicado
if st.button("Enviar") and entrada and api_key:
    try:
        resposta = conversar_com_davar(entrada)
        st.markdown("**Resposta do Davar:**")
        st.write(resposta)

        # Limpa o campo após envio
        st.session_state["entrada_texto"] = ""

    except openai.AuthenticationError:
        st.error("API Key inválida. Verifique e tente novamente.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
