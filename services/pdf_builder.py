"""
The following section is copied with alterations (arguments passed to the pdflatex for more robust operation)

Original package:
Name: latex
Version: 0.6.4
Summary: Wrappers for calling LaTeX/building LaTeX documents.
Home-page: http://github.com/mbr/latex
Author: Marc Brinkmann
Author-email: git@marcbrinkmann.de
License: MIT
"""
import os
import subprocess

from data import Data as I
from data.decorators import data
from future.utils import raise_from
from latex.build import LatexBuilder
from latex.exc import LatexBuildError
from shutilwhich import which
from tempdir import TempDir


class PdfLatexBuilder(LatexBuilder):
    """A simple pdflatex based buidler for LaTeX files.

    Builds LaTeX files by copying them to a temporary directly and running
    ``pdflatex`` until the associated ``.aux`` file stops changing.

    .. note:: This may miss changes if ``biblatex`` or other additional tools
              are used. Usually, the :class:`~latex.build.LatexMkBuilder` will
              give more reliable results.

    :param pdflatex: The path to the ``pdflatex`` binary (will looked up on
                    ``$PATH``).
    :param max_runs: An integer providing an upper limit on the amount of times
                     ``pdflatex`` can be rerun before an exception is thrown.
    """

    def __init__(self, pdflatex="pdflatex", max_runs=15):
        self.pdflatex = pdflatex
        self.max_runs = 15

    @data("source")
    def build_pdf(self, source, texinputs=[]):
        with TempDir() as tmpdir, source.temp_saved(suffix=".latex", dir=tmpdir) as tmp:

            # close temp file, so other processes can access it also on Windows
            tmp.close()

            # calculate output filename
            base_fn = os.path.splitext(tmp.name)[0]
            output_fn = base_fn + ".pdf"
            aux_fn = base_fn + ".aux"
            args = [
                self.pdflatex,
                "-interaction=nonstopmode",
                "-file-line-error",
                tmp.name,
                "-output-format",
                "pdf",
            ]

            # create environment
            newenv = os.environ.copy()
            newenv["TEXINPUTS"] = os.pathsep.join(texinputs) + os.pathsep

            # run until aux file settles
            prev_aux = None
            runs_left = self.max_runs
            while runs_left:
                # try:
                with open(os.devnull, "r") as devnull_r_fd, open(
                    os.devnull, "w"
                ) as devnull_w_fd:
                    execution_result = subprocess.run(
                        args,
                        cwd=tmpdir,
                        env=newenv,
                        stdin=devnull_r_fd,
                        stdout=devnull_w_fd,
                    )
                # except CalledProcessError as e:
                #     raise_from(LatexBuildError(base_fn + '.log'), e)

                # check aux-file
                with open(aux_fn, "rb") as auf_fd:
                    aux = auf_fd.read()

                if aux == prev_aux:
                    break

                prev_aux = aux
                runs_left -= 1
            else:
                raise RuntimeError(
                    "Maximum number of runs ({}) without a stable .aux file "
                    "reached.".format(self.max_runs)
                )

            if not os.path.exists(output_fn) and not os.stat(output_fn).st_size:
                # KEW: alterative way of checking if output is there instead of calledproc error
                raise_from(LatexBuildError(base_fn + ".log"), aux)

            with open(output_fn, "rb") as fd:
                bin_output_fn = fd.read()
            return I(bin_output_fn, encoding=None)

    def is_available(self):
        return bool(which(self.pdflatex))
