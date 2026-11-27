# Visa Culture

This is the Visa Culture website. It shows study destinations, university guides, IELTS/PTE classes, and a consultation booking form.

## Start here

- [Project guide](docs/DEVELOPER_MAP.md): how the website works and where to make changes.
- [File list](docs/FILE_INDEX.md): what each file does.
- [SEO guide](SEO_MAINTENANCE.md): how to keep pages easy to find on Google.

## Run the website

Use Python 3.11 or newer. Open a terminal in this project folder:

```powershell
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env`. Add your local settings to `.env`, then run:

```powershell
python app.py
```

You can also run `python -m flask --app app run`.

## Main folders

| Folder | What it contains |
| --- | --- |
| `backend/` | Python code: page links, settings, page data, email and spam checks |
| `templates/` | Page text, HTML, and small page sections |
| `static/css/` | Page colors, spacing, layout and animation styles |
| `static/js/` | Buttons, menus, sliders and other browser actions |
| `static/images/` | Website images |
| `tests/` | Checks that help catch broken pages and changed behavior |
| `tools/` | Tools used while working on the code |
| `docs/` | Guides for the team |

## Check your changes

Install the extra tools used by the checks:

```powershell
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python -m tools.format_styles --check
```

To tidy CSS spacing, run `python -m tools.format_styles`.

For browser checks:

```powershell
python -m playwright install chromium
python -m tests.browser_check
```

The browser check compares pages with an older version saved in Git. The newer SEO changes are meant to change the homepage, so review those differences before calling them bugs. See the project guide for details.

## Putting the website online

The existing `Dockerfile` starts the website with Gunicorn using `app:app`. No separate frontend build is needed. Editing files locally does not publish the website.

Keep passwords in `.env` or your hosting settings. Do not put real passwords in code or guides.
