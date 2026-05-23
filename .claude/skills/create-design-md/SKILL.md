---
name: create-design-md
description: Create or refine strict DESIGN.md files that follow the google-labs-code/design.md format. Use when the user wants to build a DESIGN.md through guided preference questions, generate a DESIGN.md from source material such as a website, app, brand guide, screenshots, CSS, Figma exports, or existing design tokens, or validate and repair an existing DESIGN.md against the canonical YAML front matter plus ordered markdown sections.
---

# Create DESIGN.md

## Quick Start

Create a `DESIGN.md` that uses YAML front matter for machine-readable tokens and ordered `##` markdown sections for design rationale.

Read `references/design-md-format.md` before writing or repairing a file. Use `scripts/validate_design_md.py` after drafting.

Prefer the official validator when available:

```bash
npx @google/design.md lint DESIGN.md
```

If `npx` is unavailable or network access is restricted, run:

```bash
python3 skills/create-design-md/scripts/validate_design_md.py DESIGN.md
```

## Workflow

1. Determine the input mode:
   - `guided`: The user wants to define a design system from preferences.
   - `source`: The user provided source material to derive a design system.
   - `repair`: The user provided an existing `DESIGN.md` to validate or fix.
2. Gather only missing information. Do not ask preference questions already answered by source material.
3. Draft complete YAML front matter first, then markdown sections in canonical order.
4. Ensure every component token reference resolves to a defined token.
5. Validate with the official linter or bundled validator.
6. Fix errors before returning the file. Mention warnings only if they affect user intent.

## Guided Mode

Ask concise questions in batches. Stop asking once enough signal exists to make defensible design decisions.

Required preferences:

- Product or brand name.
- Product type and primary user context.
- Desired personality using 3-5 adjectives.
- Primary actions and surfaces the UI must support.
- Accessibility or platform constraints.

Useful optional preferences:

- Existing colors, forbidden colors, or brand associations.
- Typography direction, such as editorial, technical, playful, luxury, utility, or high-density.
- Layout density, grid behavior, spacing rhythm, and mobile/desktop priority.
- Shape language, elevation model, motion restraint, and component priorities.
- Do's and don'ts the team should follow.

If the user asks for a fast draft, make reasonable choices and state assumptions inside the `Overview` and `Do's and Don'ts` sections, not outside the file.

## Source Mode

Derive tokens and rationale from the provided source. Accept sources such as URLs, screenshots, CSS files, Tailwind configs, token JSON, brand PDFs, app code, product descriptions, or rough notes.

When reading source:

- Extract observed colors as hex values; choose semantic token names intentionally.
- Extract typography from CSS, token files, rendered styles, or visual evidence.
- Infer spacing, radius, component, and elevation patterns from repeated usage.
- Preserve the brand's actual visual intent; do not genericize it into a default SaaS design system.
- If evidence conflicts, prioritize explicit design tokens, then CSS/source code, then brand guidelines, then screenshots, then prose descriptions.
- If evidence is insufficient for a required area, add a coherent default and document the assumption in prose.

## Output Contract

Write one `DESIGN.md` unless the user requests otherwise.

The file must:

- Start with YAML front matter fenced by `---`.
- Include `name`, `colors`, `typography`, `rounded`, `spacing`, and `components` token groups unless the source explicitly requires a narrower file.
- Use quoted sRGB hex colors such as `"#1A1C1E"`.
- Use dimensions with `px`, `em`, or `rem` for font sizes, letter spacing, radii, and most spacing values.
- Use token references like `"{colors.primary}"` only when the referenced token exists.
- Use component keys for variants, such as `button-primary`, `button-primary-hover`, and `input-error`.
- Use only valid component properties unless there is a source-specific reason: `backgroundColor`, `textColor`, `typography`, `rounded`, `padding`, `size`, `height`, `width`.
- Use `##` markdown headings in this order: `Overview`, `Colors`, `Typography`, `Layout`, `Elevation & Depth`, `Shapes`, `Components`, `Do's and Don'ts`.
- Avoid duplicate `##` headings.

Do not add explanatory text before or after the file when the user asks for the file content only.

## Repair Rules

When fixing an existing `DESIGN.md`:

- Preserve user intent, token names, and prose where possible.
- Reorder sections rather than rewriting them wholesale.
- Convert non-hex colors to valid hex if the equivalent is clear.
- Replace broken references with the nearest valid token only when the intended target is obvious.
- Ask before making subjective brand changes that are not required for format validity.
