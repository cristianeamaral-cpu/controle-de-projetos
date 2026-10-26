const {chromium}=require('playwright');const {spawn}=require('child_process');
const [,,dir,out,fps,only]=process.argv;
(async()=>{
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
 await p.goto('file://'+dir+'/index.html?render');await p.waitForTimeout(500);
 const D=await p.evaluate(()=>window.DURATION);
 if(only){for(const t of only.split(',')){await p.evaluate(t=>seek(t),+t);await p.screenshot({path:`${out}_${t}.png`})}await b.close();return}
 const ff=spawn('ffmpeg',['-y','-f','image2pipe','-framerate',fps,'-c:v','mjpeg','-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','medium','-movflags','+faststart',out],{stdio:['pipe','ignore','inherit']});
 const N=Math.round(D*fps);
 for(let f=0;f<N;f++){await p.evaluate(t=>seek(t),f/fps);const buf=await p.screenshot({type:'jpeg',quality:92});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));if(f%300==0)console.error('frame',f,'/',N)}
 ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();
})();
