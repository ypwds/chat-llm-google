import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Adicionamos a versão da API explicitamente
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite", 
    google_api_key="SUA_CHAVE_AQUI",
    api_version="v1"  # <--- Isso força a saída da v1beta que está dando erro
)

try:
    print(llm.invoke("Olá, você está funcionando?").content)
except Exception as e:
    print(f"Erro direto no script: {e}")