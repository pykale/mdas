/* Protect active kernels on all notebook links, reloads and tab closes. */
(() => {
  "use strict";
  window.addEventListener("beforeunload", (event) => {
    if (window.mdasSessionStarted) {
      event.preventDefault();
      event.returnValue = "";
    }
  });
})();
