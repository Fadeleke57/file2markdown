import os
import tempfile
from fastapi import FastAPI
from markitdown import MarkItDown
from pypdf import PdfReader
from pydantic import BaseModel

app = FastAPI()
md = MarkItDown()
class ConvertToMarkdownPayload(BaseModel):
    file_key: str

@app.post("/convert")
def convert_to_markdown(payload: ConvertToMarkdownPayload):
    tempdir = tempfile.TemporaryDirectory()
    with open(os.path.join(tempdir.name, payload.file_key), "wb") as f:
        s3_client.download_file("", payload.file_key, f)

    data = md.convert(os.path.join(tempdir.name, payload.file_key))
    markdown = data.text_content
    return {"markdown": markdown}
