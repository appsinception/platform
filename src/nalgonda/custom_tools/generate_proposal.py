from agency_swarm import BaseTool
from nalgonda.custom_tools.utils import get_chat_completion
from pydantic import Field

USER_PROMPT_PREFIX = "Please draft a proposal for the following project brief: "
SYSTEM_MESSAGE = """\
You are a professional proposal drafting assistant. \
Do not include any actual technologies or technical details into proposal unless \
specified in the project brief. Be concise.\
"""


class GenerateProposal(BaseTool):
    """Generate a proposal for a project based on a project brief.
    Remember that user does not have access to the output of this function.
    You must send it back to him after execution."""

    project_brief: str = Field(..., description="The project brief to generate a proposal for.")

    def run(self) -> str:
        user_prompt = self.get_user_prompt()
        message = get_chat_completion(
            user_prompt=user_prompt,
            system_message=SYSTEM_MESSAGE,
            temperature=0.6,
        )

        return message

    def get_user_prompt(self):
        return f"{USER_PROMPT_PREFIX}\n{self.project_brief}"