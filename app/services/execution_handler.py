import logging
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi import UploadFile
from latex import LatexBuildError
from typing import List, Optional, Text, Iterator

from app.services.pdf_builder import PdfLatexBuilder
from app.settings.globals import PDFLATEX_PATH, DEBUG_LOG_RENDERED_TEX, PDF_WORKSPACE_BASE


class PdfExecutionHandler(object):
    """
    Execution handler for handling the execution.

    1. will receive tex file as text
    2. will receive list of media files as UploadFiles (file-like object)
    3. Will create an execution environment (tempdir)
    4. Will writeout the tex and media
    5. Will execute the PDFLatex
    6. Will perform error handling
    7. Will return pdf as bytestream
    """

    workspace_base: Path = PDF_WORKSPACE_BASE

    def __init__(self, tex: Text, media: Optional[List[UploadFile]]):
        self.tex: Text = tex
        self.media: Optional[List[UploadFile]] = media

        self.built_pdf: Optional[Iterator[bytes]] = None
        self.workspace_tempdir: TemporaryDirectory = TemporaryDirectory(
            dir=self.workspace_base
        )
        self.workspace = Path(self.workspace_tempdir.name)

        self.pdf_builder: PdfLatexBuilder = PdfLatexBuilder(
            pdflatex=str(PDFLATEX_PATH), tempdir=self.workspace_tempdir
        )

    def execute(self) -> Iterator[bytes]:
        """
        Call the initialized Execution Handler.
        """
        self.pre_process()
        self.build()
        self.post_process()
        return self.built_pdf

    def pre_process(self):
        """
        Pre processes the workspace

        - put all the media in the workspace.
        """
        if self.media:
            for media_file in self.media:
                # create new media file with filename and write the uploaded files to disk
                with self.workspace.path(media_file.filename).open(
                        mode="wb"
                ) as saved_file:
                    shutil.copyfileobj(media_file.file, saved_file)

    def build(self):
        """
        Perform the actual build
        """

        try:
            self.built_pdf = self.pdf_builder.build_pdf(self.tex)
        except LatexBuildError as e:
            logging.error(f"Latex Build Error: {e}")
            logging.error(
                f"TEX FILE: \n-------------\n{self.tex}\n-------------")

        if DEBUG_LOG_RENDERED_TEX:
            logging.info(
                f"TEX FILE: \n-------------\n{self.tex}\n-------------")

    def post_process(self):
        """
        Post Process the exeution

        - clean out all temp dirs
        """
        self.workspace_tempdir.cleanup()
