# API para Concursos do Governo 2026

Esta API é uma réplica, para fins de estudo e desenvolvimento, de um sistema de candidatura a concursos públicos do Governo de Angola.

O projeto foi desenvolvido com uma arquitetura organizada e modular, separando as responsabilidades da aplicação em diferentes módulos e pastas. O sistema também implementa autenticação e autorização utilizando **JWT**, além de utilizar **bcrypt** para o hashing e a verificação segura de senhas.

## Entidades principais

O sistema é composto pelas seguintes entidades:

1. **User** — representa os usuários do sistema e é responsável pelos dados relacionados à autenticação e acesso.
2. **Candidato** — representa os candidatos que participam dos concursos.
3. **Candidatura** — representa a candidatura de um candidato a um determinado concurso.
4. **Concurso** — representa os concursos públicos disponíveis para candidatura.

## Tecnologias e ferramentas

* **FastAPI** — utilizado para a criação da API, endpoints e rotas.
* **SQLAlchemy** — utilizado para a definição dos modelos, relacionamentos e interação com o banco de dados SQL.
* **bcrypt** — utilizado para realizar o hashing e a verificação segura das senhas.
* **PyJWT** — utilizado para criação, codificação e validação de tokens JWT durante o processo de autenticação e autorização.
* **FPDF** — utilizado para a geração de relatórios em formato PDF.

## Arquitetura

O projeto segue uma organização modular, separando as diferentes responsabilidades da aplicação. A estrutura do projeto está organizada de forma semelhante a:

```text
api_para_concursos_do_governo2026/
│
├── src/
│   └── app/
│       ├── models/
│       ├── schemas/
│       ├── routes/
│       ├── database/
│       └── main.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Autenticação e segurança

* **bcrypt** → proteção e verificação das senhas;
* **JWT** → identificação do usuário autenticado e controle de acesso aos endpoints protegidos.
