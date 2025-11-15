# base-bank

> An API developed with FastAPI to manage users, JWT authentication, Pix keys, and financial transactions.

## About the Project

This project is a financial API that includes user registration, login/logout, Pix key creation, and transactions between users using Pix. It is designed to be a scalable and secure backend system for financial applications.

The project is fully containerized using Docker, with backend services managed by FastAPI and asynchronous tasks handled by Celery with Redis.

## Tech Stack

The main technologies and libraries used in this project are:

*   **Backend:** [Python](https://www.python.org/), [FastAPI](https://fastapi.tiangolo.com/), [SQLAlchemy](https://www.sqlalchemy.org/), [Celery](https://docs.celeryq.dev/)
*   **Database:** [PostgreSQL](https://www.postgresql.org/), [Redis](https://redis.io/)
*   **Frontend:** [React](https://react.dev/)
*   **Authentication:** [JSON Web Tokens (JWT)](https://jwt.io/)
*   **Containerization:** [Docker](https://www.docker.com/)

## Usage

Below are the instructions for you to set up and run the project locally.

### Prerequisites

You need to have the following software installed to run this project:

*   [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)

### Installation and Setup

Follow the steps below:

1.  **Clone the repository**
    ```bash
    git clone https://github.com/luizvilasboas/base-bank.git
    ```

2.  **Navigate to the project directory**
    ```bash
    cd base-bank
    ```

3.  **Run services with Docker Compose**
    This command will start all services, including 3 instances of the backend for scalability.
    ```bash
    docker compose up --scale backend=3 -d
    ```

### Configuration

Before running the project, ensure you have a properly configured environment. Key environment variables include `DB_URL`, `JWT_SECRET_KEY`, `JWT_REFRESH_SECRET_KEY`, `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`, and `REDIS_URL`.

### Workflow

1.  **Access the Web Interface:**
    Open your browser and navigate to `http://127.0.0.1:3000`

2.  **Access the Interactive API Documentation:**
    Open your browser and navigate to `http://127.0.0.1/docs`

## Key Endpoints

-   `/auth/register`: Register a new user.
-   `/auth/login`: Log in and receive access/refresh tokens.
-   `/auth/logout`: Log out and invalidate the access token.
-   `/pix/create`: Create a new Pix key.
-   `/transaction/create`: Create a new transaction between users.

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
