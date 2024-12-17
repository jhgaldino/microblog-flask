# Microblog Flask

Um site de microblog desenvolvido com Python, Flask, SQLite e Docker.

## Descrição

Este projeto é um exemplo de um site de microblog onde os usuários podem se registrar, fazer login, criar postagens e visualizar postagens de outros usuários.

## Requisitos

- Python 3.8+
- pip (gerenciador de pacotes do Python)
- Docker (opcional, para execução em contêiner)

## Instalação
Crie um ambiente virtual:
 ```
 python -m venv venv
 ```
Ative o ambiente virtual:

No Windows:
```
venv\Scripts\Activate.ps1
```
No Unix ou MacOS:
```
source venv/bin/activate
```
Instale as dependências:
```
pip install -r requirements.txt
```

Crie um arquivo .env na raiz do projeto e adicione suas variáveis de ambiente.

### Executando o Projeto
Executando Localmente

Inicialize o banco de dados:

```
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

Execute o aplicativo:
```
python run.py
```

