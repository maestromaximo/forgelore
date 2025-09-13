from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field
from agents import Agent

from ...initial_research_agents.tools import get_paper, list_literature, list_hypotheses


COMPILATION_INSTRUCTIONS = """
You are the Compilation Agent. Given the full project context, propose diffs (small, targeted changes) to the paper content to improve it based on hypotheses outcomes and literature.

Output a list of diffs. Each diff should specify a target marker (e.g., a section header or a unique snippet to replace), and the replacement text. Keep diffs small and focused.
"""


class PaperDiff(BaseModel):
    target: str = Field(description="A unique snippet or section header to match in content_raw")
    replacement: str = Field(description="Text to replace the target with")


class CompilationPlan(BaseModel):
    diffs: List[PaperDiff]


compilation_agent = Agent(
    name="paper_compilation",
    model="gpt-4.1",
    instructions=COMPILATION_INSTRUCTIONS,
    tools=[get_paper, list_literature, list_hypotheses],
    output_type=CompilationPlan,
)


