# Fast-Blog-API ⚡

Uma API de Blog moderna e totalmente assíncrona desenvolvida com **FastAPI**, focada em alta performance, tipagem forte e simplicidade de manutenção.

## ✨ Funcionalidades

- 🚀 **Performance Assíncrona**: Operações de banco de dados não bloqueantes utilizando `databases` e `aiosqlite`.
- 📁 **Arquitetura Limpa**: Organização baseada em Controllers, Models e Views (Schemas).
- ✅ **Validação de Dados**: Uso extensivo do Pydantic V2 para garantir a integridade dos dados.
- 🔄 **Lifespan Management**: Gerenciamento eficiente do ciclo de vida da conexão com o banco de dados.
- 📖 **Documentação Automática**: Swagger UI disponível nativamente para testes de endpoints.

## 🛠️ Stack Tecnológica

- **Framework**: FastAPI
- **Gerenciador de Dependências**: Poetry
- **Banco de Dados**: SQLite (Async)
- **ORM/Query Builder**: SQLAlchemy & Databases
- **Validação**: Pydantic V2

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Python 3.12 ou superior
- Poetry instalado (`pip install poetry`)

### Instalação

1. Instale as dependências do projeto:
   ```bash
   poetry install
   ```

2. Inicie o servidor de desenvolvimento:
   ```bash
   fastapi dev
   ```

3. Acesse a documentação interativa:
   Abra o navegador em http://127.0.0.1:8000/docs.

---
Desenvolvido como um exemplo de backend robusto e moderno com Python.