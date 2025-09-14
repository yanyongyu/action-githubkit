import ast
import logging
from types import CodeType

FILE_NAME = "<script>"

logger = logging.getLogger(__name__)


def parse_script(script: str) -> CodeType:
    try:
        script_stmts = ast.parse(
            script, filename=FILE_NAME, mode="exec", type_comments=True
        ).body
    except Exception:
        logger.exception("Fail to parse script")
        raise

    # transform script statements into module
    script_func = ast.AsyncFunctionDef(
        name="_user_script", args=ast.arguments(), body=script_stmts
    )

    module_ast = ast.Module(body=[script_func], type_ignores=[])

    return compile(module_ast, filename=FILE_NAME, mode="exec")


def run_script(
    script: CodeType,
    globals: dict[str, object] | None = None,
    locals: dict[str, object] | None = None,
):
    exec(script, globals, locals)
