from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Author:
    """Represents a paper author with optional identifiers."""

    name: str
    orcid: Optional[str] = None
    affiliation: Optional[str] = None


@dataclass
class PaperRecord:
    """Unified paper record across sources.

    The intent is to map different provider responses (arXiv, DOAJ, Semantic Scholar, OpenAlex)
    into a common structure so downstream logic can be provider-agnostic.
    """

    # Core identity
    source: str  # "arxiv" | "doaj" | "semanticscholar" | "openalex"
    source_id: str

    # Bibliographic
    title: str
    abstract: str = ""
    authors: List[Author] = field(default_factory=list)
    year: Optional[int] = None
    published_date: Optional[str] = None  # ISO date string if available
    venue: Optional[str] = None  # Journal, conference, or repository

    # Identifiers and links
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None
    url: Optional[str] = None
    open_access_pdf_url: Optional[str] = None

    # Extra metadata
    fields_of_study: List[str] = field(default_factory=list)
    topics: List[str] = field(default_factory=list)
    citations_count: Optional[int] = None
    references_count: Optional[int] = None
    raw: Dict = field(default_factory=dict)  # Provider-specific payload for debugging


def asdict_record(record: PaperRecord) -> Dict:
    """Convert PaperRecord to a plain dict suitable for JSON serialization."""

    return {
        "source": record.source,
        "source_id": record.source_id,
        "title": record.title,
        "abstract": record.abstract,
        "authors": [
            {"name": a.name, "orcid": a.orcid, "affiliation": a.affiliation}
            for a in record.authors
        ],
        "year": record.year,
        "published_date": record.published_date,
        "venue": record.venue,
        "doi": record.doi,
        "arxiv_id": record.arxiv_id,
        "url": record.url,
        "open_access_pdf_url": record.open_access_pdf_url,
        "fields_of_study": record.fields_of_study,
        "topics": record.topics,
        "citations_count": record.citations_count,
        "references_count": record.references_count,
        "raw": record.raw,
    }


