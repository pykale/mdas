/* Book Theme hides the inherited navbar, but both themes bind only the first
 * .primary-toggle. Run deferred, before their DOMContentLoaded handlers, so
 * they bind the visible article button and retain their native toggle logic. */
(() => {
  "use strict";
  document.querySelector("#pst-header .primary-toggle")?.classList.remove("primary-toggle");

  const button = document.querySelector(".primary-toggle");
  const sidebar = document.getElementById("pst-primary-sidebar");
  const dialog = document.getElementById("pst-primary-sidebar-modal");
  if (!button || !sidebar || !dialog) return;

  const desktop = window.matchMedia("(min-width: 992px)");
  const syncState = () => {
    button.setAttribute("aria-controls", desktop.matches ? sidebar.id : dialog.id);
    button.setAttribute("aria-expanded", String(desktop.matches
      ? !sidebar.classList.contains("pst-sidebar-hidden") : dialog.open));
  };
  // Observe the theme's state, including Escape/backdrop dismissal on mobile.
  const observer = new MutationObserver(syncState);
  observer.observe(sidebar, {attributes: true, attributeFilter: ["class"]});
  observer.observe(dialog, {attributes: true, attributeFilter: ["open"]});
  dialog.addEventListener("close", () => button.focus());
  desktop.addEventListener("change", syncState);
  syncState();
})();
