# 🤖 Chat LLM Google

Projeto de exemplo para integração local de um chatbot baseado em Large Language Models (LLMs), utilizando Streamlit como interface interativa.

> Baseado no tutorial:  
> https://elisaterumi.substack.com/p/chatbot-com-langchain-e-streamlit

---

## 📌 Visão Geral

Este projeto demonstra a criação de um chatbot utilizando modelos de linguagem, com foco em:

- Integração com APIs de LLM
- Interface interativa via Streamlit
- Estrutura modular para testes e diagnósticos
- Ambiente local para experimentação

## 📁 Estrutura do Projeto
│
├── app.py # Ponto de entrada da aplicação (interface Streamlit)
├── diag.py # Utilitários de diagnóstico e logs
├── teste.py # Script para testes rápidos
├── requirements.txt # Dependências do projeto
├── .venv/ # Ambiente virtual (não versionar)

## ⚙️ Pré-requisitos

Antes de executar o projeto, certifique-se de possuir:

- Python 3.8 ou superior
- Pip instalado
- (Opcional) VSCode ou outro editor Python


## 🚀 Instalação

### 1️⃣ Clonar o repositório
```powershell
git clone <URL_DO_REPOSITORIO>
cd chat-llm-google
```
### 2️⃣ Criar ambiente virtual
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
### 3️⃣ Instalar dependências
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### ▶️ Como rodar
```powershell
streamlit run app.py
```

### ▶️ Executar testes/demonstração rápida:

```powershell
python teste.py
python diag.py
```

### 🔄 Como atualizar `requirements.txt`

```powershell
pip freeze > requirements.txt
```
