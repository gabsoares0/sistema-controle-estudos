# Sistema de Controle de Estudos

Aplicação web desenvolvida com Python, Flask e SQLite para auxiliar estudantes no controle da rotina de estudos.

O sistema permite cadastrar matérias, registrar sessões de estudo, acompanhar o tempo estudado e visualizar um dashboard com indicadores gerais de desempenho.

## Objetivo do Projeto

O objetivo do projeto é criar uma aplicação simples e funcional para organização de estudos, permitindo que o estudante acompanhe quais matérias está estudando, quanto tempo está dedicando a cada sessão e qual é o seu progresso geral.

Este projeto foi desenvolvido para a disciplina de Desenvolvimento Rápido em Python.

## Tecnologias Utilizadas

- Python
- Flask
- SQLite
- HTML
- CSS
- Git
- GitHub

## Funcionalidades

- Página inicial de apresentação do sistema.
- Cadastro de matérias.
- Listagem de matérias cadastradas.
- Edição de matérias.
- Exclusão de matérias.
- Registro de sessões de estudo.
- Listagem de sessões registradas.
- Edição de sessões de estudo.
- Exclusão de sessões de estudo.
- Dashboard com resumo geral.
- Cálculo do total de matérias cadastradas.
- Cálculo do total de sessões registradas.
- Cálculo do tempo total estudado em minutos e horas.
- Meta semanal de estudos.
- Barra de progresso da meta semanal.
- Classificação do nível do estudante.
- Mensagem motivacional automática com base no desempenho.

## Estrutura do Projeto

```text
sistema-controle-estudos/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── materias.html
│   ├── sessoes.html
│   ├── editar_materia.html
│   └── editar_sessao.html
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Banco de Dados

O sistema utiliza SQLite como banco de dados local. O banco é criado automaticamente ao executar a aplicação pela primeira vez.

### Tabela `materias`

| Campo | Tipo | Descrição |
|---|---|---|
| id | INTEGER | Identificador único da matéria |
| nome | TEXT | Nome da matéria |
| descricao | TEXT | Descrição da matéria |

### Tabela `sessoes_estudo`

| Campo | Tipo | Descrição |
|---|---|---|
| id | INTEGER | Identificador único da sessão |
| materia_id | INTEGER | Identificador da matéria relacionada |
| descricao | TEXT | Descrição do conteúdo estudado |
| duracao | INTEGER | Duração da sessão em minutos |
| data | TEXT | Data da sessão de estudo |

## Rotas da Aplicação

| Rota | Método | Descrição |
|---|---|---|
| `/` | GET | Exibe a página inicial |
| `/dashboard` | GET | Exibe o dashboard geral |
| `/materias` | GET | Lista as matérias cadastradas |
| `/materias` | POST | Cadastra uma nova matéria |
| `/materias/editar/<id>` | GET | Exibe o formulário de edição da matéria |
| `/materias/editar/<id>` | POST | Atualiza os dados da matéria |
| `/materias/excluir/<id>` | POST | Exclui uma matéria |
| `/sessoes` | GET | Lista as sessões de estudo |
| `/sessoes` | POST | Registra uma nova sessão de estudo |
| `/sessoes/editar/<id>` | GET | Exibe o formulário de edição da sessão |
| `/sessoes/editar/<id>` | POST | Atualiza os dados da sessão |
| `/sessoes/excluir/<id>` | POST | Exclui uma sessão de estudo |

## Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/gabsoares0/sistema-controle-estudos.git
```

### 2. Entrar na pasta do projeto

```bash
cd sistema-controle-estudos
```

### 3. Criar o ambiente virtual

```bash
python -m venv venv
```

Caso o comando `python` não funcione no Windows, utilize:

```bash
py -m venv venv
```

### 4. Ativar o ambiente virtual

No Windows:

```bash
venv\Scripts\activate
```

### 5. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 6. Executar a aplicação

```bash
python app.py
```

Ou:

```bash
py app.py
```

### 7. Acessar no navegador

Abra o navegador e acesse:

```text
http://127.0.0.1:5000
```

## Regras de Negócio

- Uma matéria deve possuir um nome obrigatório.
- Uma sessão de estudo deve estar vinculada a uma matéria.
- A duração da sessão de estudo deve ser maior que zero.
- Cada sessão deve possuir uma data de realização.
- Ao excluir uma matéria, as sessões relacionadas a ela também são removidas.
- O dashboard calcula automaticamente os totais com base nas sessões cadastradas.
- A meta semanal de estudos é utilizada para calcular o progresso do estudante.
- O nível do estudante é definido com base no total de horas registradas.

## Segurança

O sistema utiliza consultas SQL parametrizadas para reduzir riscos de injeção SQL.

Esta versão foi desenvolvida com foco acadêmico e local. Por isso, ainda não possui autenticação de usuários, criptografia de senhas ou controle de permissões.

## Melhorias Futuras

- Cadastro e login de usuários.
- Relatórios por matéria.
- Filtros por data e matéria.
- Gráficos de desempenho.
- Exportação de relatórios em PDF.
- Configuração personalizada da meta semanal.
- Deploy em ambiente de produção.
- Melhorias na responsividade para dispositivos móveis.

## Autor

GABRIEL LETÁCIO
202402398164

Projeto desenvolvido para a disciplina de Desenvolvimento Rápido em Python

Professor: Anderson Bispo.