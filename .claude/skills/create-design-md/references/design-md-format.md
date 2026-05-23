# DESIGN.md Format Reference

Source: https://github.com/google-labs-code/design.md and `docs/spec.md` from that repository.

Use this reference as the contract for generated files.

## Required Shape

A `DESIGN.md` file has two layers:

- YAML front matter at the top, fenced by lines containing exactly `---`.
- Markdown body using `##` headings for human-readable design rationale.

Tokens are normative. Prose explains why and how to apply them.

## YAML Token Schema

Use this shape unless the user explicitly needs a narrower file:

```yaml
---
version: alpha
name: <string>
description: <string>
colors:
  <token-name>: "#RRGGBB"
typography:
  <token-name>:
    fontFamily: <string>
    fontSize: <dimension>
    fontWeight: <number>
    lineHeight: <dimension-or-number>
    letterSpacing: <dimension>
    fontFeature: <string>
    fontVariation: <string>
rounded:
  <scale-level>: <dimension>
spacing:
  <scale-level>: <dimension-or-number>
components:
  <component-name>:
    backgroundColor: "{colors.<token-name>}"
    textColor: "{colors.<token-name>}"
    typography: "{typography.<token-name>}"
    rounded: "{rounded.<scale-level>}"
    padding: <dimension>
    size: <dimension>
    height: <dimension>
    width: <dimension>
---
```

Allowed color values are sRGB hex values beginning with `#`. Quote hex colors in YAML.

Allowed dimensions use `px`, `em`, or `rem`, such as `48px`, `1rem`, or `-0.02em`.

Token references use `{path.to.token}` syntax. References should resolve to primitive values, except `components` may reference composite typography tokens such as `{typography.label-md}`.

Recommended token names:

- Colors: `primary`, `secondary`, `tertiary`, `neutral`, `surface`, `on-surface`, `error`.
- Typography: `headline-display`, `headline-lg`, `headline-md`, `body-lg`, `body-md`, `body-sm`, `label-lg`, `label-md`, `label-sm`.
- Rounded: `none`, `sm`, `md`, `lg`, `xl`, `full`.

## Markdown Section Order

Use `##` headings in this order:

1. `Overview`
2. `Colors`
3. `Typography`
4. `Layout`
5. `Elevation & Depth`
6. `Shapes`
7. `Components`
8. `Do's and Don'ts`

Accepted aliases from the spec:

- `Brand & Style` for `Overview`
- `Layout & Spacing` for `Layout`
- `Elevation` for `Elevation & Depth`

Prefer canonical names when creating new files. Preserve valid aliases only when repairing existing files and the user prefers minimal edits.

## Section Expectations

`Overview`: Describe the brand personality, audience, product context, visual tone, and intended emotional response.

`Colors`: Explain semantic roles for each palette or color token. Include hex values in prose for important colors.

`Typography`: Explain font families, type scale, weights, casing, letter spacing, and where each text style is used.

`Layout`: Explain grid, density, spacing rhythm, page width, gutters, mobile behavior, and content grouping.

`Elevation & Depth`: Explain shadows, tonal layers, borders, blur, glass, or flat hierarchy rules.

`Shapes`: Explain corner radii, sharpness, pills, containers, controls, and icon or image shape treatment.

`Components`: Explain key component styling and states. Mirror important component decisions in YAML `components`.

`Do's and Don'ts`: Provide practical implementation guardrails as direct bullets.

## Consumer Behavior

Unknown section headings may be preserved, but do not add unknown sections in new files unless the source material requires them.

Unknown color and typography token names are valid if their values are valid.

Unknown component properties should be avoided in new files because consumers may warn.

Duplicate `##` headings are invalid.

## Validation

Prefer:

```bash
npx @google/design.md lint DESIGN.md
```

Fallback:

```bash
python3 scripts/validate_design_md.py DESIGN.md
```

The fallback validator checks the structural contract; the official linter remains authoritative.

