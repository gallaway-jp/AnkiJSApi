# Sphinx Documentation Build Instructions

This directory contains Sphinx documentation for generating HTML API reference.

## Prerequisites

Install Sphinx and the Read the Docs theme:

```bash
pip install sphinx sphinx-rtd-theme
```

These are already included in `requirements-dev.txt`.

## Building Documentation

### Build HTML Documentation

```bash
cd docs
sphinx-build -b html . _build/html
```

Or use the Makefile (Linux/macOS):

```bash
cd docs
make html
```

Or use make.bat (Windows):

```cmd
cd docs
make.bat html
```

### View Documentation

After building, open `docs/_build/html/index.html` in your browser.

### Clean Build Artifacts

```bash
cd docs
rm -rf _build/  # Linux/macOS
# or
rmdir /s _build  # Windows
```

## Auto-build with Live Reload

For development, use sphinx-autobuild:

```bash
pip install sphinx-autobuild
cd docs
sphinx-autobuild . _build/html
```

Then visit http://localhost:8000 - documentation will auto-rebuild on changes.

## Documentation Structure

```
docs/
├── conf.py              # Sphinx configuration
├── index.rst            # Main documentation index
├── api/
│   └── index.rst        # API reference index
├── _build/              # Generated HTML (gitignored)
├── _static/             # Static assets (CSS, images)
└── _templates/          # Custom templates
```

## Publishing Documentation

### GitHub Pages

1. Build documentation:
   ```bash
   sphinx-build -b html docs docs/_build/html
   ```

2. Copy to docs/ for GitHub Pages:
   ```bash
   cp -r docs/_build/html/* docs/
   ```

3. Enable GitHub Pages in repository settings pointing to `docs/` folder.

### Read the Docs

1. Create account at https://readthedocs.org/
2. Import GitHub repository
3. Build will automatically trigger on commits
4. Documentation will be available at `https://ankidroid-js-api-desktop.readthedocs.io/`

## Customization

Edit `docs/conf.py` to customize:
- Project information
- Theme and styling
- Extensions enabled
- Autodoc options

## Troubleshooting

### Module not found errors

If you see "module not found" errors, ensure:
1. Source path is correct in conf.py: `sys.path.insert(0, os.path.abspath('../src'))`
2. Mock imports are configured for Anki modules: `autodoc_mock_imports = ['aqt', 'anki', 'PyQt6']`

### No documentation generated

Ensure:
1. All modules have docstrings
2. Functions have proper docstrings
3. autodoc extension is enabled in conf.py

### Theme not loading

Ensure sphinx-rtd-theme is installed:
```bash
pip install sphinx-rtd-theme
```
