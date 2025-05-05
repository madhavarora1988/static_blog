# Minimal Static Blog Generator

A super simple static blog generator that converts Markdown files to HTML. No complex frameworks, no databases, just pure simplicity!

## Features

- Markdown support with code highlighting
- Dark mode support
- Responsive design
- No JavaScript required
- Simple directory-based post organization
- Automatic index page generation
- Image support

## Setup

1. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a new post:
   - Create a new directory under `posts/` with a unique name (e.g., `posts/my-new-post/`)
   - Add a `post.md` file in that directory
   - Add any images referenced in your post to the same directory

3. Build the blog:
   ```bash
   python render.py
   ```

4. Move the output to the `docs/` folder for GitHub Pages:
   ```bash
   python move_to_docs.py
   ```

5. Commit all files, including the `docs/` folder, to your git repository.

## Deploying to GitHub Pages

1. Push your repository to GitHub.
2. Go to your repository's **Settings** > **Pages**.
3. Under **Source**, select the `main` branch and `/docs` folder.
4. Save. Your site will be available at `https://yourusername.github.io/reponame/`.

- **Note:** Always commit the `docs/` folder and its contents. Do not add it to `.gitignore`.
- For local testing, you can use a simple web server:
  ```bash
  python -m http.server
  ```
  Then visit `http://localhost:8000/docs/` in your browser.

## Post Format

Each post should be in Markdown format and start with a level 1 heading (#) that will be used as the post title:

```markdown
# My Post Title

Post content goes here...
```

## Directory Structure

```
.
├── docs/             # Output directory for GitHub Pages
│   ├── index.html
│   ├── blog/
│   └── posts/
├── posts/            # Source posts (recommended to keep in git)
├── render.py         # Script to generate the blog
├── move_to_docs.py   # Script to move output to docs/
├── template.html     # HTML template for all pages
├── greetings.md      # Content for the index page
├── requirements.txt
└── README.md
```

## License

MIT 