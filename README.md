
# 🤖 Projeto Davar – Escuta com Presença

O **Davar** é um projeto sem fins lucrativos que oferece um espaço de escuta acolhedora e empática, com apoio da inteligência artificial.

Acreditamos que **a escuta é um ato de cuidado** — e que a tecnologia pode ser usada para criar ambientes seguros, respeitosos e sensíveis.

---

## 🌟 Funcionalidades

- ✅ Envio de texto para conversas reflexivas
- ✅ Upload de áudio gravado (MP3, WAV, M4A)
- ✅ Gravação de voz direto pelo navegador
- ✅ Transcrição automática com Whisper
- ✅ Respostas humanizadas com base no GPT-4o
- ✅ Nenhuma conversa é salva (privacidade total)
- ✅ Interface acessível e responsiva
- ✅ Projeto sem fins lucrativos, com propósito social

---

## 🧠 Modelo Utilizado

- **Chat:** GPT-4o (OpenAI)
- **Transcrição de Áudio:** Whisper API
- **Interface:** Streamlit
- **Hospedagem:** Streamlit Community Cloud

---

## 🔒 Privacidade

Nenhum dado é armazenado. Todo o conteúdo da conversa é apagado ao encerrar a sessão. Ideal para quem busca escuta sem julgamentos.

---

## 📦 Como Rodar Localmente

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/projeto-davar.git
cd projeto-davar
```

2. Crie um ambiente virtual e instale as dependências:
```bash
python -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate no Windows
pip install -r requirements.txt
```

3. Crie o arquivo `.env` e adicione sua chave da OpenAI:
```
OPENAI_API_KEY=sua-chave-aqui
```

4. Inicie o app:
```bash
streamlit run app.py
```

---

## 🧪 Próximas Etapas (Backlog)

- Integração por voz com WebRTC
- Versão especial para idosos: **Davar Acolhe**
- Modo infantil de reforço escolar: **Davar Amigo**
- Versão musical educativa: **Toca Davar**
- Memória de conversa por sessão
- Integração com WhatsApp e assistentes

---

## ✨ Contato

📩 contato@projetodavar.com  
🌐 [projeto-davar.streamlit.app](https://projeto-davar.streamlit.app)

---

## 💡 Licença

Este projeto é livre para fins educacionais e sociais.  
**Não comercialize o Davar. Respeite o cuidado com que foi criado.**
