# Limpa campo após rerun, se necessário
if "clear_input" in st.session_state and st.session_state.clear_input:
    st.session_state.entrada_temp = ""
    st.session_state.clear_input = False

# Processa envio
if enviar and api_key:
    if audio:
        st.warning("Reconhecimento de voz ainda não está ativado. Por enquanto, envie texto manualmente.")
    if st.session_state.entrada_temp.strip():
        entrada = st.session_state.entrada_temp.strip()
        st.session_state.historico.append({"role": "user", "content": entrada})
        try:
            resposta = conversar_com_davar(st.session_state.historico)
            st.session_state.historico.append({"role": "assistant", "content": resposta})
            st.session_state.contador += 1
            st.session_state.resposta = resposta
            st.session_state.clear_input = True  # marca para limpar no próximo ciclo
            st.experimental_rerun()
        except openai.AuthenticationError:
            st.error("API Key inválida. Verifique e tente novamente.")
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
