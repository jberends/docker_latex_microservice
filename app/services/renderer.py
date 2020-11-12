import logging
import os

from latex import LatexBuildError
from latex.jinja2 import make_env
from jinja2 import FileSystemLoader

from config import PDFLATEX_PATH, DEBUG_LOG_RENDERED_TEX
from .pdf_builder import PdfLatexBuilder
from .utils import (
    filter_ellipsis_on_longtext,
    filter_no_newline,
    filter_squash_whitespace,
)

__latex_env = None

# TODO: move to app template stuff settings things
LATEX_TEMPLATE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "templates")
)


def get_latex_env():
    """Latex rendering environment singleton."""
    global __latex_env
    if not __latex_env:
        __latex_env = make_env(loader=FileSystemLoader(LATEX_TEMPLATE_PATH))
        __latex_env.filters["ellipsis"] = filter_ellipsis_on_longtext
        __latex_env.filters["no_newline"] = filter_no_newline
        __latex_env.filters["squash_whitespace"] = filter_squash_whitespace
    return __latex_env


def render_latex_to_pdf(context, template_filename="main.tex", return_tex=False):
    """
    Render content dict to a template, return the rendered response as a pdf bytestream.

    :param context: dictionary with content to render
    :param template_filename: name of the template file
    :param return_tex: (default false) if true, return a tuple with teh rendered_pdf and rendered_template string
    :return: rendered_pdf (the actual bytestream is in rendered_pdf.data)
    """
    latex_env = get_latex_env()
    template = latex_env.get_template(template_filename)

    rendered_template = template.render(**context)
    rendered_pdf = None

    # instantiate the pdf builder (in production we use texlive distrbution from CTAN, local dev is from ubuntu)
    pdf_builder = PdfLatexBuilder(pdflatex=PDFLATEX_PATH)

    try:
        rendered_pdf = pdf_builder.build_pdf(rendered_template)
    except LatexBuildError as e:
        logging.error("Latex Build Error: {}".format(e))
        logging.error(
            "TEX FILE: \n------------------\n{}\n------------------".format(
                rendered_template
            )
        )

    if DEBUG_LOG_RENDERED_TEX:
        logging.error(
            "TEX FILE: \n------------------\n{}\n------------------".format(
                rendered_template
            )
        )

    if return_tex and rendered_pdf:
        return rendered_pdf, rendered_template
    elif rendered_pdf:
        return rendered_pdf
    else:
        return None
