#!/usr/bin/env python3
"""Builds index.html from index.template.html by injecting the project cards.
Edit PROJECTS below to add/remove projects, then run:  python3 build.py"""
import html, pathlib

CATS = {
    "consult": "Consultancy",
    "tanks": "Tanks & coatings",
    "fab": "Fabrication",
    "carp": "Carpentry",
    "elec": "Electrical",
    "sys": "Systems & installs",
}

# (size tag, title, category)  — size "" for projects without one
PROJECTS = [
    ("110M+", "Fresh water valves upgrade", "sys"),
    ("70M+", "Tank cleaning and touch ups", "tanks"),
    ("110M+", "Tank cleaning and touch ups", "tanks"),
    ("60M+", "Replacement of sea strainers", "sys"),
    ("60M+", "Pipe work lagging", "sys"),
    ("110M+", "New build operational setup consultancy project", "consult"),
    ("", "Technical report for confidential legal case", "consult"),
    ("110M", "Fire hydrant replacement shipwide", "sys"),
    ("60M+", "Tank cleaning and touch ups", "tanks"),
    ("110M+", "Deck wash booster pumps", "sys"),
    ("60M+", "Custom fabrication", "fab"),
    ("110M+", "Interior storage install", "carp"),
    ("60M+", "Custom fabrication", "fab"),
    ("50M+", "Vent line inspection", "sys"),
    ("100M+", "Condensate drain lift pump install", "sys"),
    ("75M", "Alternator rewind and rebuild", "elec"),
    ("100M+", "New build technical consultancy project", "consult"),
    ("110M+", "Carpentry projects", "carp"),
    ("80M+", "Fire and safety systems consultancy", "consult"),
    ("60M+", "ER workbench install", "fab"),
    ("120M+", "Fire hydrants chrome coating", "tanks"),
    ("70M+", "Air quality management consultancy project", "consult"),
    ("100M", "Weathertight sliding door service", "sys"),
    ("75M", "500kW generator alternator removal", "elec"),
    ("75M", "Electrical fault finding", "elec"),
    ("100M", "Class approved penetrations", "fab"),
    ("110M", "Tank cleaning and coating project", "tanks"),
    ("60M", "Stainless steel fabrications", "fab"),
    ("100M", "Interior carpentry projects", "carp"),
    ("100M", "Stainless welding and polishing", "fab"),
    ("65M", "UPS project", "elec"),
    ("60M", "Chilled water system cleaning", "sys"),
    ("100M", "Crew area carpentry projects", "carp"),
    ("110M", "5 axis CNC machine fabrication project", "fab"),
    ("65M", "KNX lighting project", "elec"),
]
assert len(PROJECTS) == 35

root = pathlib.Path(__file__).parent
tpl = (root / "index.template.html").read_text(encoding="utf-8")

cards = []
for size, title, cat in PROJECTS:
    e = html.escape
    if size:
        top = f'<div class="proj__size">{e(size)}<small>Superyacht</small></div>'
    else:
        top = '<div class="proj__size">Report<small>Technical</small></div>'
    cards.append(
        f'<article class="proj" data-cat="{cat}">{top}'
        f'<div><h3>{e(title)}</h3><p class="proj__tag">{e(CATS[cat])}</p></div></article>'
    )

used = [k for k in CATS if any(p[2] == k for p in PROJECTS)]
chips = ['<button class="chip" type="button" data-cat="all" aria-pressed="true">All</button>']
chips += [f'<button class="chip" type="button" data-cat="{k}" aria-pressed="false">{html.escape(CATS[k])}</button>' for k in used]

out = tpl.replace("<!--PROJECTS-->", "\n      ".join(cards)).replace("<!--FILTERS-->", "\n      ".join(chips))
(root / "index.html").write_text(out, encoding="utf-8")
print(f"index.html written — {len(cards)} projects")
