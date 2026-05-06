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
docker-compose up --build
```

### Expected local services
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- Postgres: internal Docker network (`postgres:5432`)

## Current Status

- Backend supports ingest and stream WebSockets.
- Face ROI detection is implemented without OpenCV (MediaPipe).
- ROI metadata is persisted to PostgreSQL.
- Frontend displays processed frames and ROI data.
- Dockerfiles and Compose integration are in place.

## API Contracts

- `GET /health`: backend health check.
- `GET /roi/latest`: latest ROI snapshot from PostgreSQL.
- `WS /ws/ingest`: accepts frame payloads as data URL JSON messages.
- `WS /ws/stream`: emits processed frame + ROI payloads.

Ingest message example:
```json
{
  "frame_id": 1,
  "frame": "data:image/jpeg;base64,..."
}
```

## Local Development (without Docker)

Backend:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Frontend:
```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

## Testing

Backend unit tests:
```bash
cd backend
source venv/bin/activate
pytest -q
```

Frontend build verification:
```bash
cd frontend
npm run build
```

## Troubleshooting

- If `docker-compose` fails with `address already in use` on port `5432`, keep Postgres internal-only in compose (already configured in this repo).
- If camera access fails, verify browser permission and use `http://localhost:5173`.
- If streaming is blank, verify backend health at `http://localhost:8000/health`.
- If compose crashes with legacy `ContainerConfig` bug, run:
  - `docker-compose down --remove-orphans`
  - `docker-compose up --build`

## Architecture Artifact

- Add architecture diagram file at `docs/architecture.png`.
- Include three containers: `frontend`, `backend`, and `postgres`, plus WebSocket and REST links.

## AI Attestation

AI assistance was used for:
- planning chunked delivery from the task statement,
- generating/refactoring code structure to a layered FastAPI architecture,
- implementing route/service/repository scaffolding,
- drafting tests and documentation.

All generated changes were reviewed, edited, and validated through local compile/build checks.

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

Proceed to final polish: architecture PNG export, commit grouping, and final submission checklist.
