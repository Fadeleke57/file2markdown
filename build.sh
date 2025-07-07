#!/usr/bin/env bash
set -e
echo "📦 Starting build..."

# Confirm Python version and ensure pip is available
python3.9 --version
python3.9 -m ensurepip  # ensures pip is installed  [oai_citation:2‡medium.com](https://medium.com/%40emusyoka759/hosting-a-django-application-on-vercel-a-step-by-step-guide-9cf33e2a1ecf?utm_source=chatgpt.com) [oai_citation:3‡plus.diolinux.com.br](https://plus.diolinux.com.br/t/deploy-no-site-vercel-com-erro-pip-not-found/61285?utm_source=chatgpt.com)

# Virtual environment (optional if you need venv isolation)
python3.9 -m venv venv
source venv/bin/activate

# Install dependencies
python3.9 -m pip install --upgrade pip
python3.9 -m pip install -r requirements.txt

uvicorn main:app --host 0.0.0.0 --port 8000

echo "✅ Build complete!"