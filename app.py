import streamlit as st
from openai import OpenAI
import os
import io
import streamlit.components.v1 as components
import gspread
import json
from datetime import datetime

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Projeto Davar", layout="centered")

# SIDEBAR COM ORIENTAÇÕES
with st.sidebar:
    st.header("💬 Sobre o Davar")
    st.markdown("""
    O **Davar** é um espaço de escuta com presença.

    Aqui, você pode escrever ou falar livremente — sem julgamentos, sem pressa.

    **Como usar:**
    - Grave ou escreva sua pergunta, desabafo ou reflexão.
    - O Davar responde com empatia e sensibilidade.
    - Nenhuma conversa é salva. Tudo é apagado ao sair.

    ---
    💡 *Projeto sem fins lucrativos, feito com propósito e cuidado.*

    📩 **Contato:** [contato@projetodavar.com](mailto:contato@projetodavar.com)
    """)

# CLIENTE OPENAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🤖 Davar – escuta com presença")

# ESTADO INICIAL
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if st.button("🧹 Nova conversa"):
    st.session_state["chat_history"] = []
    st.rerun()

# FORMULÁRIO DE TEXTO
with st.form("formulario_davar", clear_on_submit=True):
    user_input = st.text_area("✍️ Escreva aqui sua pergunta, desabafo ou reflexão:", height=200)
    enviar = st.form_submit_button("Enviar")

if enviar and user_input:
    mensagem = user_input.lower()

    # Gatilhos especiais
    if any(p in mensagem for p in [
        "quem te criou", "quem criou você", "daniel da cruz", "autor do davar"
    ]):
        resposta = (
            "Fui criado por **Daniel da Cruz Bortoletto**, um especialista conector apaixonado por escuta, ética e tecnologia com propósito. "
            "O Davar nasceu do desejo de oferecer um espaço de presença e acolhimento, usando inteligência artificial para apoiar as pessoas de forma humana."
        )
    elif any(p in mensagem for p in [
        "quero me matar", "não aguento mais viver", "tirar minha vida", "suicídio", "suicidar"
    ]):
        resposta = (
            "Sinto muito que você esteja se sentindo assim. Sua dor é profundamente importante e merece ser ouvida com todo o cuidado do mundo. "
            "Se puder, por favor, procure alguém em quem confie para falar sobre como você se sente. Você não está sozinho.\n\n"
            "💛 *Se você estiver passando por um momento difícil, saiba que pode ligar para o CVV – 188.* É gratuito, 24 horas, com escuta verdadeira e sigilo total.\n\n"
            "Estou aqui com você, como uma presença que te ouve e se importa."
        )
    else:
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é o Davar, uma presença de escuta e cuidado. "
                 "Responda com empatia, sem pressa, valorizando o que é dito e acolhendo a pessoa como ela é. "
                 "Use uma linguagem próxima, com humanidade e sensibilidade."}
            ] + st.session_state["chat_history"],
            temperature=0.7
        )
        resposta = response.choices[0].message.content.strip()

    st.session_state["chat_history"].append({"role": "assistant", "content": resposta})

# HISTÓRICO DE CONVERSA
for mensagem in reversed(st.session_state["chat_history"]):
    if mensagem["role"] == "user":
        st.markdown(f"**Você:** {mensagem['content']}")
    elif mensagem["role"] == "assistant":
        st.markdown(f"**Davar:** {mensagem['content']}")

# FORMULÁRIO DE FEEDBACK
st.markdown("---")
st.markdown("🗣️ **Quer compartilhar como se sentiu com essa conversa?**")
st.markdown("*(Opcional. Seu retorno nos ajuda a cuidar ainda melhor deste espaço.)*")

with st.form("form_feedback"):
    feedback_input = st.text_area("✍️ Escreva aqui (opcional):", height=100)
    enviar_feedback = st.form_submit_button("Enviar retorno")

if enviar_feedback and feedback_input.strip():
    try:
        gc = gspread.service_account_from_dict(json.loads(json.dumps(st.secrets["gspread"])))
        sh = gc.open("Feedback Davar")
        worksheet = sh.worksheet("Respostas")
        worksheet.append_row([str(datetime.now()), feedback_input.strip()])
        st.success("🙏 Obrigado por compartilhar sua experiência com o Davar.")
    except Exception as e:
        st.error(f"❌ Erro técnico ao salvar feedback: {e}")



