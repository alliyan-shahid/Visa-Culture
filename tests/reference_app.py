"""Load the original committed application for optional browser comparisons."""
import json
from pathlib import Path
import subprocess
import sys
from types import ModuleType

from jinja2 import DictLoader

ROOT = Path(__file__).resolve().parents[1]


def load_reference():
    revision = json.loads((ROOT / "tests/fixtures/reference.json").read_text(encoding="utf-8"))["commit"]
    def git(*arguments):
        return subprocess.run(["git", *arguments], cwd=ROOT, check=True, capture_output=True).stdout

    paths = git("ls-tree", "-r", "--name-only", revision, "templates", "static").decode().splitlines()
    templates = {path.removeprefix("templates/"): git("show", revision + ":" + path).decode("utf-8")
                 for path in paths if path.startswith("templates/") and path.endswith(".html")}
    assets = {"/" + path: git("show", revision + ":" + path)
              for path in paths if path.startswith("static/") and path.endswith((".css", ".js"))}
    module = ModuleType("refactor_reference")
    module.__file__ = str(ROOT / "app.py")
    sys.modules[module.__name__] = module
    source = git("show", revision + ":app.py").decode("utf-8")
    exec(compile(source, module.__file__, "exec"), module.__dict__)
    module.app.jinja_loader = DictLoader(templates)
    module.app.config.update(TESTING=True, TURNSTILE_SITEKEY="", TURNSTILE_SECRET_KEY="")
    return module.app, assets
