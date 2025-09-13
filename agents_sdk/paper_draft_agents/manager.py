from __future__ import annotations

from typing import Optional
from asgiref.sync import async_to_sync
from pydantic import BaseModel
from agents import Runner

from main.models import Project, Paper

from .agents.drafting_agent import DraftSections, drafting_agent


class PaperDraftOutput(BaseModel):
    project_id: int
    paper_id: int
    updated_abstract: Optional[str] = None
    literature_review_added: bool = False


class PaperDraftServiceManager:
    """Generates an initial draft (abstract + literature review) when paper is empty/minimal."""

    def __init__(self) -> None:
        self.runner = Runner()

    async def process(self, project_id: int) -> PaperDraftOutput:
        project = Project.objects.get(pk=project_id)
        paper, _ = Paper.objects.get_or_create(project=project, defaults={'title': project.name, 'abstract': project.abstract})

        result = await self.runner.run(drafting_agent, input=f"Project: {project.name}\nObjective: {paper.abstract or project.abstract or ''}")
        sections: DraftSections = result.final_output  # type: ignore

        updated = False
        if sections.abstract and sections.abstract.strip():
            paper.abstract = sections.abstract.strip()
            updated = True
        # Append/seed literature review into content_raw
        content = paper.content_raw or ""
        content += ("\n\n# Literature Review\n\n" + sections.literature_review.strip())
        paper.content_raw = content
        paper.save(update_fields=['abstract', 'content_raw', 'updated_at'])

        return PaperDraftOutput(
            project_id=project.id,
            paper_id=paper.id,
            updated_abstract=paper.abstract if updated else None,
            literature_review_added=True,
        )

    def run_for_project_sync(self, project_id: int) -> PaperDraftOutput:
        async def go():
            return await self.process(project_id)
        return async_to_sync(go)()


