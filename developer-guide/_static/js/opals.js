(function() {
  // Only execute script if page is iframed
  if (window.self === window.top) {
    return;
  }

  // Force OPALS?
  const opalsOn = new URLSearchParams(window.location.search).get("opals");
  if (!opalsOn) {
    return;
  }

  const styleElement = document.createElement("style");
  styleElement.textContent = `
    .headnav, .mobile-header, .sidebar-drawer {
      display: none !important;
    }
    .main {
      padding-top: 0 !important;
    }
    .content {
      margin: 0 auto !important;
    }
  `;
  document.head.appendChild(styleElement);

  window.addEventListener("load", function() {
    const imageExt = [".png", ".jpg", ".gif"];

    Array.from(document.getElementsByTagName("a")).forEach((element) => {
      if (
        !element.href.startsWith(window.origin) ||
        imageExt.some((ext) => element.href.endsWith(ext))
      ) {
        // External links & images open in a new tab
        element.target = "_blank";
      } else {
        // Internal links that are not images have ?opals=true
        const anchorUrl = new URL(element.href);
        anchorUrl.searchParams.set("opals", true);
        element.href = anchorUrl.toString();
      }
    });

    if (typeof jQuery === "function") {
      const url = new URL(window.location);
      url.searchParams.delete("opals");
      jQuery("article[role='main'] h1:first a.headerlink").before(`
        <a href="${url.href}" target="_blank" class="open-new-tab">
          <i class="fa fa-external-link"></i>
          <span class="sr-only">Open page in a new tab</span>
        </a>
      `);
    }
  });
})();
