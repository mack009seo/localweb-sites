---
description: Generates a batch of landing pages, updates the directory index, and deploys to GitHub Pages.
---

To generate and deploy a new batch of landing pages, run:

// turbo
1. python3 src/automate.py --limit [NUMBER_OF_SITES]

### Options:
- `--limit`: Number of sites to generate (default: 5)
- `--csv`: Path to the source CSV data
- `--skip-deploy`: Use this flag to generate and index without pushing to GitHub

### Post-generation tasks:
- Verify the main index at `sites/index.html`
- Check the live directory at `https://[USERNAME].github.io/localweb-sites/`
