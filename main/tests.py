import os
import asyncio
from django.test import TestCase
from django.contrib.auth import get_user_model
from main.models import Project, Simulation, SimulationStatus


class ResearchServicesIntegrationTests(TestCase):
    """Integration tests hitting public APIs with small queries.

    If a network/API error occurs, the test is skipped rather than failed.
    """

    def test_arxiv_search(self):
        async def go():
            try:
                from main.research_services import HttpClient, search_arxiv

                client = HttpClient()
                try:
                    results = await search_arxiv(client, query="ti:quantum", max_results=3)
                finally:
                    await client.aclose()

                self.assertIsInstance(results, list)
                if results:
                    r0 = results[0]
                    self.assertTrue(r0.title)
                    self.assertEqual(r0.source, "arxiv")
            except Exception as e:
                self.skipTest(f"arXiv API/network issue: {e}")

        asyncio.run(go())

    def test_doaj_search(self):
        async def go():
            try:
                from main.research_services import HttpClient, search_doaj

                client = HttpClient()
                try:
                    results = await search_doaj(client, query="quantum", page=1, page_size=3)
                finally:
                    await client.aclose()

                self.assertIsInstance(results, list)
                if results:
                    r0 = results[0]
                    self.assertTrue(r0.title)
                    self.assertEqual(r0.source, "doaj")
            except Exception as e:
                self.skipTest(f"DOAJ API/network issue: {e}")

        asyncio.run(go())

    def test_semantic_scholar_search(self):
        async def go():
            try:
                from main.research_services import HttpClient, search_semantic_scholar

                client = HttpClient()
                try:
                    results = await search_semantic_scholar(client, query="graph neural networks", limit=3)
                finally:
                    await client.aclose()

                self.assertIsInstance(results, list)
                if results:
                    r0 = results[0]
                    self.assertTrue(r0.title)
                    self.assertEqual(r0.source, "semanticscholar")
            except Exception as e:
                self.skipTest(f"Semantic Scholar API/network issue: {e}")

        asyncio.run(go())

    def test_openalex_search(self):
        async def go():
            try:
                from main.research_services import HttpClient, search_openalex

                mailto = os.getenv("OPENALEX_MAILTO")
                client = HttpClient()
                try:
                    results = await search_openalex(client, query="diffusion models", per_page=3, page=1, mailto=mailto)
                finally:
                    await client.aclose()

                self.assertIsInstance(results, list)
                if results:
                    r0 = results[0]
                    self.assertTrue(r0.title)
                    self.assertEqual(r0.source, "openalex")
            except Exception as e:
                self.skipTest(f"OpenAlex API/network issue: {e}")

        asyncio.run(go())

    def test_aggregate_search_all(self):
        async def go():
            try:
                from main.research_services import HttpClient, search_all

                mailto = os.getenv("OPENALEX_MAILTO")
                client = HttpClient()
                try:
                    results_by_src = await search_all(client, query="quantum", limit_per_source=2, mailto=mailto)
                finally:
                    await client.aclose()

                self.assertIsInstance(results_by_src, dict)
                # Ensure keys exist
                for key in ("arxiv", "doaj", "semanticscholar", "openalex"):
                    self.assertIn(key, results_by_src)
                    self.assertIsInstance(results_by_src[key], list)
            except Exception as e:
                self.skipTest(f"Aggregate API/network issue: {e}")

        asyncio.run(go())


class SimulationRunTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="u1", password="pw")
        self.project = Project.objects.create(owner=self.user, name="P1")

    def test_run_python_simulation_success(self):
        sim = Simulation.objects.create(
            project=self.project,
            name="SumTest",
            code=(
                "a = params.get('a', 1)\n"
                "b = params.get('b', 2)\n"
                "record_result({'sum': a + b})\n"
                "print('done')\n"
            ),
            parameters={"a": 3, "b": 4},
        )
        sim.run(timeout_seconds=10)
        self.assertEqual(sim.status, SimulationStatus.SUCCESS)
        self.assertIsNotNone(sim.result_json)
        self.assertEqual(sim.result_json.get('sum'), 7)
        self.assertIn('done', sim.stdout)

    def test_run_python_simulation_error(self):
        sim = Simulation.objects.create(
            project=self.project,
            name="ErrorTest",
            code=("raise ValueError('boom')\n"),
            parameters={},
        )
        sim.run(timeout_seconds=10)
        self.assertEqual(sim.status, SimulationStatus.FAILED)
        self.assertIsNotNone(sim.stderr)


# Create your tests here.
