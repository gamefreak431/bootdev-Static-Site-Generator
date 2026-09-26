# bootdev-Static-Site-Generator
A guided project from Boot.dev's Python back-end curriculum, turning Markdown into a website.

This project was built as part of the [Build a Static Site Generator in Python](https://www.boot.dev/courses/build-static-site-generator-python) guided project on [Boot.dev](https://www.boot.dev). It walks through writing a static site generator from scratch in Python, in the spirit of tools like Hugo or Jekyll. Every page is built from Markdown files, with no third-party libraries: a hand-written parser turns each file into a tree of HTML nodes, renders it into an HTML template, and writes out a complete site ready to host on GitHub Pages.

**Live site:** [gamefreak431.github.io/bootdev-Static-Site-Generator](https://gamefreak431.github.io/bootdev-Static-Site-Generator/)

## Local Setup

### Prerequisites

- Python 3.12+
- No third-party dependencies. The generator uses only the standard library.
- A **Linux environment** is required to run the shell scripts. On Windows, use [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) (Windows Subsystem for Linux). macOS should work without modification.

### 1. Clone the repository

```bash
git clone https://github.com/gamefreak431/bootdev-Static-Site-Generator.git
cd bootdev-Static-Site-Generator
```

### 2. Build and preview the site locally

```bash
./main.sh
```

This generates the site into `docs/` and serves it at [http://localhost:8888](http://localhost:8888). Stop the server with `Ctrl+C`.

### 3. Build for production

```bash
./build.sh
```

This generates the site into `docs/` with every root-relative link prefixed by the repository name (`/bootdev-Static-Site-Generator/`). GitHub Pages needs that prefix because it serves a project site from `https://<username>.github.io/<repo-name>/` rather than from the domain root. Commit and push the regenerated `docs/` folder to publish it.

> **Note:** A production build won't display correctly under `./main.sh`'s local server, because the local server has no `/bootdev-Static-Site-Generator/` directory. Use `./main.sh` for previewing and `./build.sh` right before you commit.

### Running the tests

```bash
./test.sh
```

## Making Your Own Site

### Project layout

| Path | What it's for |
|---|---|
| `content/` | Your pages, written in Markdown. **Edit and add files here.** |
| `static/` | CSS, images and any other files copied into the site as-is. |
| `template.html` | The HTML shell wrapped around every page. |
| `build.sh` | The production build. Holds your repository name. |
| `docs/` | Generated output. Deleted and rebuilt on every run, so don't edit it by hand. |
| `src/` | The generator itself. |

### Adding pages

Every `.md` file under `content/` becomes an `.html` file at the same place in `docs/`:

| Source | Output | URL |
|---|---|---|
| `content/index.md` | `docs/index.html` | `/` |
| `content/contact/index.md` | `docs/contact/index.html` | `/contact` |
| `content/blog/tom/index.md` | `docs/blog/tom/index.html` | `/blog/tom` |

Naming each page `index.md` inside its own folder gives you clean URLs without `.html` on the end.

Each page **must have a top-level `#` heading**. The first one becomes the page's `<title>`, and the build stops with an error if a page doesn't have one.

### Supported Markdown

- Headings (`#` through `######`)
- Paragraphs
- `**bold**`, `_italic_` and `` `inline code` ``
- Code blocks fenced with ```` ``` ````
- Block quotes (`>`)
- Unordered (`-`) and ordered (`1.`) lists
- Links `[text](url)` and images `![alt](url)`

Nested lists, tables and other extended Markdown syntax aren't supported.

### Links and images

Start internal links and image paths with `/`, as in `[Contact](/contact)` or `![Tom](/images/tom.png)`. The production build adds the repository prefix to any `href="/` or `src="/` it finds, so root-relative links work both locally and on GitHub Pages. External links like `https://…` are left alone.

Images and other assets go in `static/`, and `static/images/tom.png` is served at `/images/tom.png`.

### Styling and layout

- Edit `static/index.css` to change the look of every page.
- Edit `template.html` to change the page structure. It must keep the `{{ Title }}` and `{{ Content }}` placeholders, which are replaced with the page title and the rendered Markdown.

### Deploying your fork to GitHub Pages

1. In `build.sh`, replace `/bootdev-Static-Site-Generator/` with `/<your-repo-name>/`, keeping the leading and trailing slashes.
2. Run `./build.sh`, then commit and push `docs/`.
3. On GitHub, go to **Settings → Pages**, set the source to **Deploy from a branch**, and pick the `main` branch and `/docs` folder.

Your site will be live at `https://<username>.github.io/<your-repo-name>/` a minute or two later.

## Certificate

[![Boot.dev Build a Static Site Generator in Python certificate](https://qvault-webapp-dynamic-assets.storage.googleapis.com/certificates/2c5872c1-9836-4128-a290-2d8245eaa6bb.jpeg?v=1790399215)](https://www.boot.dev/certificates/2c5872c1-9836-4128-a290-2d8245eaa6bb)
