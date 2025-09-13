from __future__ import annotations

from typing import List, Optional

from asgiref.sync import sync_to_async

# Import shared Pydantic models and internal sync helpers from tools
from .tools import (
    LiteratureMeta,
    LiteratureReadRequest,
    LiteratureReadResult,
    LinkLiteratureInput,
    LinkLiteratureResult,
    PaperModel,
    ExperimentSummary,
    ExperimentDetail,
    CreateExperimentInput,
    KeyValue,
    HypothesisModel,
    UpdateHypothesisStatusInput,
    HypothesisStatus,
    CreateHypothesisInput,
)

from .tools import (
    _list_literature_sync,
    _read_literature_sync,
    _link_literature_sync,
    _get_paper_sync,
    _list_experiments_sync,
    _get_experiment_sync,
    _create_experiment_sync,
    _run_experiment_sync,
    _list_hypotheses_sync,
    _create_hypothesis_sync,
    _update_hypothesis_status_sync,
)


# ==========================
# Undecorated async utilities
# ==========================

async def list_literature(project_id: int) -> List[LiteratureMeta]:
    return await sync_to_async(_list_literature_sync)(project_id)


async def read_literature(request: LiteratureReadRequest) -> LiteratureReadResult:
    return await sync_to_async(_read_literature_sync)(request)


async def link_literature(input: LinkLiteratureInput) -> LinkLiteratureResult:
    return await sync_to_async(_link_literature_sync)(input)


async def get_paper(project_id: int) -> PaperModel:
    return await sync_to_async(_get_paper_sync)(project_id)


async def list_experiments(project_id: int) -> List[ExperimentSummary]:
    return await sync_to_async(_list_experiments_sync)(project_id)


async def get_experiment(experiment_id: int) -> ExperimentDetail:
    return await sync_to_async(_get_experiment_sync)(experiment_id)


async def create_experiment(
    project_id: int,
    name: str,
    code: str,
    description: str = "",
    language: str = "python",
    parameters: Optional[List[KeyValue]] = None,
) -> ExperimentDetail:
    input_model = CreateExperimentInput(
        project_id=project_id,
        name=name,
        description=description,
        code=code,
        language=language,
        parameters=parameters,
    )
    return await sync_to_async(_create_experiment_sync)(input_model)


async def run_experiment(experiment_id: int) -> ExperimentDetail:
    return await sync_to_async(_run_experiment_sync)(experiment_id)


async def list_hypotheses(project_id: int) -> List[HypothesisModel]:
    return await sync_to_async(_list_hypotheses_sync)(project_id)


async def create_hypothesis(input: CreateHypothesisInput) -> HypothesisModel:
    return await sync_to_async(_create_hypothesis_sync)(input)


async def update_hypothesis_status(
    hypothesis_id: int,
    status: HypothesisStatus | str,
) -> HypothesisModel:
    status_enum = status if isinstance(status, HypothesisStatus) else HypothesisStatus(status)
    input_model = UpdateHypothesisStatusInput(hypothesis_id=hypothesis_id, status=status_enum)
    return await sync_to_async(_update_hypothesis_status_sync)(input_model)


