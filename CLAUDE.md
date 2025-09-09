# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Technology Stack

This is a Jekyll-based personal blog/website (sorokin.engineer) using:
- Jekyll static site generator
- Ruby 2.5+ (managed via rbenv)
- Liquid templating
- Kramdown for Markdown processing
- SCSS for styling
- Analytics: Google Analytics and Yandex Metrika

## Development Commands

### Local Development
```bash
# Install dependencies
bundle install

# Serve locally (default port 4000)
jekyll serve
```

### Docker Development
For containerized development without local Ruby installation:
```bash
# Build and run container
./debug.sh

# Or manually:
docker build . -t sorokin.engineer
docker run --rm -it --name sorokin.engineer -p 4000:4000 --mount type=bind,source="$(pwd)"/,target=/workspaces/sorokin.engineer sorokin.engineer
```

### VS Code DevContainer
The project includes `.devcontainer/` configuration for VS Code remote containers with automatic Jekyll setup.

## Architecture

### Site Structure
- `_layouts/`: HTML templates (default, post, page, reviews, etc.)
- `_includes/`: Reusable HTML components (analytics, search, navigation, etc.)  
- `_data/`: YAML data files (menu, localization, reviews, languages)
- `_posts/`: Blog posts in Markdown
- `_sass/`: Sass stylesheets
- `pages/`: Static pages
- `posts/`: Additional post organization
- `images/`: Static assets and media

### Key Features
- Multi-language support with language selector
- Tag cloud and search functionality
- Reviews system with structured data in `_data/reviews.yaml`
- Comment system integration (Disqus, Staticman)
- Responsive design with custom SCSS

### Configuration
- Main config: `_config.yml` 
- Analytics IDs and social links configured in `_config.yml`
- Jekyll plugins: sitemap, feed, redirect-from
- Permalink structure: `/:categories/:title.html`

### Data Files
- `_data/menu.yaml`: Site navigation structure
- `_data/localization.yaml`: Translation strings
- `_data/languages.yaml`: Supported languages
- `_data/reviews.yaml`: Structured review data
- `_data/comments/`: User comments (Staticman)

## Content Management

Posts are written in Markdown with YAML front matter and support:
- Categories and tags
- Language variants
- Redirects via jekyll-redirect-from
- Custom layouts for different content types

The site builds automatically on GitHub Pages or can be deployed via the generated `_site/` directory.