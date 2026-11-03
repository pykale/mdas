const test = require("node:test");
const assert = require("node:assert/strict");
const vm = require("node:vm");
const fs = require("node:fs");
const code = fs.readFileSync(require("node:path").join(__dirname, "../_static/mdas-notebooks.js"), "utf8");
function page(initial = "live-coding.html") {
  const selector = {value: initial};
  const state = {events: {}, navigations: [], confirmations: 0};
  const context = {document: {getElementById: () => selector},
    location: {assign: value => state.navigations.push(value)},
    confirm(message) {state.confirmations++; state.warning = message; return state.approve;},
    addEventListener: (name, handler) => {state.events[name] = handler;}};
  context.window = context;
  vm.createContext(context); vm.runInContext(code, context);
  return {context, selector, state};
}
test("static switching navigates to a separate page in either direction", () => {
  for (const [initial, target] of [["live-coding.html", "live-coding-survival.html"], ["live-coding-survival.html", "live-coding.html"]]) {
    const p = page(initial); p.selector.value = target;
    p.context.mdasSwitchNotebook(p.selector);
    assert.deepEqual(p.state.navigations, [target]);
    assert.equal(p.state.confirmations, 0);
  }
});
test("active session cancellation preserves page and resets selector", () => {
  const p = page(); p.context.mdasSessionStarted = true;
  p.selector.value = "live-coding-survival.html";
  p.context.mdasSwitchNotebook(p.selector);
  assert.equal(p.selector.value, "live-coding.html");
  assert.deepEqual(p.state.navigations, []);
  assert.equal(p.state.confirmations, 1);
  assert.match(p.state.warning, /copy code edits and important results/);
  assert.doesNotMatch(p.state.warning, /Download notebook/);
  p.state.approve = true; p.selector.value = "live-coding-survival.html";
  p.context.mdasSwitchNotebook(p.selector);
  assert.deepEqual(p.state.navigations, ["live-coding-survival.html"]);
});
test("reload and navigation are protected after launch, including failed/disconnected sessions", () => {
  const p = page(); let blocked = false;
  const event = {preventDefault() {blocked = true;}};
  p.state.events.beforeunload(event); assert.equal(blocked, false);
  p.context.mdasSessionStarted = true;
  p.state.events.beforeunload(event); assert.equal(blocked, true);
  assert.equal(event.returnValue, "");
});
test("selecting the current notebook leaves an active session alone", () => {
  const p = page(); p.context.mdasSessionStarted = true;
  p.context.mdasSwitchNotebook(p.selector);
  assert.deepEqual(p.state.navigations, []);
  assert.equal(p.state.confirmations, 0);
});
test("history restoration resets the selector to the displayed notebook", () => {
  const p = page("live-coding-survival.html");
  p.selector.value = "live-coding.html";
  p.state.events.pageshow();
  assert.equal(p.selector.value, "live-coding-survival.html");
});
test("removed export controller is absent; switching guards remain independent of notebook DOM", () => {
  const p = page();
  assert.equal(p.context.mdasDownloadNotebook, undefined);
  assert.equal(typeof p.state.events.beforeunload, "function");
});
