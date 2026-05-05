# Real-Time Face Detection Streaming System

Monorepo for a containerized system with:
- `backend/` (FastAPI, face detection pipeline, ROI API)
- `frontend/` (React viewer for stream + ROI data)
- `postgres` (ROI persistence)

## Quick Start (Chunk 0 Baseline)

### Prerequisites
- Docker + Docker Compose

### Run
```bash
docker compose up --build
```

### Expected local services
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- Postgres: `localhost:5432`

## Current Status

This setup is a baseline scaffolding for the assignment chunks.
Core API/streaming logic is implemented in later chunks.

## Repo Layout

```text
.
├── backend/
├── frontend/
├── docs/
├── docker-compose.yml
└── TASK_CHUNKS.md
```

## Next Step

Proceed to **Chunk 1** in `TASK_CHUNKS.md` to implement backend route contracts.
