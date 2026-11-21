#!/bin/sh
# Assembles ../../mycelium.html from head.html, model.js and view.js. No other step.
cd "$(dirname "$0")"
{ cat head.html; echo; echo '<script id="model">'; cat model.js; echo '</script>'; echo; echo '<script>'; cat view.js; echo '</script>'; echo '</body>'; echo '</html>'; } > ../../mycelium.html
