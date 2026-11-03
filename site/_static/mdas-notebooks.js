/* Page navigation only: never replace an active notebook DOM/session. */
(() => {
  "use strict";
  const selector = document.getElementById("mdas-notebook-select");
  if (!selector) return;
  const initial = selector.value;
  window.mdasSwitchNotebook = (select) => {
    if (select.value === initial) return;
    if (window.mdasSessionStarted && !window.confirm(
      "Switch notebooks and leave this interactive session? Unsaved edits and results will be lost. Cancel and copy code edits and important results before leaving. Save generated files separately."
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
})();
