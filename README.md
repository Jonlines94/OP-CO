# OP-CO Marine — website

Static site (no build step needed to host). Open `index.html` or upload the folder to any web host.

- `index.html` — main page (generated from `index.template.html` + `build.py`)
- `terms.html`, `privacy.html` — legal pages (**paste exact legal wording in before launch**)
- `assets/` — CSS, JS, logo, team photo

## Edit projects
Edit the `PROJECTS` list in `build.py`, then run `python3 build.py`.

## Hero video
Drop your video at `assets/video/hero.mp4` (the page falls back to the original Wix-hosted video, then to an animated gradient).

## Team photo
The page tries the full-resolution Wix image first, falling back to `assets/img/team.jpg` (low-res). Replace `team.jpg` with the original for best quality.

## Contact form
Opens the visitor's email app addressed to Info@OP-CO.co.uk. For a true "send" form, connect Formspree/Netlify Forms/etc. in `assets/js/main.js`.
