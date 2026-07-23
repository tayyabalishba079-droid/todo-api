# Todo API (Dockerized FastAPI with PostgreSQL)

A fully containerized FastAPI task management service integrated with PostgreSQL and environment configuration management via `.env`.

## Architecture & Docker Setup

- **Database:** PostgreSQL running in a dedicated Docker container (`postgres:15-alpine`).
- **Containerization:** Orchestrated via `docker-compose.yml`.
- **Data Persistence:** Managed using a named Docker volume (`postgres_data`) ensuring data survives container restarts.
- **Environment Variables:** Connection parameters loaded dynamically from `.env` (`.env.example` committed for reference).

## Running the Application Stack

Start the entire application and database with a single command:

```bash
docker compose up --build