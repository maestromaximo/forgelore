from __future__ import annotations

from pydantic import BaseModel, Field
from agents import Agent, ModelSettings

from ...initial_research_agents.tools import create_experiment, run_experiment, get_experiment, CreateExperimentInput, ExperimentDetail


SIMULATION_INSTRUCTIONS = """
You are the Simulation Creation & Execution Agent. Given a hypothesis and context, create a Python experiment to test it and run it.
Use your tools to create and run the experiment. Return the key results.
"""


class SimulationResult(BaseModel):
    experiment_id: int
    status: str
    stdout: str | None = Field(default=None, description="Optional captured stdout if available")


simulation_agent = Agent(
    name="simulation_runner",
    model="gpt-5",
    model_settings=ModelSettings(
        reasoning={
            "effort": "high"
        }
    ),
    instructions=SIMULATION_INSTRUCTIONS,
    tools=[create_experiment, run_experiment, get_experiment],
    output_type=SimulationResult,
)


