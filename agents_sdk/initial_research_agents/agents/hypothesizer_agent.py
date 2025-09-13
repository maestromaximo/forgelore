from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field
from agents import Agent

from ..tools import (
    list_experiments,
    list_literature,
    create_hypothesis,
    update_hypothesis_status,
    HypothesisModel,
)


HYPOTHESIZER_INSTRUCTIONS = """
You are the Hypothesizer Agent. Your job is to propose high-quality, testable hypotheses that would satisfy the project's objective.

Use your tools to inspect available experiments and linked literature. Then, create hypotheses (quality over quantity). Each hypothesis should be specific and testable.

When appropriate, set statuses after creation only if there is immediate strong evidence (otherwise leave as PROPOSED).
Output only the structured fields.
"""


class HypothesesOutput(BaseModel):
    created: List[HypothesisModel] = Field(default_factory=list, description="Hypotheses created during this run")


hypothesizer_agent = Agent(
    name="hypothesizer",
    model="gpt-4.1",
    instructions=HYPOTHESIZER_INSTRUCTIONS,
    tools=[list_experiments, list_literature, create_hypothesis, update_hypothesis_status],
    output_type=HypothesesOutput,
)


