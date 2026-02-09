import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent

# Configuração da página
st.set_page_config(
    page_title="Chatbot com LangChain e Streamlit e Tools",
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

# Função para inicializar o modelo with Agente com ferramentas 
@st.cache_resource
def build_agent(api_key: str):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=api_key,
        temperature=0.3,
        max_tokens=250,
    )

    tools = [DuckDuckGoSearchRun()]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um assistente útil. Use ferramentas quando precisar de informações atuais."),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=3)

# Sidebar
if st.button("Limpar Conversa"):
    st.session_state.messages = []
    st.cache_resource.clear()
    st.rerun()

# Verificar se a API key foi fornecida
if not api_key:
    st.warning("⚠️ Por favor, insira sua API Key do Google na barra lateral para começar.")
    st.stop()

# Inicializar o agente
agent_executor = build_agent(api_key)

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
                chat_history = []
                for msg in st.session_state.messages[:-1]:  # sem a msg atual
                    if msg["role"] == "user":
                        chat_history.append(HumanMessage(content=msg["content"]))
                    else:
                        chat_history.append(AIMessage(content=msg["content"]))
                
                # Gerar resposta
                result = agent_executor.invoke({
                    "input": prompt,
                    "chat_history": chat_history
                })

                assistant_response = result["output"]
                
                # Exibir resposta
                st.write(assistant_response)
                
                # Adicionar resposta ao histórico
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": assistant_response
                })
                
            except Exception as e:
                st.error(f"Erro ao gerar resposta: {str(e)}")