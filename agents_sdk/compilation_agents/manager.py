from __future__ import annotations

from typing import List
import inspect
from asgiref.sync import async_to_sync, sync_to_async
from pydantic import BaseModel
from agents import Runner

from main.models import Project, Paper

from .agents.compilation_agent import compilation_agent, CompilationPlan, PaperDiff


class CompilationOutput(BaseModel):
    project_id: int
    paper_id: int
    applied_diffs: int


class CompilationServiceManager:
    """Applies small, targeted diffs to paper content based on agent plan."""

    def __init__(self) -> None:
        self.runner = Runner()

    async def process(self, project_id: int) -> CompilationOutput:
        project = await sync_to_async(Project.objects.get)(pk=project_id)
        paper, _ = await sync_to_async(Paper.objects.get_or_create)(project=project, defaults={'title': project.name, 'abstract': project.abstract})

        result = await self._run(compilation_agent, f"Project: {project.name}", max_turns=50)
        plan: CompilationPlan = result.final_output  # type: ignore

        applied = 0
        content = paper.content_raw or ""
        for diff in plan.diffs:
            if diff.target and diff.target in content:
                content = content.replace(diff.target, diff.replacement)
                applied += 1

        if applied:
            paper.content_raw = content
            await sync_to_async(paper.save)(update_fields=['content_raw', 'updated_at'])

        return CompilationOutput(project_id=project.id, paper_id=paper.id, applied_diffs=applied)

    def run_for_project_sync(self, project_id: int) -> CompilationOutput:
        async def go():
            return await self.process(project_id)
        return async_to_sync(go)()

    async def _run(self, *args, **kwargs):
        """Call Runner.run and support both async and sync mocks."""
        result = self.runner.run(*args, **kwargs)
        if inspect.isawaitable(result):
            return await result
        return result


