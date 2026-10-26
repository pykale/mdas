// Behavioural tests of the launch controller, without pretending to run a kernel.
const test = require("node:test");
const assert = require("node:assert/strict");
const vm = require("node:vm");
const fs = require("node:fs");
const path = require("node:path");
const code = fs.readFileSync(path.join(__dirname, "../_static/mdas-interactive.js"), "utf8");

function page(available = true, missing = [], httpStatus = 200) {
  const state = {launches: 0, checks: 0, executions: 0, observers: [], classes: new Set()};
  const label = {textContent: ""};
  const button = {disabled: false, classList: {add: value => state.classes.add(value)}, querySelector: () => label};
  const status = {textContent: "Not connected"};
  const preflight = {textContent: JSON.stringify({repository: "pykale/mmai-mdas", ref: "main",
    required_files: [".binder/runtime.txt", ".binder/requirements.txt", "notebooks/MDAS/cancer/cancer_live_coding.ipynb", "notebooks/MDAS/cancer/synthetic_data_generation.py"]})};
  const config = {textContent: JSON.stringify({binderOptions: {repo: "pykale/mmai-mdas", ref: "main"}})};
  const context = {
    document: {head: {}, getElementById: id => id === "mdas-thebe-launch" ? button : id === "mdas-binder-check" ? preflight : status,
      querySelector: () => config},
    AbortController,
    fetch: async () => {
      state.checks++;
      return {ok: httpStatus === 200, status: httpStatus, json: async () => ({sha: "a".repeat(40), truncated: false,
        tree: JSON.parse(preflight.textContent).required_files.filter(file => !missing.includes(file)).map(path => ({path, type: "blob"}))})};
    },
    MutationObserver: class { constructor(callback) { state.observers.push(callback); } observe() {} disconnect() {} },
    setTimeout: () => 1, clearTimeout: () => {}, queueMicrotask: callback => callback(),
  };
  context.window = context;
  if (available) {
    context.configureThebe = () => {};
    context.thebelab = {on: (_name, callback) => { state.statusEvent = callback; }};
    context.initThebe = () => { state.launches++; context.configureThebe(); };
  }
  vm.createContext(context); vm.runInContext(code, context);
  return {context, state, button, status, label, config};
}

test("reading the page starts no session and executes no code", () => {
  const p = page();
  assert.equal(p.state.launches, 0);
  assert.equal(p.state.checks, 0);
  assert.equal(p.state.executions, 0);
  assert.equal(p.button.disabled, false);
});

test("a deliberate click checks files, pins the checked commit and launches once", async () => {
  const p = page();
  await Promise.all([p.context.mdasLaunchInteractive(), p.context.mdasLaunchInteractive()]);
  assert.equal(p.state.launches, 1);
  assert.equal(p.state.checks, 1);
  assert.equal(JSON.parse(p.config.textContent).binderOptions.ref, "a".repeat(40));
  assert.match(p.status.textContent, /requesting a temporary Binder kernel/);
  p.state.statusEvent(null, {status: "ready"});
  assert.match(p.status.textContent, /Kernel connected/);
  assert.equal(p.label.textContent, "Interactive session connected");
  assert.equal(p.state.executions, 0);
});

test("unavailable scripts do not report success or remove the static content", async () => {
  const p = page(false); await p.context.mdasLaunchInteractive();
  assert.match(p.status.textContent, /saved notebook remains readable/);
  assert.equal(p.state.launches, 0);
  assert.equal(p.button.disabled, false);
});

test("a failed connection reports the backend detail without automatically retrying", async () => {
  const p = page(); await p.context.mdasLaunchInteractive();
  p.state.statusEvent(null, {status: "failed", message: "No environment specification found"});
  assert.match(p.status.textContent, /Connection failed/);
  assert.match(p.status.textContent, /Colab/);
  assert.match(p.status.textContent, /No environment specification found/);
  assert.equal(p.state.launches, 1);
  assert.equal(p.state.executions, 0);
});

test("missing remote Binder files prevent a known-bad launch and explain the local/remote mismatch", async () => {
  const p = page(true, [".binder/runtime.txt", ".binder/requirements.txt"]);
  await p.context.mdasLaunchInteractive();
  assert.equal(p.state.launches, 0);
  assert.equal(p.state.checks, 1);
  assert.equal(p.button.disabled, false);
  assert.match(p.status.textContent, /Missing: .binder\/runtime.txt, .binder\/requirements.txt/);
  assert.match(p.status.textContent, /Local files are not sent to Binder/);
  assert.match(p.status.textContent, /No Binder launch was requested/);
});

test("a GitHub rate limit is not misreported as missing dependencies or missing files", async () => {
  const p = page(true, [], 403); await p.context.mdasLaunchInteractive();
  assert.equal(p.state.launches, 0);
  assert.match(p.status.textContent, /HTTP 403/);
  assert.doesNotMatch(p.status.textContent, /Missing:/);
});
