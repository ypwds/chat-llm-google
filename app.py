import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
import os

# Configuração da página
st.set_page_config(
    page_title="Chatbot com LangChain e Streamlit",
    page_icon="🤖",
    layout="centered"
)

# Título da aplicação
st.title("Chatbot")
st.markdown("*Chatbot com LangChain e Streamlit*")

# Sidebar para configurações
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # Campo para API Key
    api_key = st.text_input(
        "Google API Key",
        type="password",
        help="Cole aqui sua chave de API do Google AI Studio"
    )
    
    if st.button("Limpar Conversa"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📝 Como usar:")
    st.markdown("""
    1. Insira sua API Key do Google
    2. Digite sua mensagem
    3. Pressione Enter ou clique em Enviar
    """)
    
    st.markdown("---")
    st.markdown("### 🔗 Links úteis:")
    st.markdown("[Obter API Key](https://aistudio.google.com/app/apikey)")

# Inicializar o histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Função para inicializar o modelo
@st.cache_resource
def init_model(api_key):
    if not api_key:
        return None
    
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key=api_key,
            temperature=0.3,
            max_tokens=250
        )
        return llm
    except Exception as e:
        st.error(f"Erro ao inicializar o modelo: {str(e)}")
        return None

# Verificar se a API key foi fornecida
if not api_key:
    st.warning("⚠️ Por favor, insira sua API Key do Google na barra lateral para começar.")
    st.stop()

# Inicializar o modelo
llm = init_model(api_key)

if not llm:
    st.error("❌ Não foi possível inicializar o modelo. Verifique sua API Key.")
    st.stop()

# Container para o chat
chat_container = st.container()

# Exibir mensagens do histórico
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
        else:
            with st.chat_message("assistant"):
                st.write(message["content"])

# Input do usuário
if prompt := st.chat_input("Digite sua mensagem aqui..."):
    # Adicionar mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Exibir mensagem do usuário
    with st.chat_message("user"):
        st.write(prompt)
    
    # Gerar resposta do assistente
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                # Preparar o histórico para o modelo
                messages = []
                for msg in st.session_state.messages:
                    if msg["role"] == "user":
                        messages.append(HumanMessage(content=msg["content"]))
                    else:
                        messages.append(AIMessage(content=msg["content"]))
                
                # Gerar resposta
                response = llm.invoke(messages)
                assistant_response = response.content
                
                # Exibir resposta
                st.write(assistant_response)
                
                # Adicionar resposta ao histórico
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": assistant_response
                })
                
            except Exception as e:
                st.error(f"Erro ao gerar resposta: {str(e)}")