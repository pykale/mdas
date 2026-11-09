const test = require("node:test");
const assert = require("node:assert/strict");
const vm = require("node:vm");
const fs = require("node:fs");
const code = fs.readFileSync(require("node:path").join(__dirname, "../_static/mdas-notebooks.js"), "utf8");
function page() {
  const events = {};
  const context = {addEventListener: (name, handler) => {events[name] = handler;}};
  context.window = context;
  vm.createContext(context); vm.runInContext(code, context);
  return {context, events};
}
test("reading independent example pages requires no picker or notebook DOM", () => {
  const p = page();
  assert.equal(typeof p.events.beforeunload, "function");
  assert.equal(p.context.mdasSwitchNotebook, undefined);
  assert.equal(p.context.mdasDownloadNotebook, undefined);
});
test("links and reloads are unblocked before a participant launches Binder", () => {
  const p = page(); let blocked = false;
  p.events.beforeunload({preventDefault() {blocked = true;}});
  assert.equal(blocked, false);
});
test("all leave paths are protected after launch without a dropdown", () => {
  const p = page(); p.context.mdasSessionStarted = true;
  let blocked = false;
  const event = {preventDefault() {blocked = true;}};
  p.events.beforeunload(event);
  assert.equal(blocked, true);
  assert.equal(event.returnValue, "");
  // Failed/disconnected sessions retain the flag: unsaved work is still protected.
  blocked = false; p.events.beforeunload(event);
  assert.equal(blocked, true);
});
