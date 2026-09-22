## 💰 Sistema de Controle Financeiro

Sistema de Controle Financeiro é um sistema desktop de controle financeiro desenvolvido em Python, com o objetivo de facilitar o gerenciamento de contas,
movimentações e investimentos em uma única aplicação.

O projeto combina Python, SQL e uma interface gráfica,utilizando banco de dados para armazenar as informações e
gráficos para apresentar indicadores financeiros de forma visual.

## 📌 Funcionalidades

### 📊 Visão geral

- Visualização do saldo total das contas;
- Resumo de entradas e saídas;
- Análise dos gastos por categoria;
- Acompanhamento dos investimentos;
- Visualização gráfica das informações financeiras.

### 🏦 Contas bancárias

- Cadastro de contas;
- Associação da conta a diferentes instituições financeiras;
- Controle de saldo;
- Ativação e desativação de contas;
- Exclusão de contas respeitando regras de integridade dos dados.

### 💸 Movimentações

- Registro de entradas e saídas;
- Classificação das movimentações por categoria;
- Registro da data da movimentação;
- Validação de saldo disponível;
- Consulta do histórico financeiro.

### 🔄 Transferências
- Transferência de valores entre contas;
- Validação das contas de origem e destino;
- Verificação de saldo disponível;
- Atualização dos saldos após a transferência.

### 📈 Investimentos
- Cadastro de investimentos;
- Classificação por categoria;
- Registro do valor investido;
- Registro da data;
- Acompanhamento da evolução dos investimentos;
- Análise dos investimentos por categoria.


## 🛠️ Tecnologias

Tecnologia |	Utilização

Python	--> Lógica da aplicação e regras de negócio

SQL	  -->  Estrutura e consultas do banco de dados

SQLite	-->  Armazenamento local dos dados

SQLModel  -->	Modelagem das entidades e interação com o banco

PySide6	--> Construção da interface gráfica

Matplotlib -->	Criação dos gráficos e visualizações

Git/GitHub -->	Versionamento e hospedagem do projeto

## 📚 Bibliotecas utilizadas

- PySide6:

Utilizada para construir a interface gráfica da aplicação, incluindo janelas, menus, formulários, tabelas, botões e componentes de navegação.

- SQLModel:

Utilizada para estruturar os modelos de dados e realizar a comunicação entre a aplicação Python e o banco SQLite.

- Matplotlib:

Utilizada para gerar os gráficos presentes na área de análise financeira.

- Bibliotecas padrão do Python

O projeto também utiliza recursos nativos do Python, como:

 - datetime — manipulação de datas;
 - enum — criação de categorias e estados padronizados;
 - sys — recursos relacionados à execução da aplicação.

## 🗄️ Banco de dados

O sistema utiliza SQLite como banco de dados local.

A estrutura possui entidades para:

- Contas
- Histórico de movimentações
- Investimentos

As movimentações possuem relacionamento com suas respectivas contas, permitindo manter o histórico financeiro associado a cada instituição.

🏗️ Estrutura do projeto
Financeiro/
│

├── main.py          # Interface gráfica e execução da aplicação

├── models.py        # Modelos e estrutura do banco de dados

├── viwer.py         # Operações e consultas relacionadas aos dados

├── database.db      # Banco de dados SQLite

├── main.spec        # Configuração para geração do executável

│

├── build/            # Arquivos gerados durante o processo de build

└── dist/             # Aplicação compilada

## ▶️ Como executar
1. Clone o repositório
git clone https://github.com/abrahaoantonio/Financeiro.git
2. Entre na pasta
cd Financeiro
3. Instale as dependências
pip install PySide6 SQLModel matplotlib
4. Execute a aplicação
python main.py

O banco de dados database.db é utilizado pela aplicação para armazenar as informações financeiras.

## 💡 Principais desafios do projeto

Durante o desenvolvimento, alguns pontos exigiram maior atenção, principalmente a integração entre a interface gráfica, as regras de negócio e o banco de dados.

Entre eles:
 - Estruturação das entidades e relacionamentos;
 - Persistência dos dados utilizando SQLite;
 - Validação das operações financeiras;
 - Controle de saldo durante entradas, saídas e transferências;
 - Organização do código em diferentes módulos;
 - Transformação dos dados armazenados em informações visuais por meio de gráficos. 

