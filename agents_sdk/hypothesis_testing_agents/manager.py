from __future__ import annotations

from typing import List
from asgiref.sync import async_to_sync
from pydantic import BaseModel
from agents import Runner

from main.models import Project, Hypothesis, HypothesisStatus as DjangoHypothesisStatus

from .agents.research_agent import research_agent, HypothesisResearch
from .agents.sim_decider_agent import sim_decider_agent, SimulationDecision
from .agents.simulation_agent import simulation_agent, SimulationResult
from .agents.answer_agent import answer_agent, HypothesisAnswer
from ..initial_research_agents.tools import list_hypotheses, update_hypothesis_status


class HypothesisTestResult(BaseModel):
    hypothesis_id: int
    status: str
    justification: str


class HypothesisTestingOutput(BaseModel):
    project_id: int
    results: List[HypothesisTestResult]


class HypothesisTestingServiceManager:
    """Sequentially evaluates each hypothesis: research → decide simulation → (optionally) simulate → answer."""

    def __init__(self) -> None:
        self.runner = Runner()

    async def process(self, project_id: int) -> HypothesisTestingOutput:
        project = Project.objects.get(pk=project_id)
        existing = list_hypotheses(project.id)

        results: List[HypothesisTestResult] = []
        for h in existing:
            # 1) Research background
            research_result = await self.runner.run(research_agent, input=f"Hypothesis: {h.title}\n{h.statement}")
            research: HypothesisResearch = research_result.final_output  # type: ignore

            # 2) Simulation decision
            decider_result = await self.runner.run(sim_decider_agent, input=f"Hypothesis: {h.title}\n{h.statement}\nBackground:\n{research.background_summary}")
            decision: SimulationDecision = decider_result.final_output  # type: ignore

            sim_out: SimulationResult | None = None
            if decision.needed:
                # Create and run a simple placeholder experiment via tools
                sim_prompt = f"# Test for: {h.title}\nprint('Test placeholder')"
                from ..initial_research_agents.tools import create_experiment, CreateExperimentInput, run_experiment
                exp = create_experiment(CreateExperimentInput(project_id=project.id, name=f"AutoSim: {h.title}", code=sim_prompt))
                sim_out = await self._run_sim(exp.id)

            # 3) Answer hypothesis
            combined_input = "\n".join([
                f"Hypothesis: {h.title}",
                h.statement,
                "",
                "Background:",
                research.background_summary,
                "",
                f"Simulation: {sim_out.status if sim_out else 'not required'}",
            ])
            answer_result = await self.runner.run(answer_agent, input=combined_input)
            answer: HypothesisAnswer = answer_result.final_output  # type: ignore

            # Update status in DB
            target_status = answer.status.lower()
            if target_status not in {"supported", "rejected", "inconclusive"}:
                target_status = "inconclusive"
            update_hypothesis_status(dict(hypothesis_id=h.id, status=target_status))  # SDK supports dict coercion

            results.append(HypothesisTestResult(hypothesis_id=h.id, status=target_status, justification=answer.justification))

        return HypothesisTestingOutput(project_id=project.id, results=results)

    async def _run_sim(self, experiment_id: int) -> SimulationResult:
        # The agent tool will handle execution; here we call via Runner for consistency if needed later
        from ..initial_research_agents.tools import run_experiment, get_experiment
        run_experiment(experiment_id)
        det = get_experiment(experiment_id)
        return SimulationResult(experiment_id=experiment_id, status=det.status, stdout=None)

    def run_for_project_sync(self, project_id: int) -> HypothesisTestingOutput:
        async def go():
            return await self.process(project_id)
        return async_to_sync(go)()


