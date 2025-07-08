import os
import tempfile
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
import boto3
from pydantic import BaseModel
from config import settings
from extraction import service as extraction_service
from fastapi.middleware.cors import CORSMiddleware
from logger import logger
import os


app = FastAPI()
s3 = boto3.client("s3")

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://spyderweb.vercel.app",
    "https://www.spydr.dev",
    "https://spydr.dev",
    "https://api.spydr.dev",
    "https://vercel.spydr.dev",
    "https://spydrweb-git-feature-farouk-adelekes-projects.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConvertToMarkdownPayload(BaseModel):
    file_key: str


class BaseException(HTTPException):
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(status_code=status_code, detail=message)


class PyMuPDFProException(BaseException):
    def __init__(self):
        super().__init__(message="PyMuPDFPro exception", status_code=500)


class FileDownloadException(BaseException):
    def __init__(self, message: str):
        super().__init__(message=f"File download exception: {message}", status_code=500)


@app.post("/api/v1/convert")
def convert_to_markdown(payload: ConvertToMarkdownPayload):
    try:
        filename = os.path.basename(payload.file_key)
        path = os.path.join(tempfile.gettempdir(), filename)
        
        logger.error(f"FILE PATH: {path}")
        logger.error(f"FILE KEY: {payload.file_key}")

        try:
            s3.download_file(settings.s3_bucket_name, payload.file_key, path)
        except Exception as e:
            logger.error(f"FILE DOWNLOAD FAILED: {str(e)}")
            raise FileDownloadException(message=str(e))
        
        logger.error(f"FILE DOWNLOADED: {path}")
        try:
            data = extraction_service.extract(path)
            logger.error(f"EXTRACTION SERVICE SUCCESS: {str(data)}")
            return JSONResponse(content={"result": data})
        except Exception as e:
            logger.error(f"EXTRACTION SERVICE FAILED: {str(e)}")
            raise PyMuPDFProException()
        finally:
            logger.error(f"FILE REMOVED: {path}")
            os.remove(path)

    except Exception as e:
        logger.error(f"CONVERT TO MARKDOWN FAILED: {str(e)}")
        raise BaseException(message=str(e))


@app.get("/health")
def health():
    return JSONResponse(content={"status": "ok"})


@app.get("/")
def root():
    return JSONResponse(content={"status": "ok"})
