# base-bank

Este projeto é uma API desenvolvida com FastAPI para gerenciar usuários, autenticação JWT, chaves Pix e transações financeiras. O projeto inclui endpoints para registro de usuários, login, logout, criação de chaves Pix, e transações entre usuários utilizando Pix.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **FastAPI**: Framework para criação da API.
- **SQLAlchemy**: ORM para interações com o banco de dados.
- **JWT (JSON Web Tokens)**: Para autenticação e autorização.
- **Pydantic**: Para validação e criação de esquemas de dados.
- **PostgreSQL**: Banco de dados utilizado.
- **Docker**: Para containerização do ambiente de desenvolvimento e produção.
- **React**: Frontend para interação com a API.

## Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://gitlab.com/olooeez/base-bank.git
   cd base-bank
   ```

2. **Suba os serviços com o Docker:**
   ```
   docker compose up --scale backend=3 -d
   ```

## Configuração

- Certifique-se de configurar as variáveis de ambiente necessárias, como `DB_URL`, `JWT_SECRET_KEY`, e `JWT_REFRESH_SECRET_KEY`.

## Uso

1. **Acesse a interface web interativa com a API:**
   - Abra o navegador e vá para: [127.0.0.1:3000](http://127.0.0.1:3000)

2. **Acesse a documentação interativa da API:**
   - Abra o navegador e vá para: [127.0.0.1/docs](http://127.0.0.1/docs)

## Endpoints Principais

- **/auth/register**: Registro de novos usuários.
- **/auth/login**: Login e obtenção de tokens de acesso e atualização.
- **/auth/logout**: Logout e invalidação do token de acesso.
- **/pix/create**: Criação de uma nova chave Pix.
- **/transaction/create**: Criação de uma nova transação entre usuários.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e merge requests para melhorias.

## Licença

Este projeto é licenciado sob a Licença MIT - veja o arquivo [LICENSE](https://gitlab.com/olooeez/base-bank/-/blob/main/LICENSE) para mais detalhes.
