from fastapi import APIRouter, UploadFile, Form
from fastapi.responses import StreamingResponse
from typing import List, Optional, Dict, Union

from app.services.execution_handler import PdfExecutionHandler

router = APIRouter()


@router.post("/pdf", name="pdf")
# async def pdf_create(body: PDFCreateIn, files: Optional[List[UploadFile]]=[File(...)]) -> StreamingResponse:
async def create_pdf(
    tex: str = Form(...), media: Optional[List[UploadFile]] = list()
) -> Union[Dict, StreamingResponse]:
    """
    Create a PDF.
    """
    pdf = PdfExecutionHandler(tex=tex, media=media).execute()
    if pdf:
        return StreamingResponse(content=pdf, media_type="application/pdf")

    response = dict(incoming_tex=tex)
    if media:
        for file in media:
            print(file.filename)
        response["media_filenames"] = [f.filename for f in media]

    print(f"{response=}")
    return response  # StreamingResponse(test_pdf.open(mode='rb'))
