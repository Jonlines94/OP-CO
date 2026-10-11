#!/usr/bin/env python3
"""OP-CO site generator.

    python3 build.py

Generates index.html, products.html and every services/*.html page.
Content lives in the data blocks below — edit there, then rebuild.

Images: each entry in IMAGES is the original Wix-hosted file. If a copy exists in
assets/photos/ (run `python3 fetch_images.py` on a computer with internet access to
download them all) the local copy is used, otherwise the Wix URL is used.
"""
import html, pathlib, re

ROOT = pathlib.Path(__file__).parent
E = html.escape
WIX = "https://static.wixstatic.com/media/"

# --------------------------------------------------------------------------
# Images (original Wix media ids)
# --------------------------------------------------------------------------
def img_url(media_id: str, base: str) -> str:
    local = media_id.replace("~mv2", "")
    if (ROOT / "assets" / "photos" / local).exists():
        return f"{base}assets/photos/{local}"
    return WIX + media_id

ALL_IMAGES: set[str] = set()

# --------------------------------------------------------------------------
# Service pages  (slug -> content). Slugs match the original site's URLs.
# --------------------------------------------------------------------------
CONTACT_CTA = "See our most recent technical and consultancy projects"

SERVICES = [
    dict(slug="superyacht-equipment-installation", title="Technical Equipment Installation", nav="Equipment installation",
         paras=["OP-CO Marine Services offers expert mechanical engineering equipment installation, supporting clients from early concept through installation to final commissioning.",
                "Equipment is installed safely and efficiently, and in full compliance with technical specifications and client requirements."],
         imgs=[("023e89_d72463b35e474a12a1e7f1c8db5fc92a~mv2.jpg", "Lifting pump"),
               ("023e89_299b3aff72694c07904ad2adc8332366~mv2.jpeg", "Equipment installation on board"),
               ("023e89_6e2d8d211cc74c5aafc5611e3570a59e~mv2.jpg", "Installation work")],
         meta="Specialist superyacht mechanical equipment installation, delivered to the highest technical and safety standards."),
    dict(slug="superyacht-electrical-upgrades-installations", title="Electrical Upgrades, Repairs & Installations", nav="Electrical upgrades & repairs",
         paras=["OP-CO specialises in marine electrical systems, including power distribution, lighting, automation, and navigation.",
                "We deliver upgrades, repairs, and installations with a focus on safety, reliability, and long-term performance."],
         imgs=[("023e89_578ec91378ce4e3588ad5e41023cb7ac~mv2.jpg", "Electrical installation"),
               ("023e89_cb811319bb6a400c81e520977ffdd598~mv2.png", "Electrical systems"),
               ("023e89_a28814834b004a26889d2bd58a834c4a~mv2.jpg", "Marine electrical work")],
         meta="Specialist superyacht electrical upgrades, repairs and installation services."),
    dict(slug="superyacht-fabrication-welding", title="Fabrication & Welding", nav="Fabrication & welding",
         paras=["Our team carries out controlled welding and fabrication using suitable materials and techniques, with an emphasis on precision, reliability and a clean, professional finish."],
         imgs=[("023e89_d415fd7aae704808890dbf1089be2bfe~mv2.jpg", "Fabrication work"),
               ("023e89_70936ebf290d4661a5c98db8cab851d2~mv2.png", "Welding"),
               ("023e89_7b0548fa423548db8e53d07d5b4550c1~mv2.jpg", "Stainless fabrication")],
         meta="Specialist superyacht fabrication and welding for refit, repair and new build projects, with precision workmanship and high-quality finishes."),
    dict(slug="machinery-servicing", title="Machinery Servicing", nav="Machinery servicing",
         paras=["We provide reliable machinery servicing, ensuring optimal performance, safety and longevity."],
         imgs=[("023e89_d415fd7aae704808890dbf1089be2bfe~mv2.jpg", "Machinery servicing"),
               ("023e89_70936ebf290d4661a5c98db8cab851d2~mv2.png", "Engine room work"),
               ("023e89_7b0548fa423548db8e53d07d5b4550c1~mv2.jpg", "Servicing")],
         meta="Reliable superyacht machinery servicing for performance, safety and longevity."),
    dict(slug="tank-cleaning-and-repairs", title="Tank Cleaning & Repairs", nav="Tank cleaning & repairs",
         paras=["OP-CO offers complete tank cleaning for all tank types, along with professional touch-ups and repair work."],
         imgs=[("023e89_ad325033af5b4af1b6cc02aa8be39df8~mv2.jpg", "Tank cleaning")],
         meta="Complete superyacht tank cleaning, inspections, touch-ups and repairs."),
    dict(slug="air-quality-management-luxury-homes", title="Air Quality Management", nav="Air quality management",
         paras=["OP-CO offers premium air quality management for UHNW family estates, with tailored solutions for healthier, cleaner luxury living environments."],
         imgs=[("7f2c44_8c1e68c105e947e58a9f9dbb88280286~mv2.png", "Air quality management"),
               ("7f2c44_60b7c248bdc8457ea9137a7f16832438~mv2.jpg", "Air quality")],
         meta="Premium air quality management for UHNW family estates."),
    dict(slug="avit-projects", title="AVIT Projects", nav="AVIT projects",
         paras=["In partnership with marinetechnology.fr, OP-CO offers captains and crew behind-the-scenes support to meet guest needs."],
         sections=[("TV Subscription Services", ["Private TV subscriptions that keep guests current on shows, sports, and movies from around the world."]),
                   ("Media Content Procurement and Distribution", ["Media content is sourced and streamed to the vessel at any time."]),
                   ("Maintenance & Support", ["A remote IT and network support service that acts as a “Virtual ETO” — aimed at vessels without onboard IT or network expertise that want an extra layer of technical support.",
                                              "Subscribers can reach experienced engineers who guide them through onboard issues."])],
         deliver=["24/7 global support", "Priority service assistance", "Remote system aid", "Ready-to-ship spare parts", "Service level agreements",
                  "Planned maintenance and risk inventory", "Monthly reporting on systems, and risk reports", "On-board systems training", "Content and connectivity packages"],
         imgs=[("7f2c44_5e23dfcc3b8643f1817279cccbcde8f8~mv2.png", "Superyacht AV system"),
               ("7f2c44_6542e82c510d4c319b8aa932ac353aa4~mv2.jpg", "AVIT installation")],
         meta="AV, IT and TV subscription services and support for superyachts."),
    dict(slug="uhnw-family-estate-management", title="UHNW Family Estates", nav="UHNW family estate management",
         paras=["OP-CO offers discreet UHNW family estate management, maintenance and luxury interior solutions across private residences and global portfolios."],
         imgs=[("7f2c44_21dc6ae6c30145009d2a66c908d7d3da~mv2.jpg", "Family estate"),
               ("7f2c44_ed6c1c0887044a888cca3e03d0014d46~mv2.jpg", "Estate interior")],
         meta="Discreet UHNW family estate management, maintenance and luxury interior solutions."),
    dict(slug="security-systems", title="Security Systems", nav="Security systems",
         paras=["High-end security systems for luxury homes and estates. OP-CO delivers protection solutions tailored to UHNW clients."],
         imgs=[("7f2c44_2c6ffb4c60914a04a7fb203cb4cedce5~mv2.jpeg", "Security installation"),
               ("7f2c44_2a9b596a95b14db18e770a2cad7c054e~mv2.jpeg", "Security systems")],
         meta="High-end security systems for luxury homes and estates."),
    dict(slug="superyacht-carpentry", title="Carpentry Projects", nav="Carpentry",
         paras=["OP-CO offers complete carpentry solutions, taking a project from initial concept and design through to high-quality installation."],
         imgs=[("023e89_42db2895f8b7412ab7e232b6b1839e81~mv2.jpeg", "Interior carpentry"),
               ("023e89_68a3a50eb0ff48a09448009624c22480~mv2.jpeg", "Carpentry installation")],
         meta="Specialist superyacht interior carpentry installation with precision-crafted, high-quality finishes."),
]
SERVICE_BY_NAV = {s["nav"]: s["slug"] for s in SERVICES}

# --------------------------------------------------------------------------
# Products page ("Our Products", under the original site's "More" menu)
# --------------------------------------------------------------------------
PRODUCTS_INTRO = ("Our product catalogue is small but effective, built from our experience with real technical problems. "
                  "We source equipment in partnership with leading OEMs and select products that have been tested against our standards. "
                  "Products can be customised to your operational needs, with an emphasis on reliability and safety drawn from years of maritime experience.")
PRODUCTS = [
    ("RRR Oil Filtration", "2e97da_ac4ca58b997c47848b26bed7ba2e9c6d~mv2.jpg",
     "An all-in-one system that removes solid particles, water, sludge and oxidation residue from oil — the first cleaners to offer “total cleaning” of industrial hydraulic and lube oil."),
    ("Microbe Marine Oxygen Cluster Units", "2e97da_a2457bd8a661442ca028b6c256d0cfa1~mv2.png",
     "Oxygen cluster generators, customised to your requirements, that kill bacteria, sanitise surfaces and help reduce the spread of harmful viruses."),
    ("Ultraguard Antifouling", "2e97da_07650ca2bc6c469fbb241c7c7e5edabd~mv2.png",
     "An environmentally friendly way to prevent marine growth and biofouling on hulls, sea chests, plate coolers and box coolers."),
    ("Enluse Lubrication Management", "2e97da_98bf2a13f0ab4cdca89739b3072476a4~mv2.jpg",
     "A range of products for transferring, storing and identifying lubricating oil, intended to protect lubricants and extend equipment life in the engine room."),
    ("Custom Fabrications", "2e97da_a7f064b15bcc41478d9a6ea5d2336167~mv2.jpg",
     "Bespoke specialist equipment and parts made to meet nearly any requirement."),
    ("Engineering Parts Supply", "2e97da_4f84b40f2e934253ae420eb21174173a~mv2.jpg",
     "UK and EU offices that help you procure a wide range of products."),
]

# --------------------------------------------------------------------------
# Projects.  (size, title, category).  size "" = no size tag.
# Add pop-up content for any project in PROJECT_DETAILS, keyed by its 1-based
# position in this list:  {7: {"desc": "…", "imgs": ["media-id~mv2.jpg", …]}}
# --------------------------------------------------------------------------
CATS = {"consult": "Consultancy", "tanks": "Tanks & coatings", "fab": "Fabrication",
        "carp": "Carpentry", "elec": "Electrical", "sys": "Systems & installs"}
PROJECTS = [
    ("110M+", "Fresh water valves upgrade", "sys"), ("70M+", "Tank cleaning and touch ups", "tanks"),
    ("110M+", "Tank cleaning and touch ups", "tanks"), ("60M+", "Replacement of sea strainers", "sys"),
    ("60M+", "Pipe work lagging", "sys"), ("110M+", "New build operational setup consultancy project", "consult"),
    ("", "Technical report for confidential legal case", "consult"), ("110M", "Fire hydrant replacement shipwide", "sys"),
    ("60M+", "Tank cleaning and touch ups", "tanks"), ("110M+", "Deck wash booster pumps", "sys"),
    ("60M+", "Custom fabrication", "fab"), ("110M+", "Interior storage install", "carp"),
    ("60M+", "Custom fabrication", "fab"), ("50M+", "Vent line inspection", "sys"),
    ("100M+", "Condensate drain lift pump install", "sys"), ("75M", "Alternator rewind and rebuild", "elec"),
    ("100M+", "New build technical consultancy project", "consult"), ("110M+", "Carpentry projects", "carp"),
    ("80M+", "Fire and safety systems consultancy", "consult"), ("60M+", "ER workbench install", "fab"),
    ("120M+", "Fire hydrants chrome coating", "tanks"), ("70M+", "Air quality management consultancy project", "consult"),
    ("100M", "Weathertight sliding door service", "sys"), ("75M", "500kW generator alternator removal", "elec"),
    ("75M", "Electrical fault finding", "elec"), ("100M", "Class approved penetrations", "fab"),
    ("110M", "Tank cleaning and coating project", "tanks"), ("60M", "Stainless steel fabrications", "fab"),
    ("100M", "Interior carpentry projects", "carp"), ("100M", "Stainless welding and polishing", "fab"),
    ("65M", "UPS project", "elec"), ("60M", "Chilled water system cleaning", "sys"),
    ("100M", "Crew area carpentry projects", "carp"), ("110M", "5 axis CNC machine fabrication project", "fab"),
    ("65M", "KNX lighting project", "elec"),
]
PROJECT_DETAILS: dict[int, dict] = {}
assert len(PROJECTS) == 35

# --------------------------------------------------------------------------
# Shared fragments
# --------------------------------------------------------------------------
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500'
         '&family=Inter:wght@300;400;500;600&display=swap">')

def nav(base: str, home: bool) -> str:
    a = (lambda frag: f"#{frag}") if home else (lambda frag: f"{base}index.html#{frag}")
    top = "#top" if home else f"{base}index.html"
    return f'''<header class="nav" id="nav">
  <div class="nav__in">
    <a class="nav__logo" href="{top}" aria-label="OP-CO Marine — home"><img src="{base}assets/img/logo.png" alt="OP-CO" width="88" height="24"></a>
    <nav class="nav__links" id="navlinks" aria-label="Primary">
      <a href="{top}">Home</a>
      <a href="{a('about')}">About</a>
      <a href="{a('services')}">Services</a>
      <a href="{a('projects')}">Projects</a>
      <a href="{a('team')}">Our Team</a>
      <div class="nav__more">
        <button type="button" class="nav__morebtn" aria-expanded="false" aria-haspopup="true">More</button>
        <div class="nav__sub">
          <a href="{base}products.html">Our Products</a>
          <a href="{base}terms.html">Terms and Conditions</a>
          <a href="{base}privacy.html">Privacy and data protection</a>
        </div>
      </div>
      <a href="{a('contact')}" class="nav__cta">Contact</a>
    </nav>
    <button class="nav__burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="navlinks"><span></span><span></span></button>
  </div>
</header>'''

def footer(base: str) -> str:
    svc = "".join(f'<li><a href="{base}services/{s["slug"]}.html">{E(s["title"])}</a></li>' for s in SERVICES)
    return f'''<footer class="foot">
  <div class="wrap">
    <div class="foot__cols">
      <div><img src="{base}assets/img/logo.png" alt="OP-CO" width="95" height="26" loading="lazy"><p>Marine engineering — refit and repair, worldwide.</p></div>
      <div><h5>Contact</h5><ul><li><a href="tel:+442382256732">023 8225 6732</a></li><li><a href="mailto:Info@OP-CO.co.uk">Info@OP-CO.co.uk</a></li><li><a href="mailto:Sales@OP-Co.co.uk">Sales@OP-Co.co.uk</a></li></ul></div>
      <div><h5>Find Us</h5><ul><li>OP-CO Marine Ltd</li><li>Unit 3, The Boatyard</li><li>Endeavour Way</li><li>Hythe, Southampton</li><li>SO45 6LA</li></ul></div>
      <div><h5>Services</h5><ul>{svc}<li><a href="{base}products.html">Our Products</a></li></ul></div>
      <div><h5>Legal</h5><ul><li><a href="{base}terms.html">Terms and Conditions</a></li><li><a href="{base}privacy.html">Privacy and data protection</a></li></ul>
        <h5 style="margin-top:22px">Follow</h5><ul><li><a href="https://www.instagram.com/opco_marine?igsh=a210bGZ0aGpxazZ0" target="_blank" rel="noopener">Instagram</a></li><li><a href="https://www.linkedin.com/company/op-co-marine/posts/?feedView=all" target="_blank" rel="noopener">LinkedIn</a></li><li><a href="https://www.facebook.com/people/OP-CO/100091286894781/" target="_blank" rel="noopener">Facebook</a></li></ul></div>
    </div>
    <div class="foot__base"><span>© <span id="yr">2026</span> OP-CO Marine Ltd. All rights reserved.</span><span>Southampton, United Kingdom</span></div>
  </div>
</footer>'''

def head(title: str, desc: str, base: str) -> str:
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)} | OP-CO</title>
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#0a0908">
<meta property="og:title" content="{E(title)} | OP-CO"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="website"><meta property="og:site_name" content="OP-CO Marine">
<link rel="icon" href="{base}assets/img/favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="32x32" href="{base}assets/img/favicon-32.png"><link rel="apple-touch-icon" href="{base}assets/img/apple-touch-icon.png">
{FONTS}
<link rel="stylesheet" href="{base}assets/css/style.css">
<script>document.documentElement.classList.add('js')</script>
</head>'''

def figure(media_id: str, alt: str, base: str) -> str:
    ALL_IMAGES.add(media_id)
    return (f'<figure class="gal__item" data-reveal><img src="{img_url(media_id, base)}" alt="{E(alt)}" loading="lazy" '
            f'onerror="this.parentNode.remove()"></figure>')

CONTACT_BAND = '''<section class="sec contact contact--band" data-nav="dark" aria-labelledby="cb-h">
  <div class="wrap">
    <div class="sec__head"><p class="eyebrow" data-reveal>Contact</p><h2 class="h-md" id="cb-h" data-reveal>Speak to our team</h2></div>
    <div class="band" data-reveal>
      <div class="detail"><small>Phone</small><a href="tel:+442382256732">023 8225 6732</a></div>
      <div class="detail"><small>Email</small><a href="mailto:Info@OP-CO.co.uk">Info@OP-CO.co.uk</a><a href="mailto:Sales@OP-Co.co.uk">Sales@OP-Co.co.uk</a></div>
      <div class="detail"><small>Find us</small><address>OP-CO Marine Ltd, Unit 3, The Boatyard<br>Endeavour Way, Hythe, Southampton SO45 6LA</address></div>
    </div>
  </div>
</section>'''

def page(title, desc, base, inner):
    return (head(title, desc, base) + "\n<body>\n<a class=\"skip\" href=\"#main\">Skip to content</a>\n" + nav(base, False) +
            f"\n<main id=\"main\">\n{inner}\n</main>\n" + footer(base) + f'\n<script src="{base}assets/js/main.js" defer></script>\n</body>\n</html>\n')

# --------------------------------------------------------------------------
# Build: service pages
# --------------------------------------------------------------------------
def build_service(s):
    base = "../"
    body = "".join(f"<p>{E(p)}</p>" for p in s.get("paras", []))
    for h, ps in s.get("sections", []):
        body += f"<h2>{E(h)}</h2>" + "".join(f"<p>{E(p)}</p>" for p in ps)
    if s.get("deliver"):
        body += "<h2>We can deliver</h2><ul class=\"tick\">" + "".join(f"<li>{E(i)}</li>" for i in s["deliver"]) + "</ul>"
    gal = "".join(figure(m, a, base) for m, a in s.get("imgs", []))
    n = len(s.get("imgs", []))
    inner = f'''<section class="phero" data-nav="dark">
  <div class="wrap">
    <a class="crumb" href="{base}index.html#services">‹ All services</a>
    <p class="eyebrow" data-reveal>Services</p>
    <h1 class="h-lg" data-reveal style="--d:.05s">{E(s["title"])}</h1>
  </div>
</section>
<section class="sec pbody" data-nav="light">
  <div class="wrap">
    <div class="pbody__text" data-reveal>{body}</div>
    <div class="gal gal--{min(n,3)}">{gal}</div>
    <p class="pbody__cta" data-reveal><a class="btn" href="{base}index.html#projects">{CONTACT_CTA}</a></p>
  </div>
</section>
{CONTACT_BAND}'''
    out = ROOT / "services"; out.mkdir(exist_ok=True)
    (out / f'{s["slug"]}.html').write_text(page(s["title"], s["meta"] if "meta" in s else s["paras"][0], base, inner), encoding="utf-8")

for s in SERVICES:
    build_service(s)

# --------------------------------------------------------------------------
# Build: products page
# --------------------------------------------------------------------------
cards = ""
for name, mid, desc in PRODUCTS:
    ALL_IMAGES.add(mid)
    cards += (f'<article class="prod" data-reveal><figure class="prod__img"><img src="{img_url(mid, "")}" alt="{E(name)}" loading="lazy" '
              f'onerror="this.parentNode.classList.add(\'is-empty\');this.remove()"></figure><h3>{E(name)}</h3><p>{E(desc)}</p></article>')
products_inner = f'''<section class="phero" data-nav="dark">
  <div class="wrap">
    <p class="eyebrow" data-reveal>More</p>
    <h1 class="h-lg" data-reveal style="--d:.05s">Our Products</h1>
    <p class="lead" data-reveal style="--d:.1s;max-width:720px;margin-top:22px">{E(PRODUCTS_INTRO)}</p>
  </div>
</section>
<section class="sec sec--alt" data-nav="light">
  <div class="wrap"><div class="prods">{cards}</div></div>
</section>
<section class="sec contact" id="quote" data-nav="dark" aria-labelledby="q-h">
  <div class="wrap">
    <div class="sec__head"><p class="eyebrow" data-reveal>Enquiries</p><h2 class="h-lg" id="q-h" data-reveal>Get a quote</h2>
      <p class="lead" data-reveal>Tell us what you need and we’ll come back to you.</p></div>
    <form class="form form--narrow" data-mailto="Sales@OP-Co.co.uk" data-subject="Product quote request" data-reveal novalidate>
      <div class="two">
        <div class="field"><input id="q-fn" name="first" placeholder=" " autocomplete="given-name" required><label for="q-fn">First name</label></div>
        <div class="field"><input id="q-ln" name="last" placeholder=" " autocomplete="family-name" required><label for="q-ln">Last name</label></div>
      </div>
      <div class="field"><input id="q-em" name="email" type="email" placeholder=" " autocomplete="email" required><label for="q-em">Email</label></div>
      <div class="field"><textarea id="q-msg" name="message" placeholder=" "></textarea><label for="q-msg">Which products are you interested in?</label></div>
      <button class="btn" type="submit">Send</button>
      <p class="form__note" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>'''
(ROOT / "products.html").write_text(page("Our Products", "OP-CO's small but effective product catalogue: oil filtration, antifouling, lubrication management, custom fabrications and engineering parts supply.", "", products_inner), encoding="utf-8")

# --------------------------------------------------------------------------
# Build: index
# --------------------------------------------------------------------------
tpl = (ROOT / "index.template.html").read_text(encoding="utf-8")

proj_cards = []
for i, (size, title, cat) in enumerate(PROJECTS, 1):
    det = PROJECT_DETAILS.get(i, {})
    top = (f'<div class="proj__size">{E(size)}<small>Superyacht</small></div>' if size
           else '<div class="proj__size">Report<small>Technical</small></div>')
    imgs = []
    for mid in det.get("imgs", []):
        ALL_IMAGES.add(mid); imgs.append(img_url(mid, ""))
    attrs = (f'data-cat="{cat}" data-size="{E(size)}" data-title="{E(title)}" data-catlabel="{E(CATS[cat])}" '
             f'data-desc="{E(det.get("desc", ""))}" data-imgs="{E("|".join(imgs))}"')
    proj_cards.append(
        f'<article class="proj" {attrs} tabindex="0" role="button" aria-haspopup="dialog" aria-label="{E(title)} — view project">{top}'
        f'<div><h3>{E(title)}</h3><p class="proj__tag">{E(CATS[cat])}<span class="proj__go" aria-hidden="true">View</span></p></div></article>')

used = [k for k in CATS if any(p[2] == k for p in PROJECTS)]
chips = ['<button class="chip" type="button" data-cat="all" aria-pressed="true">All</button>']
chips += [f'<button class="chip" type="button" data-cat="{k}" aria-pressed="false">{E(CATS[k])}</button>' for k in used]

# link service chips to their detail pages
def link_chip(m):
    text = html.unescape(m.group(1))
    slug = SERVICE_BY_NAV.get(text)
    return f'<li><a href="services/{slug}.html">{m.group(1)}</a></li>' if slug else m.group(0)
tpl = re.sub(r"<li>([^<]+)</li>", link_chip, tpl)

out = (tpl.replace("<!--PROJECTS-->", "\n      ".join(proj_cards)).replace("<!--FILTERS-->", "\n      ".join(chips))
          .replace("<!--NAV-->", nav("", True)).replace("<!--FOOTER-->", footer("")))
(ROOT / "index.html").write_text(out, encoding="utf-8")

# manifest for fetch_images.py
(ROOT / "images.txt").write_text("\n".join(sorted(ALL_IMAGES)) + "\n", encoding="utf-8")
print(f"built index.html ({len(PROJECTS)} projects), products.html, {len(SERVICES)} service pages, {len(ALL_IMAGES)} images in manifest")
