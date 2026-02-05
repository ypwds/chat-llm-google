import google.generativeai as genai

genai.configure(api_key="SUA_CHAVE_AQUI")

print("--- Modelos disponíveis para sua chave ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Nome: {m.name}")
except Exception as e:
    print(f"Erro ao listar: {e}")