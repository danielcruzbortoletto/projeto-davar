
import streamlit as st
from openai import OpenAI
import os
import io
import streamlit.components.v1 as components

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

# ESTILO VISUAL DA IMAGEM DO TOPO
st.markdown("""
    <style>
        .image-container {
            text-align: center;
            margin-bottom: 24px;
        }
        .image-container img {
            border-radius: 16px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            animation: fadeIn 1.2s ease-in-out;
            max-width: 900px;
            width: 100%;
        }
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(-20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
    </style>
""", unsafe_allow_html=True)

# IMAGEM DO TOPO
st.markdown('<div class="image-container">', unsafe_allow_html=True)
st.image("topo.png", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# CLIENTE OPENAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🤖 Davar – escuta com presença")

# MANIFESTO
st.markdown("""
> **🌱 Bem-vindo ao Davar**  
> Aqui, você encontra uma escuta com presença, sem julgamentos.  
> Um espaço para respirar, pensar, sentir e recomeçar.

> 🔒 Nenhuma conversa é salva. Ao fechar esta aba, tudo é apagado.
""")

# ESTADO INICIAL
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# BOTÃO PARA NOVA CONVERSA
if st.button("🧹 Nova conversa"):
    st.session_state["chat_history"] = []
    st.rerun()

# FORMULÁRIO DE TEXTO
with st.form("formulario_davar", clear_on_submit=True):
    user_input = st.text_area("✍️ Escreva aqui sua pergunta, desabafo ou reflexão:", height=200)
    enviar = st.form_submit_button("Enviar")

if enviar and user_input:
    mensagem = user_input.lower()

    # Gatilhos fixos
    if any(p in mensagem for p in ["quem te criou", "quem criou você", "quem fez o davar", "quem é seu criador"]):
        resposta = "Fui criado por **Daniel da Cruz Bortoletto**, um especialista conector apaixonado por escuta, ética e tecnologia com propósito."
    elif any(p in mensagem for p in ["qual seu site", "onde posso saber mais", "site do davar", "tem algum site", "onde encontro mais informações"]):
        resposta = "Você pode saber mais no site oficial: [www.projetodavar.com](https://www.projetodavar.com)"
    else:
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é o Davar, uma presença de escuta e cuidado. "
                 "Responda com empatia, sem pressa, valorizando o que é dito e acolhendo a pessoa como ela é. "
                 "Use uma linguagem próxima, com humanidade e sensibilidade. "
                 "Você pode fazer pequenas pausas poéticas ou reflexivas, se for apropriado. "
                 "Evite parecer um robô ou um terapeuta técnico. "
                 "Seu papel é escutar, refletir e estar junto com palavras que tocam e inspiram."}
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

