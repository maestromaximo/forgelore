## Contributing to ForgeLore

Thanks for your interest in contributing! This document explains how to set up your environment, the coding style we follow, and the preferred workflow for pull requests.

---

## Getting started

### Prerequisites
- Python 3.10+
- Git

### Local setup
```bash
git clone <your-fork-or-this-repo>
cd forgelore
python3 -m venv venv
source venv/bin/activate   # Windows: ./venv/Scripts/Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to verify the app is running.

---

## Project structure
- `forgelore/`: Django project settings and ASGI/WSGI.
- `main/`: app models, views, `research_services/`, utils, and tests.
- `templates/`: server‑rendered UI using Tailwind via CDN (no build step).
- `agents_sdk/`: agent managers for research, drafting, testing, and compilation.

---

## Coding style
- Python: readable, explicit names, early returns, avoid deep nesting, handle errors meaningfully.
- Templates: extend `templates/base.html` for app pages or `templates/landing.html` for marketing. Keep the visual tone corporate and minimal (no emojis). Use Tailwind utilities already present.
- No large refactors mixed with feature changes. Keep edits focused and well‑scoped.

---

## Branching and pull requests
1. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/<short-name>
   ```
2. Make small, logically coherent commits with descriptive messages.
3. Ensure the server runs and basic flows work (create project, literature search, edit paper, run experiment).
4. Push your branch and open a PR. Include:
   - What changed and why
   - Screenshots/GIFs for UI changes
   - Any migration or config implications

We squash‑merge to keep history clean.

---

## UI guidelines (quick reference)
- Tailwind via CDN only; do not introduce a build step.
- Use Inter font and brand colors configured in base templates (`brand-600/700`).
- Use named URL helpers in templates (e.g., `{% url 'projects_list' %}`).
- Forms must include `{% csrf_token %}` and accessible labels.

---

## Tests
Light tests live under `main/tests/`. If you add substantial logic to `research_services/` or views, please include minimal tests when possible.

---

## Security & data handling
- Never commit secrets. Use environment variables.
- Treat uploaded content and external data as untrusted. Validate and sanitize.

---

## Getting help
Open a discussion or issue with clear steps to reproduce and context. PRs welcome!


