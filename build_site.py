#!/usr/bin/env python3
"""Regenerates the static validation site (index/code/compare). Data lives in examples.json,
fetched at runtime, so the HTML stays small. Run from the site directory."""
import os

CSS = '''
  :root{--bg:#f5f6f8;--card:#fff;--ink:#1a1a2e;--mut:#666;--line:#e2e2e8;
        --threat:#c0392b;--nothreat:#2c7a3f;--skip:#7a7a8a;--accent:#2b4c8c;}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,Segoe UI,Roboto,Arial,sans-serif}
  .wrap{max-width:860px;margin:0 auto;padding:24px 18px 90px}
  h1{font-size:22px;margin:0 0 4px} h2{font-size:17px;margin:22px 0 8px}
  .sub{color:var(--mut);font-size:14px;margin:0 0 20px}
  .card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:22px;box-shadow:0 1px 2px rgba(0,0,0,.04);margin-bottom:16px}
  a{color:var(--accent)}
  .codebook{font-size:14px;color:#333;background:#eef2fb;border:1px solid #d6e0f5;border-radius:10px;padding:14px 16px;margin:0 0 18px}
  .codebook b{color:var(--accent)}
  .post{font-size:18px;line-height:1.55;white-space:pre-wrap;word-break:break-word;background:#fafafc;border:1px solid var(--line);border-radius:10px;padding:18px;min-height:90px;margin:0 0 18px}
  .btns{display:flex;gap:10px;flex-wrap:wrap}
  button{font:inherit;border:0;border-radius:10px;padding:13px 18px;cursor:pointer;color:#fff;font-weight:600;flex:1;min-width:120px}
  .b-threat{background:var(--threat)} .b-nothreat{background:var(--nothreat)}
  .b-skip{background:var(--skip)} .b-ghost{background:#e4e4ec;color:#333;font-weight:500}
  button:active{transform:translateY(1px)}
  input[type=text]{font:inherit;padding:10px 12px;border:1px solid var(--line);border-radius:8px;width:100%;margin:6px 0 4px}
  select{font:inherit;padding:9px 10px;border:1px solid var(--line);border-radius:8px;margin:6px 0}
  .bar{height:8px;background:var(--line);border-radius:99px;overflow:hidden;margin:0 0 8px}
  .bar > i{display:block;height:100%;background:var(--accent);width:0;transition:width .2s}
  .prog{display:flex;justify-content:space-between;font-size:13px;color:var(--mut);margin-bottom:16px}
  .nav{display:flex;justify-content:space-between;margin-top:14px} .nav button{flex:0 0 auto;min-width:0}
  .kbd{font-size:12px;color:var(--mut);margin-top:14px;text-align:center}
  .kbd b{background:#e4e4ec;border-radius:4px;padding:1px 6px;color:#333}
  table{border-collapse:collapse;width:100%;margin:8px 0 18px;font-size:14px}
  th,td{border:1px solid var(--line);padding:7px 9px;text-align:center}
  th{background:#eef2fb}
  .metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:0 0 16px}
  .metric{background:#fafafc;border:1px solid var(--line);border-radius:10px;padding:12px}
  .metric .v{font-size:24px;font-weight:700;color:var(--accent)} .metric .l{font-size:12px;color:var(--mut)}
  .dis{font-size:14px;border-top:1px solid var(--line);padding:10px 0}
  .tag{display:inline-block;font-size:12px;font-weight:600;border-radius:6px;padding:2px 8px;color:#fff;margin-right:4px}
  .hidden{display:none} .muted{color:var(--mut);font-size:13px}
  textarea{width:100%;min-height:90px;font:13px/1.4 monospace;border:1px solid var(--line);border-radius:8px;padding:10px}
  .drop{border:2px dashed #c4ccdd;border-radius:12px;padding:26px;text-align:center;color:var(--mut);background:#fafbfe}
  .pill{font-size:12px;background:#e4e4ec;border-radius:99px;padding:3px 10px;margin:3px;display:inline-block}
  .contest{background:#fff6e6}
'''

def page(title, body):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>')

# ---------------- index ----------------
index = page("Threat Classification Validation", '''
<div class="wrap">
  <h1>Threat Classification Validation</h1>
  <p class="sub">A blind human audit of how accurately the model flags violent / eliminationist and threatening posts toward Erika Kirk, and how much human coders agree with each other.</p>
  <div class="card"><h2>1. Audit the examples</h2>
    <p class="muted">Read posts and judge each yourself, without seeing the model&#39;s label. All 4,224 examples are loaded; you can stop whenever you like and download your work as a CSV.</p>
    <div class="btns"><button class="b-threat" style="flex:0;min-width:200px" onclick="location.href='code.html'">Start auditing &rarr;</button></div></div>
  <div class="card"><h2>2. Compare coders</h2>
    <p class="muted">Load two or more coders&#39; CSVs to see inter-coder agreement, a human consensus, and the model&#39;s accuracy against that consensus.</p>
    <div class="btns"><button class="b-ghost" style="flex:0;min-width:200px" onclick="location.href='compare.html'">Open comparison &rarr;</button></div></div>
  <p class="muted">All processing happens in your browser. Nothing is uploaded.</p>
</div>''')

# ---------------- code ----------------
code = page("Audit the Examples &middot; Threat Validation", '''
<div class="wrap">
  <h1>Audit the Examples</h1>
  <p class="sub"><a href="index.html">&larr; Home</a> &middot; Blind coding vs. the model&#39;s label.</p>
  <div id="intro" class="card">
    <div class="codebook" id="codebook"></div>
    <label class="muted">Which label are you auditing?</label><br>
    <select id="dim">
      <option value="elim">Violent / eliminationist toward Erika (flag_violent_or_eliminationist)</option>
      <option value="threat">Explicit threat or incitement (is_threat_toward_erika)</option>
    </select><br>
    <label class="muted">Your name or coder ID:</label>
    <input type="text" id="coder" placeholder="e.g. coder-A">
    <p class="muted" id="loadmsg">Loading examples&hellip;</p>
    <div class="btns"><button class="b-threat" id="startbtn" disabled onclick="start()">Start</button></div>
  </div>
  <div id="coding" class="card hidden">
    <div class="bar"><i id="fill"></i></div>
    <div class="prog"><span id="counter"></span><span id="codedcount"></span></div>
    <div class="post" id="posttext"></div>
    <div class="btns">
      <button class="b-threat" onclick="code(true)" id="yesbtn">Yes</button>
      <button class="b-nothreat" onclick="code(false)" id="nobtn">No</button>
      <button class="b-skip" onclick="code(null)">Skip</button>
    </div>
    <div class="nav">
      <button class="b-ghost" onclick="prev()">&larr; Back</button>
      <button class="b-ghost" onclick="finish()">Finish &amp; download</button>
    </div>
    <div class="kbd">Keys: <b>1</b> Yes &nbsp; <b>2</b> No &nbsp; <b>3</b> Skip &nbsp; <b>&larr;</b> Back &nbsp;&middot;&nbsp; progress is saved in this browser</div>
  </div>
  <div id="results" class="card hidden">
    <h1 style="font-size:19px">Results</h1>
    <p class="muted" id="rsummary"></p>
    <div class="metrics" id="metrics"></div>
    <h2>Confusion matrix <span class="muted">(your coding = truth)</span></h2>
    <table id="cm"></table>
    <h2>Download your audit</h2>
    <p class="muted">CSV with all examples, the model flags, and your judgment (<code>human_label</code>, <code>agree</code>). Merge back to your master sheet on <code>post_id</code>.</p>
    <div class="btns" style="margin-bottom:12px">
      <button class="b-threat" style="flex:0;min-width:200px" id="dlcsv">Download CSV</button>
      <button class="b-ghost" style="flex:0;min-width:140px" onclick="location.reload()">Restart</button>
    </div>
    <h2>Disagreements with the model</h2>
    <div id="dislist"></div>
  </div>
</div>
<script>
let DATA=[], i=0, ans=[], DIM='elim';
const DEFS={
  elim:{q:'Does this post threaten, call for, wish, justify, or celebrate <b>violence against or the death of Erika Kirk</b>?',
        field:'m_elim', col:'flag_violent_or_eliminationist'},
  threat:{q:'Does this post contain an <b>explicit threat or incitement of harm toward Erika Kirk</b> (a direct threat, or urging others to harm her)?',
           field:'m_threat', col:'is_threat_toward_erika'}
};
function codebookHtml(){ const d=DEFS[document.getElementById('dim')?document.getElementById('dim').value:'elim'];
  return '<b>Your task.</b> '+d.q+'<br><br><b>Yes</b> if it does. <b>No</b> if it is hostile/insulting/accusatory but does not. <b>Skip</b> only if impossible to judge. Judge by the text alone &mdash; don&#39;t guess the model&#39;s answer.'; }
function refreshCodebook(){ document.getElementById('codebook').innerHTML=codebookHtml(); }
fetch('examples.json').then(r=>r.json()).then(d=>{ DATA=d; ans=new Array(DATA.length).fill(undefined);
  document.getElementById('loadmsg').textContent=DATA.length.toLocaleString()+' examples loaded.';
  document.getElementById('startbtn').disabled=false; refreshCodebook(); });
document.addEventListener('change',e=>{ if(e.target.id==='dim') refreshCodebook(); });
const LS='erika_audit_progress';
function save(){ try{localStorage.setItem(LS,JSON.stringify({DIM,coder:document.getElementById('coder').value,i,ans}));}catch(e){} }
function start(){ DIM=document.getElementById('dim').value;
  document.getElementById('yesbtn').textContent = DIM==='elim'?'Violent / eliminationist':'Threat';
  document.getElementById('nobtn').textContent='No';
  // resume?
  try{const s=JSON.parse(localStorage.getItem(LS)); if(s&&s.DIM===DIM&&Array.isArray(s.ans)&&s.ans.length===DATA.length&&s.ans.some(x=>x!==undefined)){
    if(confirm('Resume your saved progress for this label?')){ ans=s.ans; i=s.i||0; } }}catch(e){}
  show('coding'); render(); }
function show(id){ for(const s of ['intro','coding','results']) document.getElementById(s).classList.add('hidden'); document.getElementById(id).classList.remove('hidden'); }
function render(){ const d=DATA[i];
  document.getElementById('posttext').textContent=d.text;
  document.getElementById('counter').textContent='Post '+(i+1).toLocaleString()+' of '+DATA.length.toLocaleString();
  document.getElementById('codedcount').textContent=ans.filter(a=>a!==undefined).length+' coded';
  document.getElementById('fill').style.width=(100*i/DATA.length)+'%'; }
function code(v){ ans[i]=v; save(); if(i<DATA.length-1){i++;render();}else finish(); }
function prev(){ if(i>0){i--;render();} }
function finish(){ computeResults(); show('results'); }
document.addEventListener('keydown',e=>{ if(document.getElementById('coding').classList.contains('hidden'))return;
  if(e.key==='1')code(true); else if(e.key==='2')code(false); else if(e.key==='3')code(null); else if(e.key==='ArrowLeft')prev(); });
function wilson(k,n){ if(!n)return[0,0]; const z=1.96,p=k/n,d=1+z*z/n; const c=(p+z*z/(2*n))/d,h=z*Math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d; return[Math.max(0,c-h),Math.min(1,c+h)]; }
function esc(s){return (''+s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function mlabel(d){ return d[DEFS[DIM].field]; }
function computeResults(){
  let tp=0,fp=0,tn=0,fn=0,agree=0,n=0; const dis=[];
  DATA.forEach((d,idx)=>{ const h=ans[idx]; if(h===undefined||h===null)return; n++; const m=mlabel(d);
    if(h===m)agree++; else dis.push({d,h,m}); if(m&&h)tp++; else if(m&&!h)fp++; else if(!m&&!h)tn++; else fn++; });
  const acc=n?agree/n:0, prec=(tp+fp)?tp/(tp+fp):0, rec=(tp+fn)?tp/(tp+fn):0, f1=(prec+rec)?2*prec*rec/(prec+rec):0;
  const pmY=(tp+fp)/n, phY=(tp+fn)/n, pe=pmY*phY+(1-pmY)*(1-phY), kappa=(1-pe)?(acc-pe)/(1-pe):0;
  const [lo,hi]=wilson(agree,n);
  document.getElementById('rsummary').innerHTML=n+' coded of '+DATA.length.toLocaleString()+'. Auditing <code>'+DEFS[DIM].col+'</code>. &ldquo;Truth&rdquo; = your coding.';
  const M=[['Agreement',(100*acc).toFixed(1)+'%'],['95% CI',(100*lo).toFixed(0)+'&ndash;'+(100*hi).toFixed(0)+'%'],
    ['Precision',(100*prec).toFixed(1)+'%'],['Recall',(100*rec).toFixed(1)+'%'],['F1',f1.toFixed(3)],["Cohen&#39;s &kappa;",kappa.toFixed(3)]];
  document.getElementById('metrics').innerHTML=M.map(m=>'<div class="metric"><div class="v">'+m[1]+'</div><div class="l">'+m[0]+'</div></div>').join('');
  document.getElementById('cm').innerHTML='<tr><th></th><th>You: Yes</th><th>You: No</th></tr><tr><th>Model: Yes</th><td>'+tp+'</td><td>'+fp+'</td></tr><tr><th>Model: No</th><td>'+fn+'</td><td>'+tn+'</td></tr>';
  document.getElementById('dislist').innerHTML=dis.length?dis.slice(0,200).map(x=>{
    const mt=x.m?'<span class="tag" style="background:var(--threat)">Model: Yes</span>':'<span class="tag" style="background:var(--nothreat)">Model: No</span>';
    const ht=x.h?'<span class="tag" style="background:var(--threat)">You: Yes</span>':'<span class="tag" style="background:var(--nothreat)">You: No</span>';
    return '<div class="dis">'+mt+ht+'<br>'+esc(x.d.text)+'</div>';}).join('')+(dis.length>200?'<p class="muted">(showing first 200 of '+dis.length+')</p>':''):'<p class="muted">No disagreements.</p>';
  document.getElementById('dlcsv').onclick=downloadCSV;
}
function csvCell(s){ s=(s===null||s===undefined)?'':''+s; return '"'+s.replace(/"/g,'""')+'"'; }
function downloadCSV(){
  const coder=(document.getElementById('coder').value||'coder').trim();
  const hdr=['post_id','body','is_hostile_toward_erika','is_threat_toward_erika','is_violence_toward_erika',
             'flag_violent_or_eliminationist','mentions_candace','audited_dimension','model_label','human_label','agree','coder'];
  const lines=[hdr.join(',')];
  DATA.forEach((d,idx)=>{ const h=ans[idx]; const m=mlabel(d);
    const hl=(h===true)?'TRUE':(h===false)?'FALSE':'';
    const ag=(h===true||h===false)?((h===m)?'TRUE':'FALSE'):'';
    lines.push([csvCell(d.post_id),csvCell(d.text),d.m_hostile?'TRUE':'FALSE',d.m_threat?'TRUE':'FALSE',
      d.m_violence?'TRUE':'FALSE',d.m_elim?'TRUE':'FALSE',d.m_candace?'TRUE':'FALSE',
      DEFS[DIM].col, m?'TRUE':'FALSE', hl, ag, csvCell(coder)].join(',')); });
  const blob=new Blob([lines.join('\\n')],{type:'text/csv'});
  const safe=coder.replace(/[^a-z0-9_-]/gi,'_');
  const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='erika_audit_'+DEFS[DIM].col+'_'+safe+'.csv'; a.click();
}
</script>''')

# ---------------- compare ----------------
compare = page("Compare Coders &middot; Threat Validation", '''
<div class="wrap">
  <h1>Compare Coders</h1>
  <p class="sub"><a href="index.html">&larr; Home</a> &middot; Load each coder&#39;s audit CSV.</p>
  <div class="card">
    <div class="drop" id="drop">Drop coder CSV files here, or <label style="color:var(--accent);cursor:pointer;text-decoration:underline">browse<input type="file" id="file" multiple accept=".csv" class="hidden"></label></div>
    <div id="loaded" style="margin-top:12px"></div>
    <div class="btns" style="margin-top:8px"><button class="b-ghost" style="flex:0;min-width:120px" onclick="reset()">Clear all</button></div>
    <p class="muted" id="warn"></p>
  </div>
  <div id="out"></div>
</div>
<script>
let coders=[]; const MODEL={}, TEXT={}; let dims=new Set();
const drop=document.getElementById('drop'), file=document.getElementById('file');
drop.addEventListener('dragover',e=>{e.preventDefault();drop.style.background='#eef2fb';});
drop.addEventListener('dragleave',()=>drop.style.background='');
drop.addEventListener('drop',e=>{e.preventDefault();drop.style.background='';[...e.dataTransfer.files].forEach(readFile);});
file.addEventListener('change',e=>[...e.target.files].forEach(readFile));
function readFile(f){ const r=new FileReader(); r.onload=()=>addCSV(r.result,f.name); r.readAsText(f); }
function parseCSV(t){ // minimal RFC4180 parser
  const rows=[]; let i=0,field='',row=[],q=false;
  while(i<t.length){ const c=t[i];
    if(q){ if(c==='"'){ if(t[i+1]==='"'){field+='"';i++;} else q=false; } else field+=c; }
    else { if(c==='"')q=true; else if(c===','){row.push(field);field='';} else if(c==='\\n'||c==='\\r'){ if(c==='\\r'&&t[i+1]==='\\n')i++; row.push(field);field=''; if(row.length>1||row[0]!=='')rows.push(row); row=[]; } else field+=c; }
    i++; }
  if(field!==''||row.length){ row.push(field); rows.push(row); }
  return rows; }
function addCSV(txt,name){
  const rows=parseCSV(txt); if(rows.length<2){alert('Empty CSV: '+name);return;}
  const h=rows[0]; const idx={}; h.forEach((c,k)=>idx[c.trim()]=k);
  for(const need of ['post_id','model_label','human_label']){ if(!(need in idx)){alert(name+' missing column: '+need);return;} }
  const coderName=(idx['coder']!=null && rows[1][idx['coder']])||name.replace(/\\.csv$/,'');
  const dim=(idx['audited_dimension']!=null && rows[1][idx['audited_dimension']])||'?'; dims.add(dim);
  const map={};
  for(let r=1;r<rows.length;r++){ const row=rows[r]; const pid=row[idx['post_id']]; if(!pid)continue;
    const hl=(row[idx['human_label']]||'').toUpperCase(); const ml=(row[idx['model_label']]||'').toUpperCase();
    if(ml==='TRUE'||ml==='FALSE') MODEL[pid]=(ml==='TRUE');
    if(idx['body']!=null && !(pid in TEXT)) TEXT[pid]=row[idx['body']];
    map[pid] = hl==='TRUE'?true : hl==='FALSE'?false : null; }
  coders.push({coder:coderName,dim,map}); renderLoaded(); compute(); }
function renderLoaded(){ document.getElementById('loaded').innerHTML=coders.length?('Loaded: '+coders.map((c,k)=>'<span class="pill">'+esc(c.coder)+' <span class="muted">['+esc(c.dim)+']</span> <a href="#" onclick="rm('+k+');return false">&times;</a></span>').join('')):'';
  document.getElementById('warn').innerHTML = dims.size>1?'&#9888; Coders audited different labels ('+[...dims].join(', ')+'). Compare only files with the same audited_dimension.':''; }
function rm(k){ coders.splice(k,1); compute(); renderLoaded(); }
function reset(){ coders=[]; for(const k in MODEL)delete MODEL[k]; dims=new Set(); document.getElementById('out').innerHTML=''; renderLoaded(); }
function esc(s){return (''+s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function maj(v){ const t=v.filter(x=>x===true).length,n=v.filter(x=>x===false).length; if(t===n)return{label:null,tie:true}; return{label:t>n,tie:false}; }
function compute(){
  const out=document.getElementById('out'); if(!coders.length){out.innerHTML='';return;}
  const ids=Object.keys(MODEL);
  let html='<div class="card"><h2>Each coder vs. the model</h2><table><tr><th>Coder</th><th>Coded</th><th>Agree</th><th>Precision</th><th>Recall</th></tr>';
  coders.forEach(c=>{ let tp=0,fp=0,tn=0,fn=0,ag=0,n=0;
    ids.forEach(id=>{ const h=c.map[id]; if(h!==true&&h!==false)return; const m=MODEL[id]; n++; if(h===m)ag++;
      if(m&&h)tp++; else if(m&&!h)fp++; else if(!m&&!h)tn++; else fn++; });
    const prec=(tp+fp)?tp/(tp+fp):0, rec=(tp+fn)?tp/(tp+fn):0;
    html+='<tr><td>'+esc(c.coder)+'</td><td>'+n+'</td><td>'+(n?(100*ag/n).toFixed(1):'-')+'%</td><td>'+(100*prec).toFixed(0)+'%</td><td>'+(100*rec).toFixed(0)+'%</td></tr>'; });
  html+='</table></div>';
  if(coders.length>=2){
    html+='<div class="card"><h2>Inter-coder agreement</h2><table><tr><th></th>'+coders.map(c=>'<th>'+esc(c.coder)+'</th>').join('')+'</tr>';
    let sAg=0,sK=0,pairs=0;
    coders.forEach((a,ai)=>{ html+='<tr><th>'+esc(a.coder)+'</th>';
      coders.forEach((b,bi)=>{ if(bi<=ai){html+='<td class="muted">&middot;</td>';return;}
        let ag=0,n=0,aT=0,bT=0; ids.forEach(id=>{ const x=a.map[id],y=b.map[id]; if((x!==true&&x!==false)||(y!==true&&y!==false))return; n++; if(x===y)ag++; if(x)aT++; if(y)bT++; });
        const po=n?ag/n:0, pe=n?((aT/n)*(bT/n)+(1-aT/n)*(1-bT/n)):0, k=(1-pe)?(po-pe)/(1-pe):0; sAg+=po;sK+=k;pairs++;
        html+='<td>'+(n?(100*po).toFixed(0):'-')+'%<br><span class="muted">&kappa;='+k.toFixed(2)+' (n='+n+')</span></td>'; });
      html+='</tr>'; });
    html+='</table><p class="muted">Mean pairwise agreement '+(100*sAg/pairs).toFixed(1)+'% &middot; mean &kappa; '+(sK/pairs).toFixed(3)+'</p></div>';
  }
  let tp=0,fp=0,tn=0,fn=0,ag=0,n=0,ties=0;
  ids.forEach(id=>{ const v=coders.map(c=>c.map[id]).filter(x=>x===true||x===false); if(!v.length)return;
    const m=maj(v); if(m.tie){ties++;return;} const ml=MODEL[id]; n++; if(ml===m.label)ag++;
    if(ml&&m.label)tp++; else if(ml&&!m.label)fp++; else if(!ml&&!m.label)tn++; else fn++; });
  const prec=(tp+fp)?tp/(tp+fp):0, rec=(tp+fn)?tp/(tp+fn):0, f1=(prec+rec)?2*prec*rec/(prec+rec):0;
  html+='<div class="card"><h2>Model vs. human consensus</h2><div class="metrics">'+
    '<div class="metric"><div class="v">'+(n?(100*ag/n).toFixed(1):'-')+'%</div><div class="l">Accuracy</div></div>'+
    '<div class="metric"><div class="v">'+(100*prec).toFixed(0)+'%</div><div class="l">Precision</div></div>'+
    '<div class="metric"><div class="v">'+(100*rec).toFixed(0)+'%</div><div class="l">Recall</div></div></div>'+
    '<table><tr><th></th><th>Consensus: Yes</th><th>Consensus: No</th></tr><tr><th>Model: Yes</th><td>'+tp+'</td><td>'+fp+'</td></tr><tr><th>Model: No</th><td>'+fn+'</td><td>'+tn+'</td></tr></table>'+
    '<p class="muted">'+n+' items with a majority; '+ties+' tied (excluded). F1='+f1.toFixed(3)+'</p></div>';
  html+='<div class="card"><h2>Contested &amp; model-disagreement items</h2><table><tr><th>Post</th>'+coders.map(c=>'<th>'+esc(c.coder)+'</th>').join('')+'<th>Model</th></tr>';
  ids.forEach(id=>{ const v=coders.map(c=>c.map[id]).filter(x=>x===true||x===false); if(!v.length)return;
    const m=maj(v); const split=new Set(v).size>1; const diff=!m.tie&&MODEL[id]!==m.label; if(!(split||diff))return;
    html+='<tr class="contest"><td style="text-align:left;max-width:340px">'+esc((TEXT[id]||'').slice(0,160))+'</td>'+
      coders.map(c=>{const h=c.map[id];return '<td>'+(h===true?'Y':h===false?'N':'&middot;')+'</td>';}).join('')+'<td>'+(MODEL[id]?'Y':'N')+'</td></tr>'; });
  html+='</table><p class="muted">Y/N = the audited label. Rows where coders split or the model differs from consensus.</p></div>';
  out.innerHTML=html;
}
</script>''')

open('index.html','w').write(index)
open('code.html','w').write(code)
open('compare.html','w').write(compare)
print('wrote index.html, code.html, compare.html')
