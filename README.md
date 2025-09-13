## ForgeLore — Autonomous Research Copilot for Academics and R&D

ForgeLore is a professional, research-focused assistant that accelerates the full scientific workflow: literature review, hypothesis generation, code-based experimentation/simulation, results analysis, and structured paper drafting. It is designed for academics, professors, and R&D teams seeking a trustworthy, corporate-grade UI and a rigorous agentic backbone.

![ForgeLore](static/images/forge_lore_logo.png)

### What ForgeLore Does
- **Literature retrieval**: Pull up-to-date papers (starting with arXiv) and summarize key findings.
- **Hypothesis generation**: Propose promising directions based on gaps in the literature.
- **Simulation/experimentation**: Execute Python code for analyses, numeric experiments, or toy simulations.
- **Drafting**: Assemble Introduction, Methods, Results, and Conclusion with references.
- **Modes**: Run fully autonomous or guided/co-pilot with human-in-the-loop approvals.

---

## Architecture (MVP)
- **Backend**: Django (Python).
- **UI**: Server-rendered templates using **TailwindCSS via CDN** (no build step required).
- **Agent/Tools (planned)**: OpenAI Agents SDK integration, arXiv retrieval, PDF ingestion, Python REPL sandbox.
- **State/Storage**: Django defaults for now; vector emebeddings local too

Key templates:
- `templates/landing.html`: Marketing base frame for landing pages.
- `templates/home.html`: Simple landing page (extends `landing.html`) with Sign in/Sign up and product highlights.
- `templates/base.html`: Application shell (top header) + left sidebar container (includes `sidemenu.html`).
- `templates/sidemenu.html`: Corporate sidebar navigation.
- `templates/dashboard.html`: Overview page with KPI cards, quick actions, and recent activity.

Styling:
- Tailwind loaded via CDN in `landing.html` and `base.html`.
- Brand color is configured with a small Tailwind inline config (brand-600/700). Adjust in the `<script>` config if needed.

---

## Project Layout (top-level)
- `forgelore/`: Django project settings and ASGI/WSGI.
- `main/`: Primary Django app (views/models to be expanded).
- `templates/`: UI templates (landing, home, base, sidemenu, dashboard).
- `static/`: Project static assets (logos, images).
- `openai-agents-python/`: SDK and examples for agentic capabilities (upstream project kept vendored).
- `requirements.txt`: Python dependencies.
- `manage.py`: Django management entry point.

---

## Quickstart

### Prerequisites (testing only done in 3.10 rn for the hackathon)
- Python 3.10+

### Setup (Windows PowerShell) (first set the .env!!!)
```powershell
# From the repository root
py -m venv venv
./venv/Scripts/Activate.ps1
pip install -r requirements.txt

# Apply migrations (none or minimal in MVP)
python manage.py migrate

# Run development server
python manage.py runserver
```

### Setup (macOS/Linux) (first set the .env!!!)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open the app at `http://127.0.0.1:8000/`.

---


---

## UI Overview
- **Landing/Home**: Clean, corporate hero + features, clear auth actions, suitable for academics and enterprise.
- **App Shell**: `base.html` integrates the **left sidebar** (`sidemenu.html`) and **top header** with search and account.
- **Dashboard**: KPI cards, quick actions (autonomous run, guided workflow, upload paper, new project), and activity feed.


---

## Configuration
Environment variables (optional initial set):
- `DJANGO_SECRET_KEY` — set a secure key in production.
- `DEBUG` — `True` (dev) / `False` (prod).
- `ALLOWED_HOSTS` — hostnames for deployment.
- `OPENAI_API_KEY` — for agentic features when integrating models.

---

## Roadmap
- **Literature**: arXiv API integration; expandable to OpenAlex and Crossref.
- **PDF ingestion**: extract sections from uploaded manuscripts.
- **RAG**: store summarized facts/sections in a vector store for grounded drafting.
- **Python REPL**: sandboxed execution for simulations (NumPy/SciPy/SymPy/pandas).
- **Autonomous loop**: plan → act (tools/code) → observe → refine → draft.
- **Drafting**: section-by-section academic writing with inline numbered citations and references list.
- **Guided mode**: approvals after literature, hypothesis, experiment planning, and drafting.
- **Progress UI**: streaming step timeline and logs.

---

## Contributing
- Keep the UI strictly professional (no emojis). Prefer monochrome with a restrained brand accent.
- Match existing template patterns (`landing.html`/`base.html`).
- Use clear, well-named views and URLs.

---

## Acknowledgements
- arXiv (open-access literature source)
- OpenAI Agents SDK (agentic orchestration, planned)

---


