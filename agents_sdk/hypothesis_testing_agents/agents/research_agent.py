from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field
from agents import Agent

from ...initial_research_agents.tools import literature_search, list_literature, read_literature


RESEARCHER_INSTRUCTIONS = """
You are the Hypothesis Research Agent. For a given hypothesis, gather background information:
- Use your tools to search and read relevant literature
- Produce a concise background summary focused on evaluating the hypothesis
Avoid fabricating sources.
"""


class HypothesisResearch(BaseModel):
    background_summary: str = Field(description="Synthesis of evidence relevant to the hypothesis")


research_agent = Agent(
    name="hypothesis_researcher",
    model="gpt-4.1",
    instructions=RESEARCHER_INSTRUCTIONS,
    tools=[literature_search, list_literature, read_literature],
    output_type=HypothesisResearch,
)


