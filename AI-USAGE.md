# AI usage

This project was developed with assistance from OpenAI Codex. AI support was used for project scaffolding, API and UI implementation, debugging, and review. All generated code was inspected and tested in this repository.

Examples of edits made during review:

1. The first seed attempt failed because the supplied data contains duplicate transaction IDs. Instead of dropping records, the seed script now preserves all 10,000 rows with a suffix on repeated IDs.
2. The initial frontend stylesheet used bare selectors in a CSS module and the page shell was missing its wrapper class. Browser inspection exposed the issue; the CSS selectors and page shell were corrected.

The final implementation is intentionally small and uses direct, explainable patterns suitable for a take-home project.

