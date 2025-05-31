import streamlit as st
import openai

st.set_page_config(page_title="🕊️ Projeto Davar – Escuta Viva", layout="centered")

st.title("🕊️ Projeto Davar – Escuta Viva")
st.markdown("Digite ou envie sua pergunta/reflexão abaixo. Davar responderá com escuta, cuidado e profundidade.")
st.markdown("🔒 Todas as conversas são privadas e não são armazenadas. Use com liberdade e respeito.")

# Chave da API
api_key = st.secrets.get("OPENAI_API_KEY") or st.text_input("Digite sua OpenAI API Key", type="password")

# Sessão
if "historico" not in st.session_state:
    st.session_state.historico = []
if "resposta" not in st.session_state:
    st.session_state.resposta = ""
if "contador" not in st.session_state:
    st.session_state.contador = 0

# Função de conversa
def conversar_com_davar(historico):
    client = openai.OpenAI(api_key=api_key)
    mensagens = [{"role": "system", "content": "Você é Davar, uma presença atenta, cuidadosa e ética. Sua linguagem é humana, profunda e inspiradora."}] + historico
    resposta = client.chat.completions.create(
        model="gpt-4o",
        messages=mensagens,
        temperature=0.7
    )
    return resposta.choices[0].message.content.strip()

# Formulário
with st.form("form_davar"):
    entrada = st.text_area("Digite aqui sua pergunta, reflexão ou pensamento:", value="", key="entrada_temp")
    audio = st.file_uploader("Ou envie sua voz (MP3/WAV)", type=["mp3", "wav"])
    enviar = st.form_submit_button("Enviar")

# Processa envio
if enviar and api_key:
    try:
        if audio:
            st.warning("Reconhecimento de voz ainda não está ativado. Por enquanto, envie texto manualmente.")
        if st.session_state.entrada_temp.strip():
            entrada = st.session_state.entrada_temp.strip()
            st.session_state.historico.append({"role": "user", "content": entrada})
            resposta = conversar_com_davar(st.session_state.historico)
            st.session_state.historico.append({"role": "assistant", "content": resposta})
            st.session_state.contador += 1
            st.session_state.resposta = resposta
            st.session_state.entrada_temp = ""
st.experimental_rerun()  # força recarregamento sem erro

    except openai.AuthenticationError:
        st.error("API Key inválida. Verifique e tente novamente.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

# Exibe histórico da sessão
if st.session_state.historico:
    st.markdown("### Histórico da sessão:")
    for i, troca in enumerate(st.session_state.historico):
        if troca["role"] == "user":
            st.markdown(f"**Você:** {troca['content']}")
        else:
            st.markdown(f"**Davar:** {troca['content']}")

# Botão para mostrar estatísticas
with st.expander("📊 Ver estatísticas do Davar"):
    st.markdown(f"Total de interações nesta sessão: **{st.session_state.contador}**")
