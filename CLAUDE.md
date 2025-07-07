# Awesome Reviewers Repository Guidelines

## Repository Structure & Technology Stack

### Technology Stack
- **GitHub Pages** repository
- **Jekyll** static site generator
- **GitHub Actions** for CI/CD
- Raw HTML with Jekyll templating

### Key Pages & Layouts
1. **Root Page** (`/`)
   - Managed in `_layouts/default.html`
   - Main landing page with reviewer grid

2. **Reviewer Detail Page** (`/reviewers/{slug}/`)
   - Managed in `_layouts/reviewer.html` 
   - Individual reviewer drawer/detail view

### Directory Structure
- **Assets**: `assets/`
  - CSS files: `assets/css/`
  - Images: `assets/images/`

- **Content**: `_reviewers/`
  - Individual reviewer prompt files
  - Contains all the reviewer data and prompts

### Development Notes
- This is a Jekyll-based GitHub Pages site
- Changes to layouts, CSS, or reviewer content require Jekyll rebuild
- GitHub Actions handles the build and deployment process
- All styling should be done in the CSS files under `assets/css/`
- Reviewer content is stored as individual files in `_reviewers/` directory