import streamlit as st
import openai
from io import BytesIO

st.set_page_config(page_title="🕊️ Projeto Davar – Escuta Viva", layout="centered")

# Título e descrição
st.title("🕊️ Projeto Davar – Escuta Viva")
st.markdown("Digite ou envie sua reflexão. Davar responderá com escuta, cuidado e profundidade.")
st.markdown("🔒 Todas as conversas são privadas e não são armazenadas. Use com liberdade e respeito.")

# Chave da API
api_key = st.secrets.get("OPENAI_API_KEY") or st.text_input("Digite sua OpenAI API Key", type="password")

# Inicialização de estado
if "historico" not in st.session_state:
    st.session_state.historico = []
if "resposta" not in st.session_state:
    st.session_state.resposta = ""
if "contador" not in st.session_state:
    st.session_state.contador = 0
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

# Limpeza do campo de entrada após envio
if st.session_state.clear_input:
    st.session_state.entrada_temp = ""
    st.session_state.clear_input = False

# Função principal de conversa
def conversar_com_davar(historico):
    client = openai.OpenAI(api_key=api_key)
    mensagens = [{"role": "system", "content":
        "Você é Davar, uma presença atenta, cuidadosa e ética. Sua linguagem é humana, profunda e inspiradora."}] + historico

    resposta = client.chat.completions.create(
        model="gpt-4o",
        messages=mensagens,
        temperature=0.7
    )
    return resposta.choices[0].message.content.strip()

# Formulário de entrada
with st.form("form_davar"):
    st.markdown("**Digite aqui sua pergunta, reflexão ou pensamento:**")
    entrada = st.text_area("", key="entrada_temp")
    st.markdown("**Ou envie sua voz (MP3 ou WAV)**")
    audio = st.file_uploader("Drag and drop file here", type=["mp3", "wav"])
    enviar = st.form_submit_button("Enviar")

# Processamento da entrada
if enviar and api_key:
    if audio:
        st.warning("Reconhecimento de voz ainda não está ativado. Por enquanto, envie texto manualmente.")
    if st.session_state.entrada_temp.strip():
        entrada = st.session_state.entrada_temp.strip()
        st.session_state.historico.append({"role": "user", "content": entrada})
        try:
            resposta = conversar_com_davar(st.session_state.historico)
            st.session_state.historico.append({"role": "assistant", "content": resposta})
            st.session_state.resposta = resposta
            st.session_state.contador += 1
            st.session_state.clear_input = True
            st.experimental_rerun()
        except openai.AuthenticationError:
            st.error("API Key inválida. Verifique e tente novamente.")
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")

# Exibição do histórico
if st.session_state.historico:
    st.markdown("---")
    st.subheader("Histórico desta sessão:")
    for i, msg in enumerate(st.session_state.historico):
        autor = "Você" if msg["role"] == "user" else "Davar"
        st.markdown(f"**{autor}:** {msg['content']}")

# Estatísticas (contador de respostas)
with st.expander("📊 Ver estatísticas do Davar"):
    st.markdown(f"Respostas dadas nesta sessão: **{st.session_state.contador}**")
