#!/bin/sh
# Assembles ../../hive.html from the parts in this folder.
cd "$(dirname "$0")"
{ cat head.html about.html; echo '<script>'; cat hive_model.js; echo '</script>'; echo '<script>'; cat app.js; echo '</script>'; echo '</body>'; echo '</html>'; } > ../../hive.html
wc -c ../../hive.html
