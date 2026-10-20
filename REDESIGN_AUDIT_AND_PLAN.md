# Mayur Prabhune Website Redesign — Audit and Plan

## Phase 1: Audit

### Application and routes

- Flask application factory: `app/__init__.py`; WSGI entry: `wsgi.py`.
- Public routes in `app/routes/main.py`: `/`, `/about`, `/services`, `/premium-product-sales-training`, `/contact`, `/videos`, `/video/<slug>`, `/testimonials`, `/blog`, `/success-stories`, `/success-stories/<slug>`.
- Blog routes are registered under `/blog` in `app/routes/blog.py` and expose post listing/detail endpoints.
- Admin, authentication and JSON API routes are separate blueprints; the JSON API has a login gate.
- SQLAlchemy models support posts, videos, testimonials, contact messages, case studies, client logos and users.
- The contact form uses the existing database/email workflow and Flask-WTF CSRF protection. Keep its field contract and endpoint.
- Railway builds from the existing Dockerfile and starts `wsgi:app` with Gunicorn. Do not change deployment configuration or deploy from this task.

### Current issues and risks

- The public site has inconsistent Tailwind utility styling, bright cyan/magenta glow effects, a fixed header that consumes vertical space, and repeated hero patterns.
- Tailwind is loaded from a CDN; existing blog/video/admin-facing public templates use utility classes. Keep it for legacy pages in this change to avoid silently breaking their layout; removing it needs a complete stylesheet migration.
- The case-study detail route references `case_study_detail.html`, which is absent from the template directory. Add the missing template using the existing case-study model.
- Footer links currently point to `#` and should be replaced with real destinations or removed.
- Existing template metadata lacks canonical and Open Graph tags, and the app has no sitemap/robots routes.
- Contact form CSRF is enabled, but add a honeypot and explicit length checks as a light spam barrier without a new dependency. Preserve the database/email workflow.
- `Config` contains development fallbacks for secret/admin values and `.env.example` advertises weak admin placeholders. These are separate configuration risks; do not expose them in the redesign and verify Railway secrets before any production change.
- Two portrait assets include a visible Meta AI watermark. Their authenticity is unverified; do not present them as a real-person photograph. Use original abstract artwork until Mayur supplies an approved genuine portrait.
- No source in the application verifies role dates, employers, credentials, quantified outcomes, Charlie AI or BitBloom project details. Do not publish a career timeline or named project without evidence.
- Case studies, testimonials, videos and posts are CMS-backed. Render only published/approved records and do not add seeded or made-up examples.
- `app/linkedin_integration.py` returns hard-coded sample articles rather than live LinkedIn content. Do not show those as published posts or testimonials.

### Functionality to preserve

- Existing Flask blueprints, route URLs, auth/admin screens, protected API, database schema and migrations.
- Published posts, videos, testimonials, case studies and their detail routes.
- Contact form POST, CSRF, validation, message persistence and notification emails.
- Existing canonical page paths; add metadata and sitemap coverage without renaming indexed URLs.

## Phase 2: Design plan

### Creative direction

Create an original “AI command centre” for a person-led portfolio: deep midnight surfaces, quiet slate panels, crisp white typography, and selective cyan/violet light. Use a readable 12-column desktop grid and four-column mobile grid. Keep labels compact and editorial copy generous. Avoid automotive motifs, copied controls, synthetic performance metrics, and decorative glass panels without purpose.

Use a lightweight SVG/CSS neural constellation as the hero illustration. It should represent the connection between AI, learning and frontline enablement; it is not a dashboard with fabricated data. Use motion to reveal the illustration and key sections, with reduced-motion support and static content available by default.

### Page and section structure

- **Home:** cinematic positioning, two primary CTAs, expertise modules, published project cards, approved testimonials/posts/videos when present, and clear contact CTA.
- **Expertise/Services:** corporate AI training, generative/agentic AI workshops, learning strategy and retail/sales enablement, using only currently supported claims; cross-link premium-product training.
- **Premium product sales training:** preserve `/premium-product-sales-training`; explain customer discovery, product-value conversations and practice without claiming a category or client outcome not supplied.
- **About:** authentic first-person positioning and a portrait slot only for an approved real portrait. Omit career timeline until reliable dates/roles are supplied.
- **Projects:** use published CMS case studies only. Each card links to its existing detail route; implement the missing detail template.
- **Insights:** preserve existing blog listing/detail behavior and improve shared navigation/style where safe.
- **Contact:** preserve existing POST flow, add accessible topic selection routed into the message text, field limits, honeypot, and visible success/error states.

### Motion and accessibility

- CSS/SVG-only hero movement; no WebGL or large motion dependency.
- Use IntersectionObserver for one-time section reveals and pause decorative motion when the tab is hidden.
- Pointer tilt only for fine-pointer devices; no pointer-only content or controls.
- Honor `prefers-reduced-motion`, keep focus rings visible, ensure touch targets, semantic headings, and accessible nav labels.

### SEO and implementation

- Keep public URLs; provide unique titles/descriptions, canonical URL, Open Graph title/description/URL, and accurate Person schema.
- Add a sitemap covering static pages and published dynamic content, plus a robots route referencing it.
- Reuse Flask/Jinja and SQLAlchemy. No new frontend framework or schema changes.
- A minimal Flask `test_client` run was used for route and form verification rather than the repository's browser scripts; those scripts target a fixed localhost service and one submits through the live contact flow.
- Do not deploy from this task. Railway is configured for manual deploys, so a reviewed commit must be deployed by the site owner.

## Phase 3: Implementation delivered

- Rebuilt the shared public shell and the home, about, services, premium product sales training, contact, insights, videos, testimonials, project listing, blog detail, video detail and case-study detail pages while retaining the existing route paths and content models.
- Added a responsive dark visual system with a custom CSS/SVG neural hero, reduced-motion support, section reveals, accessible expertise tabs, pointer-only microinteractions, mobile navigation and visible keyboard focus.
- Added per-page title and description support, canonical URLs on the custom domain, Open Graph/Twitter metadata, Person structured data, and domain-stable `robots.txt` and dynamic `sitemap.xml` routes.
- Removed fabricated LinkedIn samples and fake video schema. Public items are rendered only from published or approved CMS records. No unverified career timeline, client outcome or synthetic portrait was added.
- Preserved the existing Flask factory, admin/auth/API blueprints, database schema, CSRF, contact storage and email notifications. Contact submissions now validate lengths and use a honeypot; notification failure after a successful save is logged without falsely reporting storage failure.
- Added the previously missing case-study detail template and kept the Tailwind CDN for legacy content/admin-compatible templates. No dependency, schema, or Railway configuration changes were made.

## Phase 4: Verification

- `git diff --check`: passed; Git reports only expected working-tree line-ending normalization notices.
- In-memory SQLite Flask test client: `200` for home, about, services, premium training, contact, videos, testimonials, blog, case studies, `robots.txt`, `sitemap.xml`, and health.
- Contact POST: redirected successfully and persisted a record to the isolated in-memory database; mail was suppressed.
- Seeded in-memory published post, video and case study detail routes returned `200`; generated sitemap included published detail URLs under `https://mayurprabhune.in`.
- A visual browser preview was attempted, but the local dev server port is blocked by the desktop environment's socket policy. No external or production site was changed.

### Public profile and social feed source check (2026-10-20)

- The LinkedIn URL already linked by the site resolves to the Mayur Prabhune profile headed “MAYUR PRABHUNE - Dyson”. Its public summary describes AI-enabled learning, sales capability, and workforce transformation; visible credentials include agentic AI fundamentals, Microsoft Copilot, generative AI, project management, Apple Pro Products technician, and SaaS sales certifications. A profile header location of Bengaluru conflicts with the existing site's Pune schema; location was not changed pending owner confirmation.
- The live homepage labels `/static/images/Profile1.jpg` as Mayur Prabhune's headshot. The owner explicitly asked to use that existing site asset in the redesign. It includes a visible Meta AI watermark, so the site should not describe it as an independently verified photograph.
- The Instagram profile `@aiwali_duniya` publicly links back to `mayurprabhune.in` and labels the account as an AI education creator. Instagram presents a sign-in gate on the Reels page, so no individual reel content or permanent Reel URLs were verified. The profile is linked in the site's footer and Person `sameAs` metadata; no unverified reel was embedded.
- The repository's `LinkedInBlogFetcher` did not make a live request; it returned fabricated post copy, dates, and engagement counts. Those mock items were removed. Live member-post retrieval requires an authorized LinkedIn API integration and the restricted `r_member_social` permission. Instagram feed retrieval needs an authorized Meta Instagram API connection for the account. Do not add tokens to source control or chat.

## Handoff and follow-up

- Current branch: `website/audit-trust-security`.
- Changes are local only. No push, pull request or Railway deployment was performed.
- Before a public release, replace the abstract hero with a genuine approved portrait if desired, publish verified career details and outcome-backed case studies, verify Railway secrets, and review the rendered pages on the deployed domain after the owner performs the manual deploy.
- Recurring content and SEO work still needs a defined review cadence and a human-approved source of new facts; no automatic publishing or deployment should create unsupported claims.
