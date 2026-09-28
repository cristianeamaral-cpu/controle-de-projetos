const {chromium}=require('/opt/node22/lib/node_modules/playwright');
const FPS=30,[w,W]=process.argv.slice(2).map(Number);
(async()=>{
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
 p.on('pageerror',e=>console.log('ERR',e.message));
 await p.goto('file://'+process.cwd()+'/video_built.html'); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(400);
 const END=await p.evaluate(()=>END); const N=Math.ceil(END*FPS);
 const per=Math.ceil(N/W), a=w*per, z=Math.min(N,a+per);
 for(let f=a;f<z;f++){await p.evaluate(t=>render(t),f/FPS);
   await p.screenshot({path:`frames/f${String(f).padStart(5,'0')}.jpg`,quality:93});}
 console.log('worker',w,'done',a,z,N); await b.close();})();
