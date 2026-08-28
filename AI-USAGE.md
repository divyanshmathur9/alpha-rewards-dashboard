# AI usage

OpenAI Codex was used as a development assistant for scaffolding, selected API/UI implementation, debugging, documentation, and test guidance. The implementation was reviewed and adjusted in this repository.

Examples where suggested output was corrected during review:

1. The first seed attempt failed because the supplied data contains duplicate transaction IDs. Instead of dropping records, the seed script now preserves all 10,000 rows with a suffix on repeated IDs.
2. The initial frontend stylesheet used bare selectors in a CSS module and the page shell was missing its wrapper class. Browser inspection exposed the issue; the CSS selectors and page shell were corrected.
3. The initial Next.js font setup depended on downloading a remote font at build time. That approach was removed in favor of local system fallbacks so production builds do not depend on an external font request.

The final implementation is intentionally small and uses direct, explainable patterns suitable for a take-home project. The author reviewed the behavior locally and selected the final scope, trade-offs, and deployment configuration.
