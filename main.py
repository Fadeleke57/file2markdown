import os
import tempfile
from fastapi import FastAPI
from markitdown import MarkItDown
from pydantic import BaseModel  

app = FastAPI()
md = MarkItDown()
class ConvertToMarkdownPayload(BaseModel):
    file_key: str

@app.post("/convert")
def convert_to_markdown(payload: ConvertToMarkdownPayload):
    tempdir = tempfile.TemporaryDirectory()
    with open(os.path.join(tempdir.name, payload.file_key), "wb") as f:
        f.write(payload.file_key)

    data = md.convert(os.path.join(tempdir.name, payload.file_key))
    markdown = data.text_content
    return {"markdown": markdown}
