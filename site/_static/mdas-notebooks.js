/* Page navigation only: never replace an active notebook DOM/session. */
(() => {
  "use strict";
  const selector = document.getElementById("mdas-notebook-select");
  if (!selector) return;
  const initial = selector.value;
  window.mdasSwitchNotebook = (select) => {
    if (select.value === initial) return;
    if (window.mdasSessionStarted && !window.confirm(
      "Switch notebooks and leave this interactive session? Unsaved edits and results will be lost. Cancel and use Download notebook with edits first; download generated data separately."
    )) {
      select.value = initial;
      return;
    }
    window.location.assign(select.value);
  };
  // Protect reloads, sidebar links and closing the tab as well as the selector.
  window.addEventListener("beforeunload", (event) => {
    if (window.mdasSessionStarted) {
      event.preventDefault();
      event.returnValue = "";
    }
  });
  window.addEventListener("pageshow", () => { selector.value = initial; });
  window.mdasDownloadNotebook = () => {
    const status = document.getElementById("mdas-download-status");
    try {
      const notebook = JSON.parse(document.getElementById("mdas-notebook-source").textContent);
      const cells = notebook.cells.filter(cell => cell.cell_type === "code");
      const inputs = Array.from(document.querySelectorAll(".cell_input"));
      if (inputs.length !== cells.length) throw new Error("Cannot match every code cell for export. Keep this page open and copy your edits manually.");
      cells.forEach((cell, index) => {
        const editor = inputs[index].closest(".cell").querySelector(".CodeMirror");
        if (window.mdasSessionStarted && !(editor && editor.CodeMirror)) {
          throw new Error("An interactive editor is unavailable for export. Keep this page open and copy your edits manually.");
        }
        if (editor && editor.CodeMirror) cell.source = editor.CodeMirror.getValue();
        // Saved outputs do not describe the edited code or current kernel state.
        cell.outputs = [];
        cell.execution_count = null;
      });
      const url = URL.createObjectURL(new Blob([JSON.stringify(notebook, null, 2)], {type: "application/x-ipynb+json"}));
      const link = document.createElement("a");
      link.href = url;
      link.download = initial.includes("survival") ? "survival_edited.ipynb" : "classification_edited.ipynb";
      link.click();
      setTimeout(() => URL.revokeObjectURL(url), 10000);
      status.textContent = "Notebook download requested with current code edits and original Markdown. Outputs, kernel state and generated files are not included. Check your download before leaving.";
    } catch (error) {
      status.textContent = error.message;
    }
  };
})();
