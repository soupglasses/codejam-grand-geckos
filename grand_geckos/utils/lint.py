import io
import os
from contextlib import redirect_stdout
from dataclasses import dataclass
from tempfile import NamedTemporaryFile
from typing import List, Union

from flake8.api import legacy as flake8


@dataclass
class LintResult:
    """A Dataclass that represents a linting error (flake8)"""

    line: int
    pos: int
    error: str
    message: str


def lint_code(code: str) -> Union[List[LintResult], List[None]]:
    """
    Lints the `code` string as if it would have been a python file.

    Returns a list of LintResults containg linting errors. If no errors are
    found, it returns an empty list.

    NOTE: This is a hacky solution, as we arecreating and deleting files under
    `/tmp`. But since the api only allows us to invoke the linter by giving it
    a file on disk, there is no way around it.
    """

    style_guide = flake8.get_style_guide(ignore=["W292"])

    with NamedTemporaryFile("w", encoding="utf-8", delete=False) as tmp_file:
        tmp_file.write(code)

    with io.StringIO() as buf, redirect_stdout(buf):
        style_guide.input_file(tmp_file.name)
        lint_errors = buf.getvalue()

    os.remove(tmp_file.name)

    errors = []
    for error in lint_errors.splitlines():
        _, line, pos, err_msg = error.split(":", 4)
        err, msg = err_msg[1:].split(" ", 1)
        errors.append(
            LintResult(
                line=int(line),
                pos=int(pos),
                error=err,
                message=msg,
            )
        )
    return errors
