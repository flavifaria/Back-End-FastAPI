# API - Mercearia do Erinaldo

API RESTful para gestão de uma mercearia, construída com **FastAPI**, **SQLAlchemy** e **SQLite**.

## Tabela de Conteúdos
- [Visão Geral](#visão-geral)
- [Tecnologias](#tecnologias)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Execução](#execução)
- [Endpoints da API](#endpoints-da-api)
- [Arquitetura](#arquitetura)
- [Autenticação e Autorização](#autenticação-e-autorização)
- [Base de Dados](#base-de-dados)

---

## Visão Geral

Sistema de back-end para uma mercearia que permite:
- Registo e gestão de utilizadores com perfis diferenciados
- Autenticação via JWT (JSON Web Tokens)
- CRUD completo de produtos
- Upload de imagens para produtos

## Tecnologias

| Dependência | Versão | Função |
|---|---|---|
| FastAPI | 0.135.1 | Framework web assíncrona |
| SQLAlchemy | 2.0.48 | ORM para base de dados |
| SQLite | - | Base de dados relacional |
| PyJWT | 2.12.1 | Geração e validação de tokens JWT |
| Passlib + Bcrypt | 1.7.4 / 3.2.2 | Hash seguro de passwords |
| Pydantic | 2.12.5 | Validação e serialização de dados |
| Uvicorn | 0.41.0 | Servidor ASGI |
| python-multipart | 0.0.22 | Suporte a upload de ficheiros |

---

## Estrutura do Projeto

```
Fast API - SQLLite/
├── app/
│   ├── main.py                  # Ponto de entrada da aplicação
│   ├── requirements.txt           # Dependências Python
│   ├── mercearia.db               # Base de dados SQLite (gerada automaticamente)
│   ├── core/                      # Módulo central
│   │   ├── config.py              # Configurações globais (Settings)
│   │   ├── database.py            # Conexão com a base de dados
│   │   ├── security.py            # Hash de passwords e geração de JWT
│   │   └── dependences.py         # Dependências (get_db, get_current_user, get_current_gestor)
│   ├── modules/
│   │   ├── users/
│   │   │   ├── models.py          # Modelo ORM da tabela 'users'
│   │   │   ├── schemas.py         # Pydantic schemas (UserCreate, UserResponse)
│   │   │   ├── repositories.py    # Camada de acesso a dados
│   │   │   ├── services.py        # Regras de negócio
│   │   │   └── routers.py         # Endpoints HTTP
│   │   ├── auth/
│   │   │   ├── schemas.py         # Schema Token
│   │   │   └── routers.py         # Endpoint de login
│   │   └── products/
│   │       ├── models.py          # Modelo ORM da tabela 'produtos'
│   │       ├── schemas.py         # Pydantic schemas
│   │       ├── repositories.py    # Camada de acesso a dados
│   │       ├── services.py        # Regras de negócio
│   │       └── routers.py         # Endpoints HTTP
│   ├── static/
│   │   └── images/                # Imagens dos produtos
│   └── tests/
├── teste_bd.py                    # Script de teste de conexão à base de dados
└── .env                           # Variáveis de ambiente (opcional)
```

---

## Instalação

```bash
# 1. Criar ambiente virtual
cd "app"
python -m venv .venv

# 2. Ativar ambiente virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt
```

---

## Execução

```bash
# Dentro da pasta app/
uvicorn main:app --reload
```

A API ficará disponível em:
- **Base:** `http://127.0.0.1:8000`
- **Swagger UI (documentação interativa):** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

Para testar a conexão à base de dados separadamente:

```bash
# Na raiz do projeto (fora de app/)
python teste_bd.py
```

---

## Endpoints da API

### Root

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/` | Mensagem de confirmação do servidor |

### Autenticação

| Método | Rota | Descrição | Body |
|---|---|---|---|
| `POST` | `/auth/login` | Login e geração de token JWT | Form (`username` = email, `password`) |

### Utilizadores

| Método | Rota | Descrição | Auth |
|---|---|---|---|
| `POST` | `/users/` | Criar novo utilizador | Não |
| `GET` | `/users/me` | Obter dados do próprio perfil | Sim (token de qualquer perfil) |
| `DELETE` | `/users/{user_id}` | Apagar utilizador (soft delete) | Sim (apenas `gestor`) |

### Produtos

| Método | Rota | Descrição | Body |
|---|---|---|---|
| `POST` | `/produtos/` | Criar produto | `ProdutoCreate` |
| `GET` | `/produtos/` | Listar todos os produtos | - |
| `GET` | `/produtos/{id}` | Buscar produto por ID | - |
| `PUT` | `/produtos/{id}` | Atualizar produto | `ProdutoUpdate` |
| `DELETE` | `/produtos/{id}` | Apagar produto | - |
| `POST` | `/produtos/{id}/imagem` | Upload de imagem para produto | `UploadFile` (imagem) |

---

## Arquitetura

O projeto segue uma arquitetura em camadas, por módulo:

```
Router (HTTP) → Service (Regras de Negócio) → Repository (Acesso a Dados) → Database
```

- **Router** (`routers.py`): Define os endpoints HTTP, valida inputs via Pydantic schemas e despacha para os services.
- **Service** (`services.py`): Contém a lógica de negócio (verificações de negócio, hash de passwords, etc.).
- **Repository** (`repositories.py`): Abstração para operações CRUD na base de dados via SQLAlchemy.
- **Schema** (`schemas.py`): Define os modelos de entrada/saída com validação pelo Pydantic.
- **Model** (`models.py`): Mapeamento ORM das tabelas da base de dados.

---

## Autenticação e Autorização

### Fluxo de Login

1. Cliente envia email e password via `POST /auth/login`
2. O sistema verifica o utilizador pelo email no banco de dados
3. A password é comparada com o hash armazenado (Bcrypt)
4. Se válido, gera um **JWT token** contendo:
   - `sub`: email do utilizador
   - `role`: papel/perfil do utilizador
5. Token expira após **30 minutos** (configurável)

### Perfis de Utilizador

| Perfil | Descrição | Permissões |
|---|---|---|
| `cliente` | Utilizador padrão | Aceder a próprio perfil |
| `vendedor` | Equipa de vendas | Aceder a próprio perfil |
| `gestor` | Administrador | Todas as permissões + apagar utilizadores |
| `fornecedor` | Fornecedor externo | Aceder a próprio perfil |

### Proteção de Rotas

- `get_current_user` (em `dependences.py`): Extrai e valida o token JWT, devolve o utilizador autenticado
- `get_current_gestor`: Verifica além da autenticação se o perfil é `gestor`, caso contrário retorna **403 Forbidden**

---

## Base de Dados

### Tabela `users`

| Coluna | Tipo | Constraint |
|---|---|---|
| `id` | Integer | Primary Key, Index |
| `nome` | String | Not Null, Index |
| `email` | String | Unique, Not Null, Index |
| `hashed_password` | String | Not Null |
| `role` | Enum | Default = `cliente` |
| `is_active` | Boolean | Default = `True` |

### Tabela `produtos`

| Coluna | Tipo | Constraint |
|---|---|---|
| `id` | Integer | Primary Key, Index |
| `nome` | String | Index |
| `descrição` | String | Nullable |
| `preço` | Float | - |
| `estoque` | Integer | Default = `0` |

### Configuração

As definições de conexão estão em `core/config.py` e podem ser sobrescritas via ficheiro `.env`:

```env
DATABASE_URL=sqlite:///./mercearia.db
SECRET_KEY=sua-chave-super-secreta-aqui-mude-em-producao
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> **Atenção:** Em produção, altere a `SECRET_KEY` e considere usar um banco de dados como PostgreSQL ao invés de SQLite.
