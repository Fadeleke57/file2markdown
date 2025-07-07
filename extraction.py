from pydantic import BaseModel
import pymupdf.pro
import logging
import os
from fastapi.exceptions import HTTPException
import pymupdf4llm
from config import settings

logger = logging.getLogger(__name__)


class ExtractionService(BaseModel):
    def __init__(self):
        pymupdf.pro.unlock(settings.pymupdf_license)
        logger.info("EXTRACTION SERVICE INITIALIZED!")

    def extract(self, file_path: str) -> str:
        try:
            data = pymupdf4llm.to_markdown(
                doc=file_path,
                page_chunks=True,
            )
            markdown = data
            logger.info(f"EXTRACTION SERVICE SUCCESS: {str(markdown)}")

            return markdown
        except Exception as e:
            logger.error(f"EXTRACTION SERVICE FAILED: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            os.remove(file_path)


service = ExtractionService()
