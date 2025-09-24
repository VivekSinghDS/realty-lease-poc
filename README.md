## Realty Lease POC – Deployment Guide (Render)

### Overview
This repo contains a FastAPI app that processes uploaded lease PDFs and returns a structured JSON response powered by an LLM. The repo includes a Render Blueprint (`render.yaml`) that defines two web services so you can run Docker-based and Python-based deployments side by side.

### Prerequisites
- A Render account (`https://dashboard.render.com`)
- This repo pushed to a Git host (GitHub/GitLab/Bitbucket)
- Dockerfile in the repo root (your image must bind to 0.0.0.0 and `$PORT`)
- OpenAI API key (if using the default OpenAI provider)

### 1) Deploy via Render Blueprint
1. Open the dashboard: `https://dashboard.render.com`
2. New → Blueprint → select your repo/branch → Apply
3. Render will create services from `render.yaml`

The Blueprint defines two services:
- `realty-lease-poc`: env `docker` (built from your Dockerfile)
- `realty-lease-poc-python`: env `python` (uses `pip install` + `uvicorn`)

Both expose `GET /health` and share the same environment variables.

Use one or both:
- To use only one: in Render, delete/disable the other service (or set plan to Free for testing only).
- To use both: keep both services; each will have its own URL.

### 2) Configure environment variables
In Render → Service → Settings → Environment
- OPENAI_API_KEY: set your OpenAI API key (required for OpenAI)
- LLM: defaulted to `{"provider":"openai"}` in the blueprint
- ENVIRONMENT: `production` (already set in the blueprint)

Optional (only if you implement Perplexity):
- PERPLEXITY_API_KEY and switch `LLM` to `{"provider":"perplexity"}` after implementing the adapter.

### 3) Verify after deploy
- Health check:
```bash
curl -s https://<your-service>.onrender.com/health
```
- Lease abstract (upload a PDF):
```bash
curl -s -F "assets=@/path/to/lease.pdf" https://<your-service>.onrender.com/lease-abstract
```
- Amendment analysis (requires an existing original lease directory):
```bash
curl -s -F "amendment=@/path/to/lease-amendment.pdf" https://<your-service>.onrender.com/lease-abstract/amendment-analysis
```
- Lease summary (current route wiring):
```bash
curl -s -F "assets=@/path/to/lease.pdf" https://<your-service>.onrender.com/lease-summary/lease-summary
```

### 4) Local development (optional)
Run without Docker:
```powershell
$env:OPENAI_API_KEY = "sk-..."
$env:LLM = '{"provider":"openai"}'
uvicorn app.main:app --reload
```

### Quickstart (Linux/Bash)
Run locally with one command:
```bash
./quickstart.sh
```
If needed, make it executable first:
```bash
chmod +x quickstart.sh && ./quickstart.sh
```
What it does:
- Creates `.venv` and installs `requirements.txt`
- Uses `OPENAI_API_KEY` from your shell if present
- Sets `LLM` to `{\"provider\":\"openai\"}` by default
- Starts the app at `http://127.0.0.1:8000`

Swagger/OpenAPI docs:
- Open `http://127.0.0.1:8000/docs` for Swagger UI
- Open `http://127.0.0.1:8000/redoc` for ReDoc

Test locally:
```bash
curl -s http://127.0.0.1:8000/health
# Upload a PDF to lease abstraction
curl -s -F "assets=@/path/to/lease.pdf" http://127.0.0.1:8000/lease-abstract
# Upload an amendment PDF (will return 404 until the original exists)
curl -s -F "amendment=@/path/to/lease-amendment.pdf" http://127.0.0.1:8000/lease-abstract/amendment-analysis
# Upload a PDF to lease summary
curl -s -F "assets=@/path/to/lease.pdf" http://127.0.0.1:8000/lease-summary/lease-summary
```

### Notes
- Dockerfile: Ensure your container starts the app binding to `0.0.0.0` and uses `$PORT` provided by Render.
- Plan: `free` is suitable for testing; consider higher plans for production.
- Response format: endpoints return `response.output_text` (string). If clients expect a JSON object, parse/validate before returning.

### Endpoints and behavior

- `POST /lease-abstract`
  - Form field: `assets` (PDF)
  - Stores a directory named after the uploaded filename (sanitized as `fileid`).
  - Saves model output as `original_lease.json` in that directory.
  - If the directory already exists, returns a JSON response with the message "original lease abstraction already provided" and includes the existing `original_lease` content.
  - The prompt uses `DOCUMENT_NAME` as the uploaded filename and injects the expected JSON structure.

- `POST /lease-abstract/amendment-analysis`
  - Form field: `amendment` (PDF)
  - Tries to match the amendment to an existing `fileid` directory by leading name (e.g., "Bayer*").
  - If no match, returns 404 with "Please provide original lease first. Original abstraction unavailable."
  - On match, loads the latest original JSON (`original_lease.json` or highest `original_lease_<x>.json`), sends it with the amendment to the model, and saves the new output as `original_lease_<next>.json`.
  - Returns the model output text.

### Prompt variables

- `DOCUMENT_NAME`: set to the uploaded PDF’s filename (both endpoints) to prefix page-number references in the output.
- `JSON_STRUCTURE`: the base schema injected into prompts (from `utils/references/lease_abstraction.json`).


