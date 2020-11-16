from typing import List, Optional, Dict, Union, Text

from fastapi import APIRouter, Form, UploadFile
from fastapi.responses import StreamingResponse
from starlette.datastructures import UploadFile as StarletteUploadFile

from app.services.pdf_execution_handler import PdfExecutionHandler

router = APIRouter()


@router.post("/pdf", name="pdf")
# async def pdf_create(body: PDFCreateIn, files: Optional[List[UploadFile]]=[File(...)]) -> StreamingResponse:
async def create_pdf(
    tex: Union[Text, UploadFile] = Form(...), media: Optional[List[UploadFile]] = list()
) -> Union[Dict, StreamingResponse]:
    """
    Create a PDF.
    """
    if isinstance(tex, StarletteUploadFile) and tex.content_type in (
        "text/plain",
        "application/octet-stream",
    ):
        content = await tex.read()
        await tex.close()
        tex = content

    pdf = PdfExecutionHandler(tex=tex, media=media).execute()
    if pdf:
        return StreamingResponse(content=pdf.stream, media_type="application/pdf")

    response = dict(incoming_tex=tex)
    if media:
        for file in media:
            print(file.filename)
        response["media_filenames"] = [f.filename for f in media]

    print(f"{response=}")
    return response  # StreamingResponse(test_pdf.open(mode='rb'))
