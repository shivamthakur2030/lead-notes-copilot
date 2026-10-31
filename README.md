# Lead Notes Copilot

A backend application built with FastAPI and PostgreSQL to manage sales leads, track interactions, and analyze lead activity.

## Features

- Lead CRUD operations
- Create and retrieve lead notes
- PostgreSQL database integration
- SQLAlchemy ORM
- Search, filtering, and pagination
- Lead and notes analytics
- Input validation using Pydantic
- Automated API testing with Pytest
- Docker containerization

## Tech Stack

- Python 3
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Pytest
- Docker & Docker Compose
- Git & GitHub

## Project Structure

```text
fastapi-learning/
├── tests/
│   ├── conftest.py
│   └── test_api.py
├── main.py
├── database.py
├── models.py
├── schemas.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd fastapi-learning
```

Create a virtual environment:

```bash
python -m venv myenv
```

Activate it (Windows PowerShell):

```powershell
.\myenv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=your_postgresql_connection_url
```

Never commit your `.env` file or expose database credentials.

## Run Locally

```bash
uvicorn main:app --reload
```

API documentation:

http://127.0.0.1:8000/docs

## Run with Docker

Build the application:

```bash
docker compose build
```

Start the containers:

```bash
docker compose up -d
```

View logs:

```bash
docker compose logs -f api
```

## Run Tests

```bash
python -m pytest -v
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/leads` | Create lead |
| GET | `/leads` | List leads |
| GET | `/leads/{id}` | Retrieve lead |
| PATCH | `/leads/{id}` | Update lead |
| DELETE | `/leads/{id}` | Delete lead |
| POST | `/leads/{id}/notes` | Create note |
| GET | `/leads/{id}/notes` | Retrieve notes |
| GET | `/analytics/overview` | Lead analytics |
| GET | `/analytics/notes-per-lead` | Notes analytics |

## Future Improvements

- LLM-powered lead analysis
- AI-generated follow-up emails
- Alembic database migrations
- Authentication and authorization
- Production deployment

## Author

Shivam

Built as part of my journey toward becoming an AI Engineer.
