backend only:
docker compose -f docker-compose.backend.yml up --build

full stack on localhost:80:
docker compose up --build frontend

frontend dev mode on localhost:5173:
docker compose --profile dev up --build backend frontend_dev
