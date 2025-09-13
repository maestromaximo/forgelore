import asyncio
from typing import Dict, List
from main.models import Project
from main.research_services import HttpClient, search_all
from agents import function_tool
from main.research_services.types import PaperRecord


@function_tool
def literature_search(query: str, project_id: int) -> Dict[str, List[PaperRecord]]:
    """Synchronous wrapper view that runs async provider searches and renders results.

    Query via GET param `q`. Shows grouped results by source.
    """

    ##if project id is str we convert it to int
    if isinstance(project_id, str):
        project_id = int(project_id)

    projects = Project.objects.order_by('name')
    results_by_source = None
    error = None
    if project_id:
        project = Project.objects.get(id=project_id)
    else:
        project = None
    
    if query:
        from main.research_services import HttpClient, search_all

        def _run():
            async def go():
                client = HttpClient()
                try:
                    mailto = None
                    return await search_all(client, query=query, limit_per_source=10, mailto=mailto)
                finally:
                    await client.aclose()

            return async_to_sync(go)()

        try:
            results_by_source = _run()
        except Exception as exc:
            error = str(exc)

    context = {
        'query': query,
        'results_by_source': results_by_source,
        'error': error,
        'project': project,
    }
    return context


@function_tool
def create_experiment(project_id: int, experiment_name: str) -> str:
    """Creates an experiment for a project"""
    return 

@function_tool
def run_experiment(experiment_id: int) -> str:
    """Runs an experiment for a project"""
    return

@function_tool
def get_experiment(experiment_id: int) -> str:
    """Gets an experiment (full details) for a project"""
    return

@function_tool
def list_experiments(project_id: int) -> List[str]:
    """Lists all experiments for a project with experiment ids and experiment names"""
    return

@function_tool
def list_hypotheses(project_id: int) -> List[str]:
    """Lists all hypotheses for a project with hypothesis ids and hypothesis names"""
    return

@function_tool
def get_hypothesis(hypothesis_id: int) -> str:
    """Gets a hypothesis (full details) for a project"""
    return

@function_tool
def create_hypothesis(project_id: int, hypothesis_name: str, hypothesis_body: str) -> str:
    """Creates a hypothesis for a project"""
    return

#pydantic model for hypothesis status
class HypothesisStatus(str, Enum):
    PROPOSED = "proposed"
    SUPPORTED = "supported"
    REJECTED = "rejected"
    INCONCLUSIVE = "inconclusive"

@function_tool
def update_hypothesis(hypothesis_id: int, status: HypothesisStatus) -> str:
    """Updates a hypothesis for a project"""
    return

@function_tool
def list_notes(project_id: int) -> List[str]:
    """Lists all notes for a project with note ids and note names"""
    return

@function_tool
def get_note(note_id: int) -> str:
    """Gets a note (full details) for a project"""
    return

@function_tool
def create_note(project_id: int, note_name: str, note_body: str) -> str:
    """Creates a note for a project"""
    return

@function_tool
def update_note(note_id: int, note_name: str, note_body: str) -> str:
    """Updates a note for a project"""
    return

@function_tool
def get_paper(project_id: int) -> str:
    """Gets a paper (full details) for the project"""
    return

## WE ALSO NEED to be able to create literature (like after searching for it) and associate it to a project
## then we also need to be able to have a function to get literature, (the model can choose chars to read)
## should also be able to have a function that can just read as well by chars but without being associated to a project, should be the same function.



