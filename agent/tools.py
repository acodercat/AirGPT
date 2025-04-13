from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from langchain_core.callbacks.manager import AsyncCallbackManagerForToolRun
from typing import Any, Optional
from IPython import InteractiveShell
from IPython.utils.capture import capture_output


class _PythonREPLToolInput(BaseModel):
    code_snippets: str = Field(
        ..., description="The python code to execute to analyse data."
    )


class PythonREPLTool(BaseTool):
    name: str = "python_repl_tool"
    description: str = """
        "A IPython shell. Use this to execute python code. "
        "This is an IPython environment with a pre-built SQLAlchemy engine. Do not create a new SQLAlchemy engine. You can also use pandas for further data analysis."
    """
    return_direct: bool = False
    args_schema: Type[BaseModel] = _PythonREPLToolInput
    ipython_shell: InteractiveShell = Field(..., exclude=True)

    def __init__(self, ipython_shell: InteractiveShell, **kwargs: Any) -> None:
        super().__init__(ipython_shell=ipython_shell, **kwargs)

    def _run(
        self,
        code_snippets: str,
    ) -> str:
        """Use the tool."""
        try:
            with capture_output() as output:
                self.ipython_shell.run_cell(code_snippets)
            return output.stdout
        except Exception as e:
            return repr(e)

    async def _arun(
        self,
        code_snippets: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        """Use the tool asynchronously."""
        return self._run(code_snippets)