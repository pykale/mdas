(() => {
  "use strict";
  const doc = document;
  const button = doc.createElement("button");
  button.type = "button";
  button.id = "mdas-presentation-toggle";
  button.className = "btn btn-sm mdas-presentation-toggle";
  button.innerHTML = '<span aria-hidden="true">⛶</span><span class="mdas-presentation-label"> Present</span>';
  let active = false;
  let ownFullscreen = false;
  let scrollPosition = 0;
  const update = (enabled) => {
    active = enabled;
    doc.documentElement.classList.toggle("mdas-presentation", enabled);
    const label = enabled ? "Exit presentation mode" : "Enter presentation mode";
    button.setAttribute("aria-label", label);
    button.setAttribute("title", label);
    button.setAttribute("aria-pressed", String(enabled));
  };
  const restoreScroll = () => requestAnimationFrame(() => window.scrollTo(0, scrollPosition));
  const exit = async () => {
    update(false);
    if (ownFullscreen && doc.fullscreenElement && doc.exitFullscreen) {
      try { await doc.exitFullscreen(); } catch (_) { /* Layout still restores. */ }
    }
    ownFullscreen = false;
    restoreScroll();
  };
  button.addEventListener("click", async () => {
    if (active) { await exit(); return; }
    scrollPosition = window.scrollY;
    update(true);
    if (!doc.fullscreenElement && doc.documentElement.requestFullscreen) {
      try {
        await doc.documentElement.requestFullscreen();
        ownFullscreen = true;
        if (!active) await exit();
      } catch (_) { /* Keep the expanded layout when fullscreen is unavailable. */ }
    }
    restoreScroll();
  });
  doc.addEventListener("fullscreenchange", () => {
    if (!doc.fullscreenElement && active && ownFullscreen) {
      ownFullscreen = false;
      update(false);
      restoreScroll();
    }
  });
  doc.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && active) { event.preventDefault(); void exit(); }
  });
  update(false);
  const mount = () => {
    const header = doc.querySelector(".article-header-buttons");
    if (header && !doc.getElementById(button.id)) header.prepend(button);
  };
  if (doc.readyState === "loading") doc.addEventListener("DOMContentLoaded", mount, {once: true});
  else mount();
})();
