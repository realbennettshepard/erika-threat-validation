# Threat Classification Validation

A static, browser-only tool to measure how accurately an LLM classifies explicit threats toward Erika Kirk, and how much independent human coders agree.

- **index.html** - landing page
- **code.html** - blind coding of an 80-post balanced sample; exports a per-coder results JSON
- **compare.html** - load multiple coders' result files for inter-coder agreement, a human consensus, and model-vs-consensus accuracy

All computation runs client-side; no data is uploaded. Deployable as-is to GitHub Pages.
