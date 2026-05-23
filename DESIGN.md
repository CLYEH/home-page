---
version: alpha
name: Personal Portfolio — Minimal Developer
description: A minimal, modern design system for a developer portfolio. Light-first with a full dark theme, a single classic-blue accent, Inter for all UI text, and a mono face reserved for code.
colors:
  primary: "#2563EB"
  primary-hover: "#1D4ED8"
  primary-subtle: "#EFF6FF"
  primary-bright: "#60A5FA"
  on-primary: "#FFFFFF"
  surface: "#FFFFFF"
  surface-subtle: "#FAFAFA"
  on-surface: "#0A0A0A"
  on-surface-muted: "#71717A"
  border: "#E4E4E7"
  surface-dark: "#0A0A0A"
  surface-dark-subtle: "#18181B"
  on-surface-dark: "#FAFAFA"
  on-surface-dark-muted: "#A1A1AA"
  border-dark: "#27272A"
  error: "#DC2626"
  success: "#16A34A"
typography:
  headline-display:
    fontFamily: "Inter, ui-sans-serif, system-ui, sans-serif"
    fontSize: 60px
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: -0.03em
  headline-lg:
    fontFamily: "Inter, ui-sans-serif, system-ui, sans-serif"
    fontSize: 40px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: -0.02em
  headline-md:
    fontFamily: "Inter, ui-sans-serif, system-ui, sans-serif"
    fontSize: 28px
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: "Inter, ui-sans-serif, system-ui, sans-serif"
    fontSize: 20px
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: -0.01em
  body-lg:
    fontFamily: "Inter, ui-sans-serif, system-ui, sans-serif"
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.7
    letterSpacing: 0em
  body-md:
    fontFamily: "Inter, ui-sans-serif, system-ui, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.7
    letterSpacing: 0em
  body-sm:
    fontFamily: "Inter, ui-sans-serif, system-ui, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: 0em
  label-md:
    fontFamily: "Inter, ui-sans-serif, system-ui, sans-serif"
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0em
  label-sm:
    fontFamily: "Inter, ui-sans-serif, system-ui, sans-serif"
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0.04em
  code:
    fontFamily: "JetBrains Mono, ui-monospace, SFMono-Regular, Menlo, monospace"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: 0em
rounded:
  none: 0px
  sm: 4px
  md: 8px
  lg: 12px
  xl: 16px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
  4xl: 96px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.md}"
    padding: 20px
    height: 44px
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.md}"
    padding: 20px
    height: 44px
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.label-md}"
    rounded: "{rounded.md}"
    padding: 20px
    height: 44px
  button-secondary-hover:
    backgroundColor: "{colors.surface-subtle}"
    textColor: "{colors.on-surface}"
    typography: "{typography.label-md}"
    rounded: "{rounded.md}"
    padding: 20px
    height: 44px
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 24px
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 14px
    height: 44px
  input-error:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.error}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 14px
    height: 44px
  tag:
    backgroundColor: "{colors.primary-subtle}"
    textColor: "{colors.primary}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
    padding: 12px
    height: 28px
  code-block:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.on-surface-dark}"
    typography: "{typography.code}"
    rounded: "{rounded.lg}"
    padding: 20px
---

## Overview

This is the design system for a personal **developer portfolio** — a place to show projects, skills, and experience and to link out to GitHub, case studies, and contact channels.

The personality is **minimal, modern, calm, and confident**. The work is the hero; the interface gets out of the way. Generous whitespace, a tight neutral palette, a single decisive blue accent, and restrained motion communicate craft and seriousness without decoration for its own sake.

The site is **light-first with a complete dark theme**. Light mode is the default — bright, clean, and friendly to read. Dark mode is the supported secondary, ideal for code-heavy content and visual project shots; both must be first-class, never an afterthought.

Intended emotional response: *"This person is precise, thoughtful, and good at their craft."* Visitors should feel oriented immediately and never distracted from the content.

## Colors

The palette is intentionally narrow: a near-neutral foundation plus one accent. This keeps the design quiet and lets project imagery provide the color.

**Accent (blue)**

- `primary` `#2563EB` — the single brand accent. Used for links, primary buttons, active states, and focus rings. Apply it sparingly so it always reads as "this matters."
- `primary-hover` `#1D4ED8` — darker step for hover/pressed states of primary actions in light mode.
- `primary-subtle` `#EFF6FF` — a faint blue wash for tag/chip backgrounds and highlighted callouts.
- `primary-bright` `#60A5FA` — a lighter blue used as the accent on dark surfaces, where `#2563EB` lacks contrast.
- `on-primary` `#FFFFFF` — text/icons placed on the accent.

**Light neutrals**

- `surface` `#FFFFFF` — page background and cards.
- `surface-subtle` `#FAFAFA` — alternating sections, hovered rows, and inset panels.
- `on-surface` `#0A0A0A` — primary text and headings (near-black, not pure black, to soften glare).
- `on-surface-muted` `#71717A` — secondary text, captions, metadata, and placeholder copy.
- `border` `#E4E4E7` — hairline dividers and card outlines. Borders do the structural work instead of heavy shadows.

**Dark neutrals**

- `surface-dark` `#0A0A0A` — dark-mode page background; also the background for code blocks in light mode.
- `surface-dark-subtle` `#18181B` — dark-mode cards and raised panels.
- `on-surface-dark` `#FAFAFA` — primary text on dark.
- `on-surface-dark-muted` `#A1A1AA` — secondary text on dark.
- `border-dark` `#27272A` — dividers and outlines on dark.

**Status**

- `error` `#DC2626` — form validation errors and destructive actions only.
- `success` `#16A34A` — confirmations (e.g. "message sent").

Contrast: `on-surface` on `surface` and `on-surface-dark` on `surface-dark` both exceed WCAG AAA for body text. Always pair the bright accent (`primary-bright`) with dark surfaces and the standard accent (`primary`) with light surfaces.

## Typography

One typeface carries the entire interface: **Inter**, a modern grotesque chosen for its neutrality and excellent screen legibility. A monospace face (**JetBrains Mono**) is reserved strictly for code — inline snippets and code blocks — to reinforce the developer context without turning the UI into a terminal.

**Scale & usage**

- `headline-display` 60px / 700 — the hero name or landing statement, one per page. Tight tracking (`-0.03em`) for a crafted look.
- `headline-lg` 40px / 700 — major section titles ("Projects", "About").
- `headline-md` 28px / 600 — project titles and subsection headers.
- `headline-sm` 20px / 600 — card titles and inline group labels.
- `body-lg` 18px / 400 — intro paragraphs and lead copy; line-height 1.7 for comfortable reading.
- `body-md` 16px / 400 — default body text.
- `body-sm` 14px / 400 — captions, footnotes, and dense metadata.
- `label-md` 14px / 500 — buttons and navigation links.
- `label-sm` 12px / 500 — overline labels and tags; slight positive tracking (`0.04em`) and typically uppercase.
- `code` 14px mono — inline code and code blocks only.

Weights are limited to **400 / 500 / 600 / 700**. Headings use negative letter-spacing for tightness; body copy stays at `0em`. Avoid italics except for genuine emphasis or citations.

## Layout

The layout is built on **whitespace and a single readable column**, not on dense grids.

- **Content width:** cap the main reading column at ~720px for prose and ~1120px for project grids. Center within the viewport.
- **Page gutters:** 24px on mobile, 48px+ on desktop.
- **Grid:** project listings use a responsive 1 → 2 → 3 column grid with a 24px (`lg`) gutter. Everything else is a single column.
- **Spacing rhythm:** all spacing comes from the 4px-based scale. Use `md` (16px) inside components, `xl`–`2xl` (32–48px) between related blocks, and `3xl`–`4xl` (64–96px) between major page sections. Generous vertical spacing is the signature of this system — when unsure, add more.
- **Density:** low. Let elements breathe; avoid cramming.
- **Mobile:** single column, full-width cards, comfortable 16px body text, and tap targets ≥ 44px.

## Elevation & Depth

This system is **flat and border-driven**. Hierarchy comes from spacing, type weight, and hairline borders — not from drop shadows.

- Cards and panels are defined by a 1px `border` (light) / `border-dark` (dark), not a shadow.
- Use at most one subtle shadow, and only for genuinely floating UI (dropdowns, popovers, sticky nav on scroll): a soft, low-opacity shadow such as `0 1px 2px rgba(0,0,0,0.05)` light / a faint border in dark mode.
- No glassmorphism, no gradients on surfaces, no neumorphism.
- Layering on dark mode is expressed by stepping the surface tone: `surface-dark` → `surface-dark-subtle` for raised elements.
- Focus states use a 2px `primary` / `primary-bright` ring for accessibility, never a glow.

## Shapes

Corners are **softly rounded but never bubbly** — modern and quiet.

- Buttons, inputs, and tags-as-controls: `md` (8px).
- Cards, code blocks, and images: `lg` (12px); large feature panels may use `xl` (16px).
- Pills, avatars, and tags: `full` for a clean chip/circle.
- Dividers and section edges: square (`none`).
- Images and project thumbnails: `lg` corners with a 1px border to keep them crisp against the background.
- Icons: line-style (stroked), ~1.5–2px weight, to match the light, modern feel.

## Components

Components are minimal and state-aware. Mirror the YAML `components` tokens.

- **button-primary** — solid `primary` background, `on-primary` text, 8px radius, 44px tall. The single high-emphasis action per view (e.g. "View project", "Get in touch"). Hover → `button-primary-hover`.
- **button-secondary** — `surface` background with a 1px `border`, `on-surface` text. For secondary actions ("Source", "Resume"). Hover → `button-secondary-hover` (fills with `surface-subtle`).
- **card** — `surface` background, 1px `border`, 12px radius, 24px padding. The project tile and content container. On hover, raise emphasis by shifting the border toward `primary` rather than adding shadow.
- **input** / **input-error** — `surface` background, 8px radius, 44px tall. Default border is `border`; focus border is `primary` with a 2px ring; `input-error` switches text/border to `error` and shows a `body-sm` message below.
- **tag** — `primary-subtle` background, `primary` text, full radius, `label-sm` type. Used for tech-stack chips on project cards. In dark mode, use a transparent fill with a `border-dark` outline and `primary-bright` text.
- **code-block** — always dark (`surface-dark` background, `on-surface-dark` text) in both themes, `code` typography, 12px radius. Keeps code legible and visually distinct from prose.
- **link** — `primary` text, no underline at rest, underline on hover; inherits weight from context. The accent's most frequent appearance.
- **nav** — minimal top bar: wordmark/name left, a few `label-md` links right, plus a light/dark toggle. Transparent over the hero, gaining a hairline bottom `border` on scroll.

## Do's and Don'ts

- **Do** keep one accent color. Blue carries all interactivity; introducing a second hue breaks the system.
- **Do** lead with whitespace — when a layout feels off, add space before adding elements.
- **Do** use borders, not shadows, to separate surfaces.
- **Do** treat dark mode as a real deliverable: test every component and use `primary-bright` for the accent on dark.
- **Do** reserve the monospace font for actual code only.
- **Do** keep one primary button per view; everything else is secondary or a link.
- **Don't** use pure black (`#000000`) or pure shadows-heavy cards; stick to `#0A0A0A` and hairline borders.
- **Don't** add gradients, glows, glassmorphism, or decorative illustration that competes with project content.
- **Don't** mix more than four font weights or introduce a second typeface for UI.
- **Don't** let the accent appear on large fill areas; it should always feel deliberate and scarce.
- **Don't** crowd the type scale — pick the nearest token rather than inventing in-between sizes.
