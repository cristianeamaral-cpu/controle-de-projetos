const { chromium } = require('playwright');
(async()=>{
  const [,,mode,a,b]=process.argv;
  const br=await chromium.launch();
  const p=await br.newPage({viewport:{width:1920,height:1080}});
  await p.goto('file://'+__dirname+'/video.html'); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(500);
  if(mode==='test'){ for(const t of a.split(',')){ await p.evaluate(t=>seek(+t),t); await p.screenshot({path:`test_${t}.png`}); } }
  else { const fps=30,N=Math.round(+a*fps); require('fs').mkdirSync('frames',{recursive:true});
    for(let i=0;i<N;i++){ await p.evaluate(t=>seek(t),i/fps); await p.screenshot({path:`frames/f${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:92}); if(i%150==0)console.log(i,N);} }
  await br.close();
})();
