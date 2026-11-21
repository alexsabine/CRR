#!/bin/sh
# Joins the parts into the one self-contained page. Run from anywhere.
cd "$(dirname "$0")"
{ cat head.html; echo '<script>'; cat model.js; echo '</script>'; echo '<script>'; cat audio.js; echo '</script>'; echo '<script>'; cat view.js; echo '</script>'; echo '</body>'; echo '</html>'; } > ../../willow.html
wc -c ../../willow.html
