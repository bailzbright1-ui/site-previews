// node tools/shots.js slug [slug...]  -> qa/<slug>-full.png (scrolled, 1440) and qa/<slug>-m.png (390 first screen)
const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();for(const s of process.argv.slice(2)){
 const u='file://'+path.resolve('docs',s,'index.html');
 let p=await b.newPage({viewport:{width:1440,height:900}});await p.goto(u);await p.waitForTimeout(1200);
 await p.addStyleTag({content:'html{scroll-behavior:auto!important}'});await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=500){scrollTo(0,y);await new Promise(r=>setTimeout(r,90))}scrollTo(0,0);await new Promise(r=>setTimeout(r,500))});
 await p.screenshot({path:`qa/${s}-full.png`,fullPage:true});await p.close();
 p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:2});await p.goto(u);await p.waitForTimeout(1300);await p.screenshot({path:`qa/${s}-m.png`});await p.close();}
 await b.close()})();
