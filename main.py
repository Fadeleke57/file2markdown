import os
import tempfile
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
import pymupdf4llm
import pymupdf.pro
import boto3
from pydantic import BaseModel
from config import settings

app = FastAPI()
s3 = boto3.client("s3")
pymupdf.pro.unlock()

class ConvertToMarkdownPayload(BaseModel):
    file_key: str

class BaseException(HTTPException):
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(status_code=status_code, detail=message)

class PyMuPDFProException(BaseException):
    def __init__(self):
        super().__init__(message="PyMuPDFPro exception", status_code=500)


@app.post("/api/v1/convert")
def convert_to_markdown(payload: ConvertToMarkdownPayload):
    try:
        path = os.path.join(tempfile.gettempdir(), payload.file_key)
        s3.download_file(settings.s3_bucket_name, payload.file_key, path)

        try:
            data = pymupdf4llm.to_markdown(
                doc=path,
                page_chunks=True,
            )
            markdown = data
        except Exception as e:
            raise PyMuPDFProException(message=str(e))
        finally:
            os.remove(path)

        return JSONResponse(content={"markdown": markdown})
    except Exception as e:
        raise BaseException(message=str(e))


@app.get("/health")
def health():
    return JSONResponse(content={"status": "ok"})


@app.get("/")
def root():
    return JSONResponse(content={"status": "ok"})
