
# Tela Técnica — Projeto Davar

## 🎯 Objetivo
Explicar tecnicamente a principal diferença entre o Projeto Davar e uma aplicação padrão do ChatGPT.

---

## 📌 Componente-chave: System Prompt

**Local no código:** `app.py`  
**Modelo utilizado:** GPT-4 via OpenAI API

---

## 🧠 Prompt padrão (ChatGPT via site)

```python
{"role": "system", "content": "You are a helpful, honest, and harmless assistant."}
```

---

## 🌱 Prompt personalizado do Davar

```python
{"role": "system", "content": "Você é o Davar, uma IA que escuta com empatia e responde com sabedoria."}
```

---

## 🔍 Impacto prático

| Componente      | ChatGPT padrão            | Projeto Davar                          |
|------------------|---------------------------|----------------------------------------|
| Tom              | Neutro, genérico          | Afetivo, empático, respeitoso          |
| Finalidade       | Ajuda geral               | Escuta ativa e cuidado emocional       |
| Resposta padrão  | Técnica e direta          | Reflexiva, com presença                |
| Linguagem        | Racional                  | Humanizada e adaptada ao sensível      |

---

## ✅ Conclusão

Mesmo utilizando a **mesma API da OpenAI**, o Projeto Davar se diferencia profundamente por causa de **uma única linha de propósito**.

Esse é o poder do `system prompt` quando usado com intenção.
