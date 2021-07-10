import tempfile
from contextlib import redirect_stdout
from dataclasses import dataclass
from typing import List, Union

from flake8.api import legacy as flake8


@dataclass
class LintResult:
    """A Dataclass that represents a linting error (flake8)"""

    filename: str
    line: str
    character: str
    error_msg: str


def lint_file_flake8(filename: str) -> Union[List[LintResult], None]:
    """
    Lints the file `filename`, and returns a list of LintResults containg all of the linting errors.

    If no error found returns None.
    """

    style_guide = flake8.get_style_guide()
    temporary_file = tempfile.TemporaryFile(mode="r+")
    with redirect_stdout(temporary_file):
        style_guide.input_file(filename)
        temporary_file.seek(0)
    linting_errors = temporary_file.readlines()
    temporary_file.close()
    if not linting_errors:
        return None
    else:
        errors = []
        for error in linting_errors:
            current_error = error.replace("\n", "").split(":")
            errors.append(
                LintResult(
                    filename=current_error[0],
                    line=current_error[1],
                    character=current_error[2],
                    error_msg=current_error[3],
                )
            )
    return errors
