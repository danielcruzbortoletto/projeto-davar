
import re
import unicodedata

# Lista expandida de expressões sensíveis
SUICIDE_KEYWORDS = [
    r"\bquero morrer\b",
    r"\bnão quero mais viver\b",
    r"\bnão aguento mais\b",
    r"\bvou acabar com tudo\b",
    r"\bnão faz mais sentido\b",
    r"\bnão vejo saída\b",
    r"\bnão tenho mais forças\b",
    r"\bme matar\b",
    r"\bvou me matar\b",
    r"\bninguém se importa comigo\b",
    r"\bminha vida não vale nada\b",
    r"\bseria melhor se eu sumisse\b",
    r"\bestou pensando em desistir\b",
    r"\bnão sou importante\b",
    r"\bninguém vai sentir minha falta\b",
    r"\bcansei de tudo\b",
    r"\bqueria desaparecer\b",
    r"\bperdi a vontade de viver\b",
    r"\bqueria dormir e não acordar\b",
    r"\bnão tenho mais por que lutar\b",
    r"\btudo seria melhor sem mim\b",
    r"\bcheguei no meu limite\b",
    r"\bpreciso de ajuda pra sair disso\b",
    r"\bnão quero mais continuar\b"
]

# Função de normalização para lidar com acentos
def normalize_text(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').lower()

# Verifica se há expressão sensível no texto do usuário
def contains_suicide_keywords(text: str) -> bool:
    normalized_text = normalize_text(text)
    return any(re.search(pattern, normalized_text, re.IGNORECASE) for pattern in SUICIDE_KEYWORDS)

# Mensagem de apoio complementar
def get_suicide_support_message() -> str:
    return (
        "\n\n🧡 *Se você estiver passando por um momento difícil, quero que saiba: você não está sozinho.*\n"
        "Você pode ligar para o **CVV – 188**. É gratuito, 24 horas, com escuta verdadeira e sigilo total.\n"
        "E eu também estou aqui. Posso continuar conversando com você, ou só ficar em silêncio se preferir.\n"
        "Você é importante. Sua vida importa. 🌱"
    )

# Função principal para integrar no fluxo do Davar
def gerar_resposta_final(user_input, resposta_davar):
    if contains_suicide_keywords(user_input):
        resposta_davar += get_suicide_support_message()
    return resposta_davar
