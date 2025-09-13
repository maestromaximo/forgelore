from __future__ import annotations

import random
from typing import List, Optional

from asgiref.sync import async_to_sync
from pydantic import BaseModel, Field

from agents import Runner

from main.models import Project, Paper, Note

from .tools import (
    PaperModel,
    ExperimentSummary,
    HypothesisModel,
    list_experiments,
    list_literature,
)
from .agents.formalizer_agent import FormalizedAsk, formalizer_agent
from .agents.literature_reviewer_agent import LiteratureReviewOutcome, literature_reviewer_agent
from .agents.literature_summarizer_agent import ProjectFocusedSummary, literature_summarizer_agent
from .agents.hypothesizer_agent import HypothesesOutput, hypothesizer_agent


class InitialResearchOutput(BaseModel):
    project_id: int
    paper_id: int
    improved_abstract: Optional[str] = None
    literature_summary_note_id: Optional[int] = None
    created_hypotheses: List[HypothesisModel] = Field(default_factory=list)


class InitialResearchServiceManager:
    """Orchestrates the initial research workflow for a project.

    Steps:
    1. Formalize/Improve the abstract and objectives
    2. Literature review with search + linking
    3. Literature summarization focused on project goal (saved as Note)
    4. Hypothesis generation using available tools
    """

    def __init__(self) -> None:
        self.runner = Runner()

    async def process(self, project_id: int) -> InitialResearchOutput:
        project = Project.objects.get(pk=project_id)
        paper, _ = Paper.objects.get_or_create(project=project, defaults={
            'title': project.name,
            'abstract': project.abstract,
        })

        # Gather context summaries
        experiments: List[ExperimentSummary] = list_experiments(project_id)
        literature_meta = list_literature(project_id)

        # Step 1: Formalize
        formalizer_input = self._build_formalizer_prompt(project, paper, experiments, literature_meta)
        formalizer_result = await self.runner.run(
            formalizer_agent,
            input=formalizer_input,
        )
        formalized: FormalizedAsk = formalizer_result.final_output  # type: ignore

        improved_abstract = (formalized.improved_abstract or '').strip()
        if improved_abstract and improved_abstract != (paper.abstract or '').strip():
            paper.abstract = improved_abstract
            paper.save(update_fields=['abstract', 'updated_at'])

        # Step 2: Literature review (agent uses tools to search/link)
        reviewer_input = self._build_reviewer_prompt(project, paper, formalized, literature_meta)
        await self.runner.run(literature_reviewer_agent, input=reviewer_input)

        # Refresh literature after potential linking
        literature_meta = list_literature(project_id)

        # Step 3: Literature summarization (agent reads via tools)
        summarizer_input = self._build_summarizer_prompt(project, paper, formalized, literature_meta)
        summarizer_result = await self.runner.run(literature_summarizer_agent, input=summarizer_input)
        summary: ProjectFocusedSummary = summarizer_result.final_output  # type: ignore

        # Save as Note with a 4-digit id suffix in title
        note_title = f"Literature Summary {random.randint(1000, 9999)}"
        note = Note.objects.create(project=project, title=note_title, body=summary.combined_summary)

        # Step 4: Hypothesis generation (agent can create hypotheses via tools)
        hypothesizer_input = self._build_hypothesizer_prompt(project, paper, formalized, literature_meta, experiments)
        hypotheses_result = await self.runner.run(hypothesizer_agent, input=hypothesizer_input)
        hypotheses_output: HypothesesOutput = hypotheses_result.final_output  # type: ignore

        # Return snapshot of created/updated items
        return InitialResearchOutput(
            project_id=project.id,
            paper_id=paper.id,
            improved_abstract=paper.abstract or None,
            literature_summary_note_id=note.id,
            created_hypotheses=hypotheses_output.created or [],
        )

    def run_for_project_sync(self, project_id: int) -> InitialResearchOutput:
        """Sync wrapper for Django contexts."""

        async def go():
            return await self.process(project_id)

        return async_to_sync(go)()

    def _build_formalizer_prompt(
        self,
        project: Project,
        paper: Paper,
        experiments: List[ExperimentSummary],
        literature_meta,
    ) -> str:
        lines: List[str] = []
        lines.append(f"Project: {project.name}")
        lines.append("")
        lines.append("Current abstract:")
        lines.append(paper.abstract or "")
        lines.append("")
        if experiments:
            lines.append("Experiments available:")
            for e in experiments:
                lines.append(f"- {e.name} (status={e.status})")
            lines.append("")
        if literature_meta:
            lines.append("Linked literature (by title/year):")
            for lm in literature_meta:
                year = f" ({lm.year})" if getattr(lm, 'year', None) else ""
                lines.append(f"- {lm.title}{year}")
            lines.append("")
        lines.append("Task: Improve and formalize the research ask.")
        return "\n".join(lines)

    def _build_reviewer_prompt(
        self,
        project: Project,
        paper: Paper,
        formalized: FormalizedAsk,
        literature_meta,
    ) -> str:
        lines: List[str] = []
        lines.append(f"Project: {project.name}")
        lines.append("Formalized ask:")
        lines.append(formalized.improved_abstract or paper.abstract or "")
        lines.append("")
        lines.append("Use your tools to search and (if appropriate) link relevant literature to support the project.")
        return "\n".join(lines)

    def _build_summarizer_prompt(
        self,
        project: Project,
        paper: Paper,
        formalized: FormalizedAsk,
        literature_meta,
    ) -> str:
        lines: List[str] = []
        lines.append(f"Project: {project.name}")
        lines.append("Objective:")
        lines.append(formalized.improved_abstract or paper.abstract or "")
        lines.append("")
        lines.append("Summarize linked literature with focus on how each connects to the objective.")
        lines.append("Only use your reading tools; do not invent sources.")
        return "\n".join(lines)

    def _build_hypothesizer_prompt(
        self,
        project: Project,
        paper: Paper,
        formalized: FormalizedAsk,
        literature_meta,
        experiments: List[ExperimentSummary],
    ) -> str:
        lines: List[str] = []
        lines.append(f"Project: {project.name}")
        lines.append("Objective:")
        lines.append(formalized.improved_abstract or paper.abstract or "")
        lines.append("")
        if experiments:
            lines.append("Available experiments:")
            for e in experiments:
                lines.append(f"- {e.name} (status={e.status})")
            lines.append("")
        lines.append("Create high-quality hypotheses needed to satisfy the research task.")
        lines.append("Use your tools to create hypotheses; prefer quality over quantity.")
        return "\n".join(lines)


