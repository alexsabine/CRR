#!/bin/bash
#
# Compile CRR Comprehensive Documentation
# This script compiles the LaTeX document with proper passes for references and bibliography
#

set -e  # Exit on error

echo "=========================================="
echo "CRR Documentation Compilation Script"
echo "=========================================="
echo ""

# Check if pdflatex is available
if ! command -v pdflatex &> /dev/null; then
    echo "ERROR: pdflatex not found!"
    echo ""
    echo "Please install LaTeX:"
    echo "  - Ubuntu/Debian: sudo apt-get install texlive-full"
    echo "  - macOS: brew install --cask mactex"
    echo "  - Windows: Download MiKTeX from https://miktex.org/"
    echo ""
    exit 1
fi

echo "✓ pdflatex found"
echo ""

# Main document
DOC="crr-comprehensive-documentation"

# Check if source file exists
if [ ! -f "${DOC}.tex" ]; then
    echo "ERROR: ${DOC}.tex not found!"
    echo "Make sure you're in the correct directory."
    exit 1
fi

echo "Compiling ${DOC}.tex..."
echo ""

# First pass
echo "[1/3] First pass - generating structure..."
pdflatex -interaction=nonstopmode "${DOC}.tex" > /dev/null 2>&1
echo "✓ First pass complete"

# Second pass - resolve references
echo "[2/3] Second pass - resolving references..."
pdflatex -interaction=nonstopmode "${DOC}.tex" > /dev/null 2>&1
echo "✓ Second pass complete"

# Third pass - final cleanup
echo "[3/3] Third pass - final compilation..."
pdflatex -interaction=nonstopmode "${DOC}.tex" > /dev/null 2>&1
echo "✓ Third pass complete"

echo ""
echo "=========================================="
echo "✓ Compilation successful!"
echo "=========================================="
echo ""
echo "Output file: ${DOC}.pdf"
echo ""

# Check file size
if [ -f "${DOC}.pdf" ]; then
    SIZE=$(du -h "${DOC}.pdf" | cut -f1)
    PAGES=$(pdfinfo "${DOC}.pdf" 2>/dev/null | grep Pages | awk '{print $2}')

    echo "PDF Statistics:"
    echo "  - Size: ${SIZE}"
    if [ ! -z "$PAGES" ]; then
        echo "  - Pages: ${PAGES}"
    fi
    echo ""

    # Clean up auxiliary files
    echo "Cleaning up auxiliary files..."
    rm -f "${DOC}.aux" "${DOC}.log" "${DOC}.out" "${DOC}.toc"
    echo "✓ Cleanup complete"
    echo ""
fi

echo "To view the PDF:"
echo "  - Linux: xdg-open ${DOC}.pdf"
echo "  - macOS: open ${DOC}.pdf"
echo "  - Windows: start ${DOC}.pdf"
echo ""
