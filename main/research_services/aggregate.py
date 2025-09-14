from __future__ import annotations

import asyncio
from typing import Dict, List, Optional

from .http import HttpClient
from .types import PaperRecord
from .arxiv import search_arxiv
from .doaj import search_doaj
from .semanticscholar import search_semantic_scholar
from .openalex import search_openalex


async def search_all(
    client: HttpClient,
    query: str,
    limit_per_source: int = 20,
    mailto: Optional[str] = None,
    open_access_only: bool = False,
) -> Dict[str, List[PaperRecord]]:
    """Run parallel searches across sources and return a dict keyed by source.

    If open_access_only is True, only include records that have an open_access_pdf_url.
    """

    arxiv_coro = search_arxiv(client, query=query, max_results=limit_per_source)
    doaj_coro = search_doaj(client, query=query, page=1, page_size=limit_per_source)
    s2_coro = search_semantic_scholar(client, query=query, limit=limit_per_source)
    openalex_coro = search_openalex(client, query=query, per_page=limit_per_source, page=1, mailto=mailto)

    arxiv_res, doaj_res, s2_res, oa_res = await asyncio.gather(arxiv_coro, doaj_coro, s2_coro, openalex_coro, return_exceptions=True)

    results: Dict[str, List[PaperRecord]] = {"arxiv": [], "doaj": [], "semanticscholar": [], "openalex": []}

    if isinstance(arxiv_res, list):
        results["arxiv"] = arxiv_res
    if isinstance(doaj_res, list):
        results["doaj"] = doaj_res
    if isinstance(s2_res, list):
        results["semanticscholar"] = s2_res
    if isinstance(oa_res, list):
        results["openalex"] = oa_res

    if open_access_only:
        for source_key, items in results.items():
            results[source_key] = [r for r in items if getattr(r, "open_access_pdf_url", None)]

    return results


