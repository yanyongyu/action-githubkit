import ast
import logging
from types import CodeType
from typing import Any

FILE_NAME = "<script>"
SCRIPT_FUNC_NAME = "_user_script"
MAIN_FUNC_NAME = "_main"

logger = logging.getLogger(__name__)


def parse_script(script: str) -> CodeType:
    """Parse and wrap input script into a coroutine function.

    Args:
        script (str): The script to parse.

    Returns:
        CodeType: The compiled code object to run the given script.
    """

    try:
        script_stmts = ast.parse(
            script, filename=FILE_NAME, mode="exec", type_comments=True
        ).body
    except Exception:
        logger.exception("Fail to parse script")
        raise

    preload_stmts = [
        ast.Import(
            names=[ast.alias(name="asyncio", lineno=1, col_offset=0)],
            lineno=1,
            col_offset=0,
        )
    ]

    # transform script statements into module
    script_func = ast.AsyncFunctionDef(
        name=SCRIPT_FUNC_NAME,
        args=ast.arguments(),
        body=script_stmts,
        lineno=2,
        col_offset=0,
    )

    main_func = ast.FunctionDef(
        name=MAIN_FUNC_NAME,
        args=ast.arguments(),
        body=[
            ast.Expr(
                ast.Call(
                    func=ast.Attribute(
                        ast.Name("asyncio", ctx=ast.Load(), lineno=1, col_offset=0),
                        "run",
                        lineno=1,
                        col_offset=0,
                    ),
                    args=[
                        ast.Call(
                            func=ast.Name(
                                SCRIPT_FUNC_NAME, ctx=ast.Load(), lineno=1, col_offset=0
                            ),
                            args=[],
                            keywords=[],
                            lineno=1,
                            col_offset=0,
                        )
                    ],
                    keywords=[],
                    lineno=1,
                    col_offset=0,
                ),
                lineno=1,
                col_offset=0,
            )
        ],
        lineno=3,
        col_offset=0,
    )

    module_ast = ast.Module(
        body=[*preload_stmts, script_func, main_func], type_ignores=[]
    )

    logger.debug(f"Constructed script:\n{ast.unparse(module_ast)}")

    return compile(module_ast, filename=FILE_NAME, mode="exec")


def run_script(script: CodeType, globals: dict[str, Any] | None = None) -> None:
    ctx_globals = globals.copy() if globals is not None else {}
    logger.info(f"Running script with globals: {ctx_globals!r}")
    exec(script, ctx_globals)
    assert MAIN_FUNC_NAME in ctx_globals, "main entrypoint not found in globals"
    main = ctx_globals[MAIN_FUNC_NAME]
    assert callable(main), "main entrypoint is not callable"
    try:
        main()
    except Exception:
        logger.exception("Error occurred while running script")
        raise
    else:
        logger.info("Script execution completed.")
