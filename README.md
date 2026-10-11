# OP-CO Marine — website

Static site, no build step needed to host (Netlify: build command blank, publish directory `/`).

## Pages
- `index.html` — home (hero, about, services, projects with pop-ups, team, contact)
- `services/*.html` — the ten service detail pages (same URLs as the original Wix site)
- `products.html` — Our Products + "Get a quote" form (the original site's "More → Our Products")
- `terms.html`, `privacy.html` — legal (**paste exact legal wording before launch**)
- `_redirects` — keeps old Wix URLs (/general-4, /services-4, /terms-and-conditions …) working

## Editing content
All page content (services, products, projects) lives in `build.py`. Edit, then run `python3 build.py`.

### Project pop-ups
Click a project card to open its pop-up. The original site's pop-up text/photos weren't retrievable, so each
currently shows size, title and category. To add real content, fill `PROJECT_DETAILS` in `build.py`:

    PROJECT_DETAILS = {1: {"desc": "What we did…", "imgs": ["023e89_xxxx~mv2.jpg"]}}   # key = project number

## Photos
Photos are loaded from the original Wix CDN until you self-host them. To download them all (run on a computer with
normal internet access):

    python3 fetch_images.py && python3 build.py

then commit `assets/photos/`. Optional extras: `assets/photos/hero.jpg` (hero background) and
`service-1.jpg … service-4.jpg` (backgrounds for the four service cards); `assets/video/hero.mp4` (hero video).

## Forms
The contact and quote forms open the visitor's email app. Swap in Netlify Forms / Formspree for direct submission.
