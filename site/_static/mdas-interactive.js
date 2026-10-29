/* Optional enhancement. No network connection or notebook execution on load. */
(() => {
  "use strict";
  let launched = false;
  let observed = false;
  let slowTimer;
  const status = () => document.getElementById("mdas-thebe-status");
  const button = () => document.getElementById("mdas-thebe-launch");
  const report = (text) => { if (status()) status().textContent = text; };
  const fail = (detail = "") => {
    clearTimeout(slowTimer);
    const reason = typeof detail === "string" && detail ? ` Backend message: ${detail.slice(0, 1000)}.` : "";
    report(`Connection failed.${reason} The saved notebook is still available. Open the Binder build logs for the failure phase, try Colab, or reload before retrying.`);
    if (button()) button().classList.add("mdas-connection-failed");
  };

  async function checkRemoteEnvironment() {
    const configNode = document.getElementById("mdas-binder-check");
    if (!configNode) throw new Error("The page's Binder preflight configuration is missing. Rebuild and reload the page.");
    const config = JSON.parse(configNode.textContent);
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15000);
    try {
      const api = `https://api.github.com/repos/${config.repository}/git/trees/${encodeURIComponent(config.ref)}?recursive=1`;
      const response = await fetch(api, {
        headers: {Accept: "application/vnd.github+json"}, signal: controller.signal, cache: "no-store",
      });
      if (!response.ok) {
        throw new Error(`Cannot check public GitHub revision ${config.ref} (HTTP ${response.status}). It may be unavailable, private, rate-limited or blocked. No Binder launch was requested.`);
      }
      const tree = await response.json();
      if (!Array.isArray(tree.tree) || !/^[0-9a-f]{40}$/.test(tree.sha || "")) {
        throw new Error("GitHub returned an invalid repository tree. No Binder launch was requested.");
      }
      const files = new Set(tree.tree.filter(item => item.type === "blob").map(item => item.path));
      const missing = config.required_files.filter(file => !files.has(file));
      if (missing.length) {
        if (tree.truncated) throw new Error("GitHub returned an incomplete file tree; environment readiness cannot be determined. No Binder launch was requested.");
        throw new Error(`Binder environment is unavailable on ${config.repository}@${config.ref} (${tree.sha.slice(0, 7)}). Missing: ${missing.join(", ")}. Local files are not sent to Binder; the reviewed files must exist on the configured public revision. No Binder launch was requested.`);
      }
      // Use exactly the commit just checked, rather than a moving main branch.
      const thebeNode = document.querySelector('script[type="text/x-thebe-config"]');
      if (!thebeNode) throw new Error("The page's Thebe configuration is missing. Rebuild and reload.");
      const thebe = JSON.parse(thebeNode.textContent);
      thebe.binderOptions.ref = tree.sha;
      thebeNode.textContent = JSON.stringify(thebe);
      return tree.sha;
    } finally {
      clearTimeout(timeout);
    }
  }

  window.mdasLaunchInteractive = async () => {
    if (launched) return;
    if (typeof window.initThebe !== "function" || typeof window.configureThebe !== "function") {
      report("Interactive scripts are not available yet. Wait for the page to finish loading, or use Colab. The saved notebook remains readable.");
      return;
    }
    launched = true;
    window.mdasSessionStarted = true;
    button().disabled = true;
    report("Checking that the public GitHub revision contains the Binder environment and notebook files. No Binder session has been requested yet.");
    try {
      await checkRemoteEnvironment();
    } catch (error) {
      report(error.name === "AbortError"
        ? "The GitHub readiness check timed out. No Binder session was requested. Read the saved notebook, use Colab, or retry later."
        : `Cannot launch: ${error.message} The saved notebook and Colab link remain available.`);
      launched = false;
      window.mdasSessionStarted = false;
      button().disabled = false;
      return;
    }
    report("Loading Thebe and requesting a temporary Binder kernel. The first environment build may take several minutes. No notebook cells will run automatically.");
    slowTimer = setTimeout(() => report("Binder is still starting. Public capacity and first-build times vary; you can keep reading or use Colab instead."), 180000);

    // Hook supported status events before sphinx-thebe calls bootstrap.
    const configure = window.configureThebe;
    window.configureThebe = () => {
      if (!observed) {
        observed = true;
        window.thebelab.on("status", (_event, data) => {
          if (data.status === "ready") {
            clearTimeout(slowTimer);
            report("Kernel connected. Edit and run cells individually, in order. Training and advanced comparisons may be slow; changes are temporary.");
            button().classList.add("mdas-kernel-ready");
            queueMicrotask(() => {
              const label = button().querySelector(".loading-text");
              if (label) label.textContent = "Interactive session connected";
            });
          } else if (["failed", "error", "dead", "disconnected"].includes(data.status)) {
            fail(typeof data.message === "string" ? data.message : "");
          } else {
            report(`Binder connection: ${data.status}. Please wait; no notebook cells are being run automatically.`);
          }
        });
      }
      return configure();
    };
    // The upstream loader is lazy; report a CDN failure without hiding content.
    const observer = new MutationObserver((records) => records.forEach((record) => {
      record.addedNodes.forEach((node) => {
        if (node.tagName === "SCRIPT" && node.src.includes("thebe@")) {
          node.addEventListener("error", fail, {once: true});
          node.addEventListener("load", () => observer.disconnect(), {once: true});
        }
      });
    }));
    observer.observe(document.head, {childList: true});
    try { window.initThebe(); } catch (_error) { observer.disconnect(); fail(); }
  };
})();
