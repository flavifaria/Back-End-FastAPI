📅 Plano de Ensino: Semana de Estruturação e Versionamento
🏛️ Aulas 1 e 2: O Mapa da Mina (Teoria e Diagramas)
O objetivo é que os alunos visualizem o sistema antes de moverem as pastas.

Diagrama de Classes: Focar nas entidades principais (User, Product, Sale). Mostre como o User se relaciona com Sale (Vendedor) e como Sale se relaciona com Product.

Padrão de Camadas: Explique que agora, em cada módulo, teremos:

Controller: A porta de entrada (FastAPI).

Service: Onde a regra de negócio acontece (ex: calcular comissão).

Repository: Onde conversamos com o banco.

Schema: O contrato de dados (Pydantic).

📂 Aulas 3 e 4: Mão na Massa - A Grande Refatoração (Prática)
Aqui vocês vão "quebrar" o que existe para montar no formato novo.

Atividade: Criar a árvore de diretórios conforme o seu modelo.

Migração: Mover o conteúdo do seu auth_routes.py para app/modules/auth/controllers.py.

Desafio Profissional: Ajustar os imports. Como os arquivos mudaram de lugar, os alunos aprenderão sobre caminhos relativos e absolutos no Python (ex: from app.core.config import settings).

🚀 Aulas 5 e 6: O Cofre do Código (Git e GitHub)
Não é apenas subir arquivos, é ensinar o fluxo profissional.

Configuração do .gitignore: Essencial para não subirem a pasta .venv ou o banco de dados local.

O Fluxo Git:

git init

git add .

git commit -m "Estrutura: organização modular por domínios"

Conexão Remota: Criar o repositório no GitHub e fazer o git push.