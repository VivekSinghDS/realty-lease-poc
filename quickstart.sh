#!/usr/bin/env bash
set -euo pipefail

# Quickstart script to run the FastAPI app locally on Linux
# - Creates a Python venv in .venv
# - Installs dependencies
# - Sets minimal env vars
# - Starts the app with uvicorn

PYTHON_BIN="python3"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "python3 not found. Please install Python 3.11+" >&2
  exit 1
fi

if [ ! -d ".venv" ]; then
  "$PYTHON_BIN" -m venv .venv
fi

source .venv/bin/activate
python -m pip install --upgrade pip >/dev/null
pip install -r requirements.txt

# Environment: set defaults only if absent
: "${OPENAI_API_KEY:=}"
if [ -z "$OPENAI_API_KEY" ]; then
  echo "WARNING: OPENAI_API_KEY not set. Set it to enable LLM calls." >&2
fi

export LLM=${LLM:-'{"provider":"openai"}'}
export ENVIRONMENT=${ENVIRONMENT:-development}

echo "Starting app on http://127.0.0.1:8000"
exec uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload


