# Real-Time Face Detection Streaming System

Monorepo for a containerized system with:
- `backend/` (FastAPI, face detection pipeline, ROI API)
- `frontend/` (React viewer for stream + ROI data)
- `postgres` (ROI persistence)

## Quick Start

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

- Backend supports ingest and stream WebSockets.
- Face ROI detection is implemented without OpenCV (MediaPipe).
- ROI metadata is persisted to PostgreSQL.
- Frontend displays processed frames and ROI data.
- Dockerfiles and Compose integration are in place.

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

Proceed to **Chunk 7** in `TASK_CHUNKS.md` for error handling and security hardening.
