"""Format CSS and templated CSS without changing declaration order or values.

Run: python -m tools.format_styles [--check]
Requires the development dependencies, never runs in production.
"""
from pathlib import Path
import re
import sys

import tinycss2

ROOT = Path(__file__).resolve().parents[1]


def declarations(tokens, indent):
    lines = []
    for item in tinycss2.parse_declaration_list(tokens, skip_whitespace=True):
        if item.type == "comment":
            lines.append(indent + "/*" + item.value.strip() + "*/")
        elif item.type == "declaration":
            important = " !important" if item.important else ""
            lines.append(f"{indent}{item.name}: {tinycss2.serialize(item.value).strip()}{important};")
        else:
            raise ValueError(f"Unsupported declaration: {item}")
    return "\n".join(lines)


def rules(source, depth=0):
    indent = "  " * depth
    parts = []
    for item in tinycss2.parse_stylesheet(source, skip_whitespace=True):
        if item.type == "comment":
            parts.append(indent + "/*" + item.value.strip() + "*/")
            continue
        if item.type == "qualified-rule":
            heading = tinycss2.serialize(item.prelude).strip()
            body = declarations(item.content, indent + "  ")
        elif item.type == "at-rule":
            prelude = tinycss2.serialize(item.prelude).strip()
            heading = "@" + item.at_keyword + (" " + prelude if prelude else "")
            if item.content is None:
                parts.append(indent + heading + ";")
                continue
            if item.at_keyword.lower() in {"viewport", "font-face", "page"}:
                body = declarations(item.content, indent + "  ")
            else:
                body = rules(tinycss2.serialize(item.content), depth + 1).rstrip()
        else:
            raise ValueError(f"Unsupported CSS rule: {item}")
        parts.append(indent + heading + " {\n" + body + "\n" + indent + "}")
    return "\n\n".join(parts) + "\n"


def format_style(source):
    expressions = []
    def protect(match):
        expressions.append(match[0])
        return f"__JINJA_VALUE_{len(expressions) - 1}__"
    protected = re.sub(r"{{.*?}}", protect, source, flags=re.S)
    formatted = rules(protected)
    for index, expression in enumerate(expressions):
        formatted = formatted.replace(f"__JINJA_VALUE_{index}__", expression)
    return formatted


def main():
    check = "--check" in sys.argv[1:]
    changed = []
    paths = sorted((ROOT / "static" / "css").rglob("*.css"))
    paths += sorted((ROOT / "templates" / "styles").rglob("*.css.jinja"))
    for path in paths:
        source = path.read_text(encoding="utf-8")
        if "{%" in source:
            continue
        formatted = format_style(source)
        if source != formatted:
            changed.append(str(path.relative_to(ROOT)))
            if not check:
                path.write_text(formatted, encoding="utf-8")
    if check and changed:
        print("Styles need formatting: " + ", ".join(changed))
        raise SystemExit(1)
    print(f"Checked {len(paths)} stylesheets; {len(changed)} {'need formatting' if check else 'formatted'}.")


if __name__ == "__main__":
    main()
