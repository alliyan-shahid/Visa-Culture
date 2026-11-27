"""Stable comparison helpers for extraction and presentation-only formatting."""
import json
from pathlib import Path
import re

import tinycss2

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
BLOCK_TAGS = "section|article|div|header|footer|nav|main|aside|h[1-6]|p|ul|ol|li|details|summary|form"
BLOCK_GAP = re.compile(r"(</?(?:" + BLOCK_TAGS + r")\b[^>]*>)\s+(?=</?(?:" + BLOCK_TAGS + r")\b)", re.I)


def expand_css(path):
    """Expand local CSS entry points in order for comparison with original assets."""
    path = Path(path)
    source = path.read_text(encoding="utf-8")
    return re.sub(r'@import url\("([^"\n]+)"\);\n?',
                  lambda match: expand_css(path.parent / match[1]), source)


def normalized_body(response):
    body = response.get_data(as_text=True)
    manifest = FIXTURES / "extracted_assets.json"
    if manifest.exists():
        for item in json.loads(manifest.read_text(encoding="utf-8")):
            paths = item.get("files", [item.get("file")])
            content = "".join(expand_css(ROOT / "static" / path) if path.endswith(".css") else
                              (ROOT / "static" / path).read_text(encoding="utf-8") for path in paths)
            body = body.replace(item["replacement"], item["opening"] + content + item["closing"])
    return body


def components(tokens):
    """Retain tokens, quoted strings, selector spaces, and value spaces."""
    return tinycss2.serialize(tokens).strip()


def css_contract(source):
    result = []
    rules = tinycss2.parse_stylesheet(source, skip_whitespace=True, skip_comments=True)
    for rule in rules:
        if rule.type == "qualified-rule":
            declarations = []
            for declaration in tinycss2.parse_declaration_list(rule.content, skip_whitespace=True, skip_comments=True):
                if declaration.type == "declaration":
                    declarations.append([declaration.name, components(declaration.value), declaration.important])
                else:
                    raise AssertionError(f"Unexpected CSS declaration: {declaration}")
            result.append(["rule", components(rule.prelude), declarations])
        elif rule.type == "at-rule":
            if rule.content is not None and rule.at_keyword.lower() in {"viewport", "font-face", "page"}:
                children = [[d.name, components(d.value), d.important] for d in tinycss2.parse_declaration_list(rule.content, skip_comments=True, skip_whitespace=True)]
            else:
                children = css_contract(tinycss2.serialize(rule.content)) if rule.content is not None else None
            result.append(["at", rule.at_keyword, components(rule.prelude), children])
        else:
            raise AssertionError(f"Unexpected CSS rule: {rule}")
    return result


def canonical_body(body):
    # Only block-to-block indentation is ignored. Inline text remains exact.
    body = re.sub(r"<style([^>]*)>(.*?)</style>",
                  lambda match: "<style" + match[1] + ">" + json.dumps(css_contract(match[2]), ensure_ascii=False) + "</style>",
                  body, flags=re.S)
    return BLOCK_GAP.sub(r"\1", body)
