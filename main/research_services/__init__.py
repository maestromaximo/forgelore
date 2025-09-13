from .types import PaperRecord, Author, asdict_record
from .http import HttpClient, with_client
from .arxiv import search_arxiv, fetch_arxiv_by_id
from .doaj import search_doaj
from .semanticscholar import search_semantic_scholar, fetch_semantic_scholar_by_id
from .openalex import search_openalex, fetch_openalex_by_id
from .aggregate import search_all

__all__ = [
    "Author",
    "PaperRecord",
    "asdict_record",
    "HttpClient",
    "with_client",
    "search_arxiv",
    "fetch_arxiv_by_id",
    "search_doaj",
    "search_semantic_scholar",
    "fetch_semantic_scholar_by_id",
    "search_openalex",
    "fetch_openalex_by_id",
    "search_all",
]


