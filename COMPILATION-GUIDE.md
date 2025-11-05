# CRR Documentation Compilation Guide

This guide provides multiple methods to compile `crr-comprehensive-documentation.tex` into a PDF.

## Quick Start (Recommended)

If you have LaTeX installed, simply run:

```bash
./compile-documentation.sh
```

This script handles all compilation passes automatically and cleans up auxiliary files.

---

## Method 1: Local Compilation (Full Control)

### Prerequisites

Install a LaTeX distribution:

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install texlive-full
```

**macOS:**
```bash
brew install --cask mactex
# Or download from: https://www.tug.org/mactex/
```

**Windows:**
- Download MiKTeX: https://miktex.org/download
- Or TeX Live: https://www.tug.org/texlive/

### Required Packages

The document uses standard packages included in full LaTeX distributions:
- amsmath, amssymb, amsthm (mathematics)
- graphicx (images)
- tikz (diagrams)
- hyperref, cleveref (cross-references)
- booktabs, caption, subcaption (tables/figures)
- listings, xcolor (code highlighting)
- geometry, float (layout)

### Compilation Commands

#### Option A: Automated Script
```bash
cd /home/user/CRR
./compile-documentation.sh
```

#### Option B: Manual Compilation
```bash
cd /home/user/CRR

# First pass - generate structure
pdflatex crr-comprehensive-documentation.tex

# Second pass - resolve references
pdflatex crr-comprehensive-documentation.tex

# Third pass (optional) - final cleanup
pdflatex crr-comprehensive-documentation.tex
```

#### Option C: Using latexmk (recommended for advanced users)
```bash
latexmk -pdf crr-comprehensive-documentation.tex
```

### Viewing the PDF

**Linux:**
```bash
xdg-open crr-comprehensive-documentation.pdf
```

**macOS:**
```bash
open crr-comprehensive-documentation.pdf
```

**Windows:**
```bash
start crr-comprehensive-documentation.pdf
```

---

## Method 2: Online Compilation (No Installation)

### Overleaf (Recommended for Online)

1. Go to https://www.overleaf.com/
2. Create a free account (or login)
3. Click "New Project" → "Upload Project"
4. Create a ZIP file with all files:
   ```bash
   cd /home/user/CRR
   zip crr-documentation.zip \
       crr-comprehensive-documentation.tex \
       *.png \
       DOCUMENTATION-README.md
   ```
5. Upload the ZIP file
6. Overleaf will compile automatically
7. Download PDF from the interface

**Overleaf Benefits:**
- No installation required
- Real-time preview
- Collaboration features
- Automatic compilation on save
- Mobile-friendly interface

### Alternative Online Compilers

**Papeeria:** https://papeeria.com/
- Similar to Overleaf
- Free tier available

**CoCalc:** https://cocalc.com/
- Collaborative LaTeX editing
- Jupyter notebooks integration

**LaTeX Base:** https://latexbase.com/
- Simple, no-registration option
- Good for quick compilations

---

## Method 3: Docker (Consistent Environment)

### Using Official TeX Live Docker Image

Create a `Dockerfile`:

```dockerfile
FROM texlive/texlive:latest

WORKDIR /document

COPY . .

RUN pdflatex crr-comprehensive-documentation.tex && \
    pdflatex crr-comprehensive-documentation.tex

CMD ["cp", "crr-comprehensive-documentation.pdf", "/output/"]
```

Build and run:

```bash
cd /home/user/CRR
docker build -t crr-doc-compiler .
docker run -v $(pwd):/output crr-doc-compiler
```

### Using Pre-built LaTeX Container

```bash
docker run --rm -v $(pwd):/workdir \
    -w /workdir \
    danteev/texlive:latest \
    pdflatex -interaction=nonstopmode crr-comprehensive-documentation.tex
```

---

## Method 4: GitHub Actions (Automated)

Create `.github/workflows/compile-latex.yml`:

```yaml
name: Compile LaTeX Document

on:
  push:
    paths:
      - '**.tex'
      - '**.png'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Compile LaTeX document
        uses: xu-cheng/latex-action@v2
        with:
          root_file: crr-comprehensive-documentation.tex

      - name: Upload PDF artifact
        uses: actions/upload-artifact@v3
        with:
          name: crr-documentation-pdf
          path: crr-comprehensive-documentation.pdf
```

Push to GitHub and the PDF will compile automatically on every push.

---

## Method 5: Tectonic (Modern LaTeX Engine)

### Install Tectonic

**Linux/macOS:**
```bash
curl --proto '=https' --tlsv1.2 -fsSL https://drop-sh.fullyjustified.net | sh
```

**Or with Cargo:**
```bash
cargo install tectonic
```

### Compile

```bash
tectonic crr-comprehensive-documentation.tex
```

**Benefits:**
- Single-pass compilation
- Automatic package downloading
- Fast and modern
- Self-contained

---

## Troubleshooting

### Missing Packages Error

If you see "LaTeX Error: File `package.sty' not found":

**Solution 1: Install full distribution**
```bash
# Linux
sudo apt-get install texlive-full

# macOS
brew install --cask mactex-no-gui
```

**Solution 2: Install specific package**
```bash
# Find package
tlmgr search --global --file package.sty

# Install it
sudo tlmgr install package-name
```

### Graphics Not Found

If images aren't showing:

1. Ensure all PNG files are in the same directory
2. Check file names match exactly (case-sensitive)
3. Run `ls *.png` to verify files exist

```bash
# Required PNG files:
- crr-cycle-diagram.png
- coherence-accumulation-graph.png
- regeneration-visualization.png
- fep-crr-connection.png
- scale-invariance-diagram.png
- memory-signatures-diagram.png
```

### Compilation Hangs

If compilation appears frozen:

1. Press `X` or `Ctrl+C` to cancel
2. Run with `--halt-on-error`:
   ```bash
   pdflatex --halt-on-error crr-comprehensive-documentation.tex
   ```
3. Check the `.log` file for errors:
   ```bash
   tail -50 crr-comprehensive-documentation.log
   ```

### Out of Memory

For large documents:

```bash
# Increase TeX memory
export main_memory=12000000
export extra_mem_bot=12000000
pdflatex crr-comprehensive-documentation.tex
```

Or edit `texmf.cnf` to increase memory permanently.

---

## Expected Output

### PDF Statistics
- **Pages:** ~50-60
- **File Size:** 2-4 MB (depends on image compression)
- **Compilation Time:** 10-30 seconds (depending on system)

### PDF Contents
1. Title page with author and date
2. Abstract (1 page)
3. Table of Contents (2-3 pages)
4. Main sections (40-50 pages):
   - Introduction
   - Mathematical Framework
   - FEP Connection
   - Simulation Documentation
   - LLM Methodology
   - Coarse-Graining
   - Discussion
5. Bibliography
6. Appendices (proofs and derivations)

---

## Optimization Tips

### Faster Compilation

```bash
# Use draft mode (faster, no images)
pdflatex -draftmode crr-comprehensive-documentation.tex

# Parallel compilation with arara
arara -v crr-comprehensive-documentation.tex
```

### Smaller PDF Size

```bash
# Compile with compression
pdflatex -synctex=1 -interaction=nonstopmode \
    -output-format=pdf \
    crr-comprehensive-documentation.tex

# Then compress
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 \
   -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH \
   -sOutputFile=crr-comprehensive-documentation-compressed.pdf \
   crr-comprehensive-documentation.pdf
```

### High-Quality PDF

```bash
pdflatex -output-format=pdf \
    -synctex=1 \
    -interaction=nonstopmode \
    crr-comprehensive-documentation.tex
```

---

## Regenerating Diagrams

If you modify diagram code:

```bash
# Regenerate all PNG diagrams
python3 generate_crr_diagrams.py

# Then recompile LaTeX
./compile-documentation.sh
```

---

## Getting Help

### LaTeX Resources

- **TeX StackExchange:** https://tex.stackexchange.com/
- **Overleaf Documentation:** https://www.overleaf.com/learn
- **LaTeX Wikibook:** https://en.wikibooks.org/wiki/LaTeX

### Package Documentation

```bash
# View package documentation
texdoc amsmath
texdoc tikz
texdoc hyperref
```

### CRR-Specific Issues

For questions about the CRR framework itself, visit:
- **Website:** https://alexsabine.github.io/CRR/
- **Repository:** https://github.com/alexsabine/CRR

---

## Alternative Formats

### Convert to Other Formats

**HTML (via tex4ht):**
```bash
htlatex crr-comprehensive-documentation.tex
```

**Word (via pandoc):**
```bash
pandoc crr-comprehensive-documentation.tex -o crr-comprehensive-documentation.docx
```

**Markdown:**
```bash
pandoc crr-comprehensive-documentation.pdf -o crr-comprehensive-documentation.md
```

---

## Summary of Methods

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **Local** | Full control, offline | Requires installation | Regular use, customization |
| **Overleaf** | No installation, collaborative | Requires internet | Quick sharing, collaboration |
| **Docker** | Consistent environment | Requires Docker | CI/CD, reproducibility |
| **GitHub Actions** | Automatic, version-controlled | Requires GitHub setup | Open-source projects |
| **Tectonic** | Modern, fast, self-contained | Less established | Modern workflows |

---

## Quick Reference Card

```bash
# Quick compilation
./compile-documentation.sh

# Manual compilation
pdflatex crr-comprehensive-documentation.tex (run 2-3 times)

# View PDF
xdg-open crr-comprehensive-documentation.pdf  # Linux
open crr-comprehensive-documentation.pdf      # macOS
start crr-comprehensive-documentation.pdf     # Windows

# Clean auxiliary files
rm *.aux *.log *.out *.toc

# Regenerate diagrams
python3 generate_crr_diagrams.py

# Check for errors
tail -50 crr-comprehensive-documentation.log
```

---

**Last Updated:** November 5, 2025
**Document Version:** 1.0
**Tested Platforms:** Ubuntu 22.04, macOS 14, Windows 11
