// node render.js preview 3,12,20  -> PNGs  |  node render.js video out.mp4 [fps]
// Também grava timeline.json (início da locução de cada cena) para o mixar.sh.
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const { spawn } = require('child_process');
const path = require('path');

(async () => {
  const [mode, arg, fpsArg] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.join(__dirname, 'voo.html'));
  await page.evaluate(() => window.ready);
  const tl = await page.evaluate(() => ({ duration: window.DURATION, scenes: window.TIMELINE }));
  require('fs').writeFileSync(path.join(__dirname, 'timeline.json'), JSON.stringify(tl, null, 1));
  if (mode === 'preview') {
    for (const t of arg.split(',').map(Number)) {
      await page.evaluate(t => window.seek(t), t);
      await page.screenshot({ path: path.join(__dirname, `prev_${t}.png`) });
    }
  } else {
    const fps = +(fpsArg || 30), dur = await page.evaluate(() => window.DURATION);
    const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', '-movflags', '+faststart', arg], { stdio: ['pipe', 'inherit', 'inherit'] });
    const n = Math.round(dur * fps);
    for (let i = 0; i < n; i++) {
      await page.evaluate(t => window.seek(t), i / fps);
      const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % 300 === 0) console.error(`frame ${i}/${n}`);
    }
    ff.stdin.end();
    await new Promise(r => ff.on('close', r));
  }
  await browser.close();
})();
