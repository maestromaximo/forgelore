from __future__ import annotations

from typing import List, Optional
from asgiref.sync import async_to_sync
from pydantic import BaseModel, Field
from enum import Enum

from agents import function_tool

from main.models import Project, Paper, Literature, Citation, Simulation, Hypothesis, HypothesisStatus as DjangoHypothesisStatus, Note
from main.research_services import HttpClient, search_all
from main.research_services.types import PaperRecord, asdict_record


# ==========================
# Pydantic Models (Tool I/O)
# ==========================

class SearchInput(BaseModel):
    query: str = Field(description="Search query string")
    limit_per_source: int = Field(default=10, description="Max results per provider")


class SearchResultItem(BaseModel):
    source: str
    source_id: str
    title: str
    abstract: str = ""
    year: Optional[int] = None
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None
    url: Optional[str] = None
    open_access_pdf_url: Optional[str] = None
    venue: Optional[str] = None


class SearchSourceResults(BaseModel):
    provider: str = Field(description="Provider name, e.g., arxiv, openalex")
    papers: List[SearchResultItem]


class SearchResults(BaseModel):
    results: List[SearchSourceResults]


class LiteratureMeta(BaseModel):
    id: int
    title: str
    year: Optional[int] = None
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None
    url: Optional[str] = None
    source_type: str


class LiteratureReadRequest(BaseModel):
    literature_id: int
    max_chars: int = Field(default=8000, ge=100, le=200000)
    include_abstract: bool = True


class LiteratureReadResult(BaseModel):
    id: int
    title: str
    content: str
    year: Optional[int] = None
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None
    url: Optional[str] = None


class LinkLiteratureInput(BaseModel):
    project_id: int
    title: str
    authors: Optional[str] = Field(default="", description="Comma-separated author names")
    year: Optional[int] = None
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None
    url: Optional[str] = None
    open_access_pdf_url: Optional[str] = None
    abstract: Optional[str] = None
    venue: Optional[str] = None


class LinkLiteratureResult(BaseModel):
    literature_id: int
    created: bool
    citation_id: Optional[int] = None


class PaperModel(BaseModel):
    id: int
    title: str
    abstract: str = ""
    content_format: str
    content_raw: str = ""


class ExperimentSummary(BaseModel):
    id: int
    name: str
    description: str = ""
    status: str


class ExperimentDetail(BaseModel):
    id: int
    name: str
    description: str = ""
    code: str
    language: str
    parameters: Optional[dict] = None
    status: str


class HypothesisStatus(str, Enum):
    PROPOSED = "proposed"
    SUPPORTED = "supported"
    REJECTED = "rejected"
    INCONCLUSIVE = "inconclusive"


class HypothesisModel(BaseModel):
    id: int
    title: str
    statement: str
    status: HypothesisStatus


class CreateHypothesisInput(BaseModel):
    project_id: int
    title: str
    statement: str


class UpdateHypothesisStatusInput(BaseModel):
    hypothesis_id: int
    status: HypothesisStatus


class NoteModel(BaseModel):
    id: int
    title: str
    body: str


class CreateNoteInput(BaseModel):
    project_id: int
    title: str
    body: str


# ======
# Tools
# ======

@function_tool
def literature_search(input: SearchInput) -> SearchResults:
    """Search literature across providers (arXiv/OpenAlex/DOAJ/Semantic Scholar).

    Returns structured results grouped by provider.
    """

    def _run():
        async def go():
            client = HttpClient()
            try:
                grouped = await search_all(
                    client,
                    query=input.query,
                    limit_per_source=input.limit_per_source,
                    mailto=None,
                )
                return grouped
            finally:
                await client.aclose()

        return async_to_sync(go)()

    grouped = _run()
    source_results: List[SearchSourceResults] = []
    for provider, records in (grouped or {}).items():
        items: List[SearchResultItem] = []
        for rec in records or []:
            # rec is a PaperRecord dataclass
            data = asdict_record(rec)
            items.append(
                SearchResultItem(
                    source=data.get("source", provider),
                    source_id=data.get("source_id", ""),
                    title=data.get("title", ""),
                    abstract=data.get("abstract", ""),
                    year=data.get("year"),
                    doi=data.get("doi"),
                    arxiv_id=data.get("arxiv_id"),
                    url=data.get("url"),
                    open_access_pdf_url=data.get("open_access_pdf_url"),
                    venue=data.get("venue"),
                )
            )
        source_results.append(SearchSourceResults(provider=str(provider), papers=items))
    return SearchResults(results=source_results)


@function_tool
def list_literature(project_id: int) -> List[LiteratureMeta]:
    """List literature linked to the project's paper (via citations)."""
    project = Project.objects.get(pk=project_id)
    try:
        paper = project.paper
    except Paper.DoesNotExist:
        return []

    results: List[LiteratureMeta] = []
    for cit in paper.citations.select_related('literature').order_by('order'):
        lit = cit.literature
        results.append(
            LiteratureMeta(
                id=lit.id,
                title=lit.title,
                year=lit.year,
                doi=lit.doi or None,
                arxiv_id=lit.arxiv_id or None,
                url=lit.url or None,
                source_type=lit.source_type,
            )
        )
    return results


@function_tool
def read_literature(request: LiteratureReadRequest) -> LiteratureReadResult:
    """Read literature text up to a maximum number of characters (abstract + full text)."""
    lit = Literature.objects.get(pk=request.literature_id)
    blocks: List[str] = []
    if request.include_abstract and lit.abstract:
        blocks.append(lit.abstract.strip())
    if lit.full_text:
        blocks.append(lit.full_text.strip())
    content = ("\n\n".join(blocks)).strip()
    if not content:
        content = ""
    if len(content) > request.max_chars:
        content = content[: request.max_chars]
    return LiteratureReadResult(
        id=lit.id,
        title=lit.title,
        content=content,
        year=lit.year,
        doi=lit.doi or None,
        arxiv_id=lit.arxiv_id or None,
        url=lit.url or None,
    )


@function_tool
def link_literature(input: LinkLiteratureInput) -> LinkLiteratureResult:
    """Create or link a Literature entry to the project's paper via a Citation.

    De-duplicates by DOI, then arXiv ID, else (title+url).
    """
    project = Project.objects.get(pk=input.project_id)
    paper, _ = Paper.objects.get_or_create(project=project, defaults={'title': project.name, 'abstract': project.abstract})

    qs = Literature.objects.all()
    if input.doi:
        qs = qs.filter(doi=input.doi)
    elif input.arxiv_id:
        qs = qs.filter(arxiv_id=input.arxiv_id)
    else:
        qs = qs.filter(title=input.title, url=input.url or "")
    literature = qs.first()
    created = False
    if not literature:
        literature = Literature.objects.create(
            title=input.title,
            authors=input.authors or "",
            journal_or_publisher=input.venue or "",
            year=input.year,
            doi=input.doi or "",
            arxiv_id=input.arxiv_id or "",
            url=input.url or (input.open_access_pdf_url or ""),
            abstract=input.abstract or "",
        )
        created = True

    last_order = paper.citations.order_by('-order').first().order if paper.citations.exists() else 0
    cit = Citation.objects.create(paper=paper, literature=literature, order=last_order + 1)
    return LinkLiteratureResult(literature_id=literature.id, created=created, citation_id=cit.id)


@function_tool
def get_paper(project_id: int) -> PaperModel:
    """Get the project's Paper (creating a default if missing)."""
    project = Project.objects.get(pk=project_id)
    paper, _ = Paper.objects.get_or_create(project=project, defaults={'title': project.name, 'abstract': project.abstract})
    return PaperModel(
        id=paper.id,
        title=paper.title,
        abstract=paper.abstract or "",
        content_format=paper.content_format,
        content_raw=paper.content_raw or "",
    )


@function_tool
def list_experiments(project_id: int) -> List[ExperimentSummary]:
    """List simulations/experiments for a project."""
    sims = Simulation.objects.filter(project_id=project_id).order_by('-updated_at')
    return [
        ExperimentSummary(id=s.id, name=s.name, description=s.description or "", status=s.status)
        for s in sims
    ]


@function_tool
def get_experiment(experiment_id: int) -> ExperimentDetail:
    """Get a simulation/experiment details."""
    s = Simulation.objects.get(pk=experiment_id)
    return ExperimentDetail(
        id=s.id,
        name=s.name,
        description=s.description or "",
        code=s.code,
        language=s.language,
        parameters=s.parameters,
        status=s.status,
    )


@function_tool
def list_hypotheses(project_id: int) -> List[HypothesisModel]:
    """List hypotheses for a project."""
    items = Hypothesis.objects.filter(project_id=project_id).order_by('-updated_at')
    results: List[HypothesisModel] = []
    for h in items:
        results.append(
            HypothesisModel(
                id=h.id,
                title=h.title,
                statement=h.statement,
                status=HypothesisStatus(h.status),
            )
        )
    return results


@function_tool
def create_hypothesis(input: CreateHypothesisInput) -> HypothesisModel:
    """Create a hypothesis under the project (auto-links to the project's paper if present)."""
    project = Project.objects.get(pk=input.project_id)
    h = Hypothesis.objects.create(
        project=project,
        title=input.title,
        statement=input.statement,
        status=DjangoHypothesisStatus.PROPOSED,
    )
    # Best-effort link to paper
    try:
        h.paper = project.paper
        h.save(update_fields=['paper'])
    except Paper.DoesNotExist:
        pass
    return HypothesisModel(id=h.id, title=h.title, statement=h.statement, status=HypothesisStatus(h.status))


@function_tool
def update_hypothesis_status(input: UpdateHypothesisStatusInput) -> HypothesisModel:
    """Update hypothesis status."""
    h = Hypothesis.objects.get(pk=input.hypothesis_id)
    h.status = input.status.value
    h.save(update_fields=['status', 'updated_at'])
    return HypothesisModel(id=h.id, title=h.title, statement=h.statement, status=HypothesisStatus(h.status))


@function_tool
def create_note(input: CreateNoteInput) -> NoteModel:
    """Create a project note."""
    project = Project.objects.get(pk=input.project_id)
    note = Note.objects.create(project=project, title=input.title, body=input.body)
    return NoteModel(id=note.id, title=note.title, body=note.body)


@function_tool
def get_note(note_id: int) -> NoteModel:
    """Get a note by id."""
    note = Note.objects.get(pk=note_id)
    return NoteModel(id=note.id, title=note.title, body=note.body)


@function_tool
def list_notes(project_id: int) -> List[NoteModel]:
    """List notes for a project."""
    notes = Note.objects.filter(project_id=project_id).order_by('-updated_at')
    return [NoteModel(id=n.id, title=n.title, body=n.body) for n in notes]


@function_tool
def update_note(note_id: int, title: str, body: str) -> NoteModel:
    """Update a note's title and body."""
    note = Note.objects.get(pk=note_id)
    note.title = title
    note.body = body
    note.save(update_fields=['title', 'body', 'updated_at'])
    return NoteModel(id=note.id, title=note.title, body=note.body)




