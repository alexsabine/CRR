// loads the model script out of forest.html, with no browser
const fs = require('fs'), path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', '..', 'forest.html'), 'utf8');
const m = /<script id="model">([\s\S]*?)<\/script>/.exec(html);
const mod = { exports: {} };
new Function('module', 'globalThis', m[1])(mod, {});
module.exports = mod.exports;
