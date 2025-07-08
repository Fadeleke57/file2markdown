from pydantic import BaseModel
import pymupdf.pro
import pymupdf4llm
from config import settings
from logger import logger


class ExtractionService(BaseModel):
    def __init__(self):
        pymupdf.pro.unlock(settings.pymupdf_license)
        logger.error("EXTRACTION SERVICE INITIALIZED!")

    def extract(self, file_path: str) -> list[dict]:
        data = pymupdf4llm.to_markdown(
            doc=file_path,
            page_chunks=True,
        )
        data = [{"page": page + 1, "text": content["text"]} for page, content in enumerate(data)]
        logger.error(f"EXTRACTION SERVICE SUCCESS: {str(data)}")
        return data


service = ExtractionService()
