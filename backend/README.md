# Sistema de Gestão de Notas de Alunos - Backend API

Sistema completo para gerenciamento de notas acadêmicas desenvolvido com FastAPI, SQLAlchemy e PostgreSQL.

## 📋 Funcionalidades

### Gestão de Usuários
- ✅ Cadastro, edição e remoção de usuários
- ✅ Sistema de login e autenticação JWT
- ✅ Controle de permissões (Aluno, Professor, Administrador)

### Gestão Acadêmica
- ✅ Gerenciamento de alunos e professores
- ✅ Cadastro de disciplinas e períodos
- ✅ Criação e gerenciamento de turmas
- ✅ Sistema de matrículas

### Gestão de Notas
- ✅ Cadastro de avaliações por turma
- ✅ Registro e edição de notas
- ✅ Cálculo automático de média final
- ✅ Sistema de pesos para avaliações

### Relatórios
- ✅ Relatório de notas por aluno
- ✅ Relatório de desempenho por disciplina
- ✅ Relatório geral por período
- ✅ Histórico acadêmico completo

## 🚀 Instalação

### Pré-requisitos
- Python 3.10+
- PostgreSQL 12+

### 1. Clone o repositório
```bash
git clone https://github.com/Ricardo-rtc/projeto-lpg3
cd projeto-lpg3
```

### 2. Crie ambiente virtual
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

Crie um banco PostgreSQL:
```sql
CREATE DATABASE projetolpdb;
```

Execute o script SQL fornecido (`database.sql`) para criar as tabelas:
```bash
psql -U seu_usuario -d projetolpdb -f database.sql
```

### 5. Configure variáveis de ambiente

Copie o arquivo `.env.example` para `.env`:
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:
```env
DATABASE_URL=postgresql://seu_usuario:sua_senha@localhost:5432/projetolpdb
SECRET_KEY=gere-uma-chave-secreta-forte-aqui
```

### 6. Inicie a aplicação
```bash
uvicorn app.main:app --reload
```

A API estará disponível em: **http://localhost:8000**

## 📚 Documentação da API

Acesse a documentação interativa em:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Autenticação

A API usa JWT (JSON Web Tokens) para autenticação.

### Login
```bash
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=seu_usuario&password=sua_senha
```

Resposta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Usando o Token
Inclua o token no header de todas as requisições protegidas:
```
Authorization: Bearer seu_token_aqui
```