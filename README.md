# Alexa & Bruno — Wedding Invite · Deployment Guide

## Overview
A single-file static website (`alexa-bruno-wedding-invite.html`). All images and fonts are either embedded (base64) or loaded from Google Fonts CDN. No backend, no database, no build step required.

---

## Option 1 — Static hosting (recommended, simplest)

The site is a **single HTML file**. Any static host will work.

### Netlify (drag & drop, free)
1. Go to [netlify.com](https://netlify.com) → Log in
2. Drag `alexa-bruno-wedding-invite.html` onto the Netlify dashboard
3. It's live instantly at a `*.netlify.app` URL
4. To use a custom domain (e.g. `alexaybruno.com`): Site settings → Domain management → Add custom domain

### Vercel
```bash
npm i -g vercel
vercel deploy alexa-bruno-wedding-invite.html
```

### GitHub Pages
1. Create a repo (e.g. `alexa-bruno-wedding`)
2. Rename the file to `index.html`
3. Push to `main` branch
4. Settings → Pages → Source: `main` / `root`
5. Done — live at `https://username.github.io/alexa-bruno-wedding`

### Any web server (nginx / Apache)
```bash
# Rename and place in web root
cp alexa-bruno-wedding-invite.html /var/www/html/index.html
```

---

## Option 2 — Custom domain

1. Buy domain at Namecheap, GoDaddy, or Google Domains (e.g. `alexaybruno2027.com`)
2. Deploy to Netlify or Vercel as above
3. In your hosting dashboard: Add custom domain
4. In your domain registrar: Point nameservers or add CNAME/A record as instructed

---

## File structure

```
alexa-bruno-wedding-invite.html   ← the entire site, self-contained
README-deploy.md                  ← this file
```

All assets (photos, QR code) are **base64-encoded** inside the HTML — no separate image folder needed.

---

## Performance notes

- File size: ~2.5 MB (due to embedded images)
- Google Fonts are loaded from CDN — requires internet connection to display custom typography
- Fully responsive: works on mobile, tablet, and desktop
- All scroll animations work natively with IntersectionObserver (no JS libraries required)

---

## To update content

All text is in plain HTML — search for the relevant string and edit directly.

| What to change | Search for |
|---|---|
| Package price / installments | `USD 200` / `USD 175` |
| Agency contact info | `0992 404 780` |
| Date | `25 de Junio` |
| Hero phrase | `Nuestro 25 ayer` |
| Agency name | `Almacén de Viajes` |

---

## Browser support
Chrome, Safari, Firefox, Edge — all modern versions. IE not supported.

---

*Built with love for Alexa & Bruno · June 2026*
