const assert = require('node:assert/strict');
const test = require('node:test');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('site/_static/mdas-presentation.js', 'utf8');
function setup({fullscreen = true, reject = false} = {}) {
  const events = {}, handlers = {}, classes = new Set(), attrs = {};
  const button = {setAttribute: (k,v) => attrs[k]=v, addEventListener: (k,v) => handlers[k]=v};
  const header = {prepend: b => {assert.equal(b,button); header.mounted=true;}};
  const scrolls = [];
  const doc = {readyState:'complete', createElement:()=>button, getElementById:()=>null,
    querySelector:s => s==='.article-header-buttons'?header:null,
    addEventListener:(k,v)=>events[k]=v,
    documentElement:{classList:{toggle:(k,v)=>v?classes.add(k):classes.delete(k)}},
    exitFullscreen:async()=>{doc.fullscreenElement=null; events.fullscreenchange();}};
  if(fullscreen) doc.documentElement.requestFullscreen=async()=>{
    if(reject) throw Error('denied'); doc.fullscreenElement=doc.documentElement;
  };
  vm.runInNewContext(source,{document:doc,window:{scrollY:240,scrollTo:(x,y)=>scrolls.push(y)},requestAnimationFrame:fn=>fn()});
  return {doc,button,events,attrs,classes,scrolls,header,click:()=>handlers.click()};
}
test('mounts an accessible keyboard-operable header button without activating',()=>{
 const s=setup();assert.ok(s.header.mounted);assert.equal(s.button.type,'button');assert.equal(s.attrs['aria-pressed'],'false');assert.equal(s.classes.size,0);
});
test('enters and exits fullscreen with same toggle, restoring scroll',async()=>{
 const s=setup();await s.click();assert.ok(s.classes.has('mdas-presentation'));assert.ok(s.doc.fullscreenElement);assert.equal(s.attrs['aria-label'],'Exit presentation mode');
 await s.click();assert.equal(s.doc.fullscreenElement,null);assert.equal(s.classes.size,0);assert.equal(s.scrolls.at(-1),240);
});
test('unavailable or denied fullscreen retains layout fallback and Escape exits',async()=>{
 for(const options of [{fullscreen:false},{reject:true}]) {
  const s=setup(options);await s.click();assert.ok(s.classes.has('mdas-presentation'));let prevented=false;
  s.events.keydown({key:'Escape',preventDefault:()=>prevented=true});await Promise.resolve();
  assert.ok(prevented);assert.equal(s.classes.size,0);assert.equal(s.attrs['aria-pressed'],'false');
 }
});
test('native fullscreen exit restores navigation layout',async()=>{
 const s=setup();await s.click();s.doc.fullscreenElement=null;s.events.fullscreenchange();assert.equal(s.classes.size,0);
});
test('leaves externally owned fullscreen intact',async()=>{
 const s=setup();const owner={};s.doc.fullscreenElement=owner;await s.click();await s.click();assert.equal(s.doc.fullscreenElement,owner);
});
