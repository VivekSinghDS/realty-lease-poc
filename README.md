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

### Notes
- Dockerfile: Ensure your container starts the app binding to `0.0.0.0` and uses `$PORT` provided by Render.
- Plan: `free` is suitable for testing; consider higher plans for production.
- Response format: endpoints return `response.output_text` (string). If clients expect a JSON object, parse/validate before returning.


