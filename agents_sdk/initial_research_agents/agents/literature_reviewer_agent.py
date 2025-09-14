from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field
from agents import Agent, ModelSettings

from ..tools import literature_search, link_literature


REVIEWER_INSTRUCTIONS = """
You are the Literature Reviewer Agent. Using your tools, search for relevant literature based on the project's objective.
- Use the search tool with thoughtful queries derived from the prompt
- For highly relevant items, link them to the project's paper via the link tool
- Avoid redundant links; de-duplication is handled by the tool
Output only the structured fields.
"""


class ReviewItem(BaseModel):
    title: str
    rationale: str = Field(description="Why this item is relevant")


class LiteratureReviewOutcome(BaseModel):
    selected: List[ReviewItem] = Field(default_factory=list, description="Items intentionally linked to the project")


literature_reviewer_agent = Agent(
    name="literature_reviewer",
    model="gpt-5",
    model_settings=ModelSettings(
        reasoning={
            "effort": "high"
        }
    ),
    instructions=REVIEWER_INSTRUCTIONS,
    tools=[literature_search, link_literature],
    output_type=LiteratureReviewOutcome,
)


