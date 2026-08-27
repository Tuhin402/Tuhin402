# Profile Generator — Setup

## Local setup

Create a `.env` file in the project root:

```env
GITHUB_TOKEN=your_github_personal_access_token
```

Keep `.env` ignored by Git.

Install the project environment from `requirements.txt` or `environment.yml`.

Then run:

```powershell
python build.py
```

The pipeline generates:

```text
generated/
├── ascii/
├── images/
├── svg/
└── github/
```

`generated/svg/` contains the animated SVG versions for local/browser viewing.

`generated/github/` contains GitHub-safe final-state SVGs plus the animated ASCII hero GIF.

## Local interactive preview

From the project root:

```powershell
python -m http.server 8000
```

Open:

```text
http://localhost:8000/preview.html
```

The preview provides:

- animated SVGs
- icon-only skill arsenal
- hover effects
- animated progress/XP UI
- responsive cards
- gamified presentation

## GitHub Actions

Create a repository Actions secret named:

```text
PROFILE_GENERATOR_TOKEN
```

Do not name a custom secret with the `GITHUB_` prefix.

The workflow maps it to the environment variable already expected by the Python application:

```yaml
env:
  GITHUB_TOKEN: ${{ secrets.PROFILE_GENERATOR_TOKEN }}
```

No Python authentication code needs to change.

The workflow can be run manually from the Actions tab and is also scheduled.

## Profile README

The repository must be the username-matching profile repository:

```text
Tuhin402/Tuhin402
```

The generated root `README.md` references the files under:

```text
generated/github/
```

This keeps the README compatible with the static rendering limitations of GitHub.

## Tuning

The main ASCII hero display size is controlled from:

```python
ASCII_DISPLAY_WIDTH = 520
```

The skill icons are defined in:

```python
PROFILE_SKILLS = (...)
```

No skills are rendered as text badges; the README uses icon-only Simple Icons.

The animated ASCII hero GIF duration is controlled by:

```python
ASCIIAnimatedGIFExporter(
    ...
    duration_seconds=8.0,
)
```

The local SVG animation remains independent from the GitHub GIF export.
