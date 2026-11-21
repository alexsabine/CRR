/* Puts the page together: head.html + model.js + app.js (with the ported voice) -> ../../murmuration.html */
const fs = require('fs'), d = __dirname, r = f => fs.readFileSync(d + '/' + f, 'utf8');
const app = r('app.js').replace('/*AUDIO_PORT*/', () => r('audio_port.js'));
fs.writeFileSync(d + '/../../murmuration.html', r('head.html') + '\n<script>\n' + r('model.js') + '\n</script>\n<script>\n' + app + '\n</script>\n</body>\n</html>\n');
console.log('murmuration.html', fs.statSync(d + '/../../murmuration.html').size, 'bytes');
