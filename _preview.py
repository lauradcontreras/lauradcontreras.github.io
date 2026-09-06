#!/usr/bin/env python3
"""Approximate local renderer so the design can be reviewed without Jekyll.

Handles only the small Liquid subset used by _layouts/default.html:
{{ var }}, {{ var | relative_url }}, {% for %}...{% endfor %}, {% if %}...{% endif %},
{% seo %} and {{ content }}. Not a Jekyll substitute — preview only.
"""
import os
import re
import sys
import datetime
import yaml
import markdown

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "_preview")

MD_EXT = ["extra", "attr_list", "md_in_html", "sane_lists"]


def split_front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def deep_get(obj, dotted):
    cur = obj
    for part in dotted.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur


def render_liquid(tpl, ctx):
    # {% for x in coll %} ... {% endfor %}
    def do_for(m):
        var, coll_expr, body = m.group(1), m.group(2), m.group(3)
        coll = deep_get(ctx, coll_expr) or []
        out = []
        for item in coll:
            sub = dict(ctx)
            sub[var] = item
            out.append(render_liquid(body, sub))
        return "".join(out)

    tpl = re.sub(
        r"\{%-?\s*for\s+(\w+)\s+in\s+([\w.]+)\s*-?%\}(.*?)\{%-?\s*endfor\s*-?%\}",
        do_for, tpl, flags=re.S)

    # {% if a == b %} ... {% endif %}   (only equality, as used in the layout)
    def do_if(m):
        left, right, body = m.group(1), m.group(2), m.group(3)
        lv = deep_get(ctx, left)
        rv = deep_get(ctx, right)
        if rv is None:
            rv = right.strip("'\"")
        return render_liquid(body, ctx) if lv == rv else ""

    tpl = re.sub(
        r"\{%-?\s*if\s+([\w.]+)\s*==\s*([\w.'\"]+)\s*-?%\}(.*?)\{%-?\s*endif\s*-?%\}",
        do_if, tpl, flags=re.S)

    # {% seo %}
    title = deep_get(ctx, "page.title")
    site_title = deep_get(ctx, "site.title")
    full = f"{title} | {site_title}" if title else site_title
    tpl = tpl.replace(
        "{% seo %}",
        f"<title>{full}</title>\n<meta name=\"description\" content=\"{deep_get(ctx,'site.description') or ''}\">")

    # {{ var }} and {{ var | filter: 'x' }}
    def do_var(m):
        expr = m.group(1).strip()
        parts = [p.strip() for p in expr.split("|")]
        val = deep_get(ctx, parts[0])
        if val is None and parts[0] == "content":
            val = ctx.get("content", "")
        if val is None:
            for p in parts[1:]:
                dm = re.match(r"default:\s*'([^']*)'", p)
                if dm:
                    val = dm.group(1)
        if val is None:
            val = ""
        for p in parts[1:]:
            if p.startswith("relative_url"):
                val = str(val)
            if p.startswith("date:"):
                val = datetime.date.today().strftime("%B %Y")
        return str(val)

    tpl = re.sub(r"\{\{(.*?)\}\}", do_var, tpl, flags=re.S)
    return tpl


def main():
    site = yaml.safe_load(open(os.path.join(ROOT, "_config.yml")).read())
    site["data"] = {}
    data_dir = os.path.join(ROOT, "_data")
    for f in os.listdir(data_dir):
        site["data"][os.path.splitext(f)[0]] = yaml.safe_load(
            open(os.path.join(data_dir, f)).read())
    site["time"] = datetime.date.today().isoformat()

    layout = open(os.path.join(ROOT, "_layouts", "default.html")).read()
    os.makedirs(OUT, exist_ok=True)

    pages = [f for f in os.listdir(ROOT) if f.endswith(".md")]
    for fname in pages:
        fm, body = split_front_matter(open(os.path.join(ROOT, fname)).read())
        # resolve {{ '...' | relative_url }} inside page bodies
        body = re.sub(r"\{\{\s*'([^']+)'\s*\|\s*relative_url\s*\}\}", r"\1", body)
        html = markdown.markdown(body, extensions=MD_EXT)
        ctx = {"site": site, "page": fm, "content": html}
        out = render_liquid(layout, ctx)
        # rewrite root-absolute asset paths to local ones for the preview
        out = out.replace('src="/assets/', 'src="assets/')
        out = out.replace('href="/assets/', 'href="assets/')
        name = "index.html" if fname == "index.md" else fname.replace(".md", ".html")
        open(os.path.join(OUT, name), "w").write(out)
        print("rendered", name)


if __name__ == "__main__":
    main()
