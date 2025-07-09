# 📝 fadeleke57-file2markdown

A lightweight FastAPI microservice that downloads files from AWS S3, extracts their contents using `PyMuPDFPro`, and returns Markdown chunks per page—ready for AI pipelines, note-taking tools, or searchable memory systems.

---

## 🚀 Features

- 🔐 S3 integration for secure file downloads  
- 📄 PDF-to-Markdown conversion with per-page chunking using `pymupdf4llm`  
- 🧠 Fine-tuned for AI preprocessing and document memory stores  
- 🐳 Dockerized for production environments  
- ⚡ FastAPI-powered with CORS enabled for cross-origin access  
- 🔥 Plug-and-play endpoint: just provide an S3 key!

---

## 🗂️ Directory Structure

```
fadeleke57-file2markdown/
├── __init__.py
├── config.py              # Pydantic settings for env vars
├── docker-compose.yml     # Docker Compose config
├── Dockerfile             # Container setup
├── extraction.py          # PDF → Markdown conversion logic
├── logger.py              # Centralized logger
├── main.py                # FastAPI entry point with endpoints
├── Makefile               # Dev shortcuts
├── requirements.txt       # Python dependencies
└── .dockerignore          # Ignore files from Docker context
```

---

## ⚙️ Environment Setup

### 1. **Required Environment Variables**

Create a `.env` file in the root directory with the following:

```env
S3_BUCKET_NAME=your-s3-bucket-name
PYMUPDF_LICENSE=your_pymupdfpro_license_key
```

> 🔒 Make sure `.env` is **never** committed — it's included in `.dockerignore`.

---

## 🐳 Docker Setup

### 🔧 Build & Run (Docker Compose)

```bash
make docker-start
```

Visit `http://localhost:4000/health` to confirm it's running.

### 🛑 Stop Containers

```bash
make docker-stop
```

---

## 🧪 Local Development

### ▶️ Run Server Locally

```bash
make start
```

> This uses `uvicorn` with hot-reloading on port `4000`.

---

## 📬 API Endpoints

### ✅ Health Check

```http
GET /health
```

Returns:
```json
{ "status": "ok" }
```

---

### 📥 Convert to Markdown

```http
POST /api/v1/convert
```

#### Payload:

```json
{
  "file_key": "path/to/your.pdf"
}
```

- Downloads the file from S3 using `file_key`
- Extracts markdown content per page
- Returns JSON with page-level Markdown

#### Response:

```json
{
  "result": [
    { "page": 1, "text": "# Page 1 content..." },
    { "page": 2, "text": "# Page 2 content..." }
  ]
}
```

#### Possible Errors:
- `500` - PyMuPDFPro error
- `500` - File download failure

---

## 📦 Dependencies

```txt
fastapi
uvicorn
boto3
pymupdf4llm
pymupdfpro
pymupdf
pydantic-settings
pydantic
```

---

## 🐍 Python Version

- Python 3.9.6 (enforced in Docker)

---

## 🔍 Logging

All logs are centralized via `logger.py` and emitted in the format:

```
[LEVEL] filename:function: message
```

Errors from S3 downloads, extraction, and file cleanup are surfaced for easier debugging.

---

## 🧱 Tech Stack

- **FastAPI** – REST API
- **PyMuPDFPro** – PDF content access
- **pymupdf4llm** – Page-level Markdown extraction
- **Boto3** – AWS S3 interaction
- **Docker** – Deployment-ready containerization

---

## 📌 TODO

- [ ] Add support for other file types (e.g., .docx)
- [ ] Add authentication or API key protection
- [ ] Unit tests with `pytest`
- [ ] Upload output to S3 or return as a downloadable file

---

## 👨‍💻 Author

Built with 💡 by [fadeleke57](https://github.com/fadeleke57)
