const test = require("node:test");
const assert = require("node:assert/strict");
const vm = require("node:vm");
const fs = require("node:fs");
const code = fs.readFileSync(require("node:path").join(__dirname, "../_static/mdas-notebooks.js"), "utf8");
function page() {
  const selector = {value: "live-coding.html"};
  const state = {events: {}, navigations: [], confirmations: 0, downloads: []};
  const original = {cells: [{cell_type: "markdown", source: ["# Original"]}, {cell_type: "code", source: ["old"], outputs: [1], execution_count: 1}]};
  const status = {};
  const editor = {CodeMirror: {getValue: () => "edited code"}};
  const context = {document: {
    getElementById: id => id === "mdas-notebook-select" ? selector : id === "mdas-notebook-source" ? {textContent: JSON.stringify(original)} : status,
    querySelectorAll: () => [{closest: () => ({querySelector: () => editor})}],
    createElement: () => ({click() {state.downloads.push(this.download);}}),
  }, Blob, URL: {createObjectURL(blob) {state.blob = blob; return "blob:test";}, revokeObjectURL() {}},
    setTimeout() {}, location: {assign: value => state.navigations.push(value)},
    confirm() {state.confirmations++; return state.approve;}, addEventListener: (name, handler) => {state.events[name] = handler;}};
  context.window = context;
  vm.createContext(context); vm.runInContext(code, context);
  return {context, selector, state, original, status};
}
test("static switching navigates to a separate page without launching anything", () => {
  const p = page(); p.selector.value = "live-coding-survival.html";
  p.context.mdasSwitchNotebook(p.selector);
  assert.deepEqual(p.state.navigations, ["live-coding-survival.html"]);
  assert.equal(p.state.confirmations, 0);
});
test("active session cancellation preserves page and resets selector", () => {
  const p = page(); p.context.mdasSessionStarted = true;
  p.selector.value = "live-coding-survival.html";
  p.context.mdasSwitchNotebook(p.selector);
  assert.equal(p.selector.value, "live-coding.html");
  assert.deepEqual(p.state.navigations, []);
  assert.equal(p.state.confirmations, 1);
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
test("export preserves original Markdown, saves edited code and clears stale outputs", async () => {
  const p = page(); p.context.mdasDownloadNotebook();
  const saved = JSON.parse(await p.state.blob.text());
  assert.deepEqual(saved.cells[0], p.original.cells[0]);
  assert.equal(saved.cells[1].source, "edited code");
  assert.deepEqual(saved.cells[1].outputs, []);
  assert.equal(saved.cells[1].execution_count, null);
  assert.deepEqual(p.state.downloads, ["classification_edited.ipynb"]);
});
test("export refuses an incomplete cell mapping", () => {
  const p = page(); p.context.document.querySelectorAll = () => [];
  p.context.mdasDownloadNotebook();
  assert.deepEqual(p.state.downloads, []);
  assert.match(p.status.textContent, /copy your edits manually/);
});

test("an active session never silently exports stale source when an editor is missing", () => {
  const p = page(); p.context.mdasSessionStarted = true;
  p.context.document.querySelectorAll = () => [{closest: () => ({querySelector: () => null})}];
  p.context.mdasDownloadNotebook();
  assert.deepEqual(p.state.downloads, []);
  assert.match(p.status.textContent, /editor is unavailable/);
});
