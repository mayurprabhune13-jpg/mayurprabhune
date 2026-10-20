(() => {
  const body = document.body;
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const menuButton = document.querySelector("#menu-toggle");
  const mobileNav = document.querySelector("#mobile-navigation");
  if (mobileNav) mobileNav.inert = true;
  const closeMenu = () => {
    if (!menuButton || !mobileNav) return;
    menuButton.setAttribute("aria-expanded", "false");
    menuButton.setAttribute("aria-label", "Open navigation");
    mobileNav.classList.remove("is-open");
    mobileNav.inert = true;
  };
  if (menuButton && mobileNav) {
    menuButton.addEventListener("click", () => {
      const opening = menuButton.getAttribute("aria-expanded") !== "true";
      menuButton.setAttribute("aria-expanded", String(opening));
      menuButton.setAttribute("aria-label", opening ? "Close navigation" : "Open navigation");
      mobileNav.classList.toggle("is-open", opening);
      mobileNav.inert = !opening;
    });
    mobileNav.addEventListener("click", (event) => {
      if (event.target.closest("a")) closeMenu();
    });
    document.addEventListener("click", (event) => {
      if (!event.target.closest(".site-header")) closeMenu();
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        closeMenu();
        menuButton.focus();
      }
    });
  }

  const tabs = Array.from(document.querySelectorAll("[data-expertise-tab]"));
  const panels = Array.from(document.querySelectorAll("[data-expertise-panel]"));
  const activateTab = (tab, moveFocus = false) => {
    const key = tab.dataset.expertiseTab;
    tabs.forEach((item) => {
      const selected = item === tab;
      item.setAttribute("aria-selected", String(selected));
      item.tabIndex = selected ? 0 : -1;
    });
    panels.forEach((panel) => {
      panel.hidden = panel.dataset.expertisePanel !== key;
    });
    if (moveFocus) tab.focus();
  };
  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => activateTab(tab));
    tab.addEventListener("keydown", (event) => {
      let next = index;
      if (event.key === "ArrowRight" || event.key === "ArrowDown") next = (index + 1) % tabs.length;
      else if (event.key === "ArrowLeft" || event.key === "ArrowUp") next = (index - 1 + tabs.length) % tabs.length;
      else if (event.key === "Home") next = 0;
      else if (event.key === "End") next = tabs.length - 1;
      else return;
      event.preventDefault();
      activateTab(tabs[next], true);
    });
  });
  if (tabs.length && panels.length) {
    const initial = tabs.find((tab) => tab.getAttribute("aria-selected") === "true") || tabs[0];
    activateTab(initial);
  }

  const sections = Array.from(document.querySelectorAll("[data-nav-section]"));
  const activeLinks = Array.from(document.querySelectorAll("[data-section-link]"));
  if (sections.length && "IntersectionObserver" in window) {
    const sectionObserver = new IntersectionObserver((entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (!visible) return;
      activeLinks.forEach((link) => {
        if (link.hash === `#${visible.target.id}`) link.setAttribute("aria-current", "location");
        else link.removeAttribute("aria-current");
      });
    }, { rootMargin: "-22% 0px -58% 0px", threshold: [0, .15, .4] });
    sections.forEach((section) => sectionObserver.observe(section));
  }

  if (!reduceMotion && "IntersectionObserver" in window) {
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -48px 0px", threshold: .08 });
    document.querySelectorAll(".reveal").forEach((item, index) => {
      item.style.setProperty("--reveal-delay", `${Math.min(index % 4, 3) * 65}ms`);
      item.classList.add("reveal-ready");
      revealObserver.observe(item);
    });
    document.documentElement.classList.add("motion-ready");
  } else {
    document.querySelectorAll(".reveal").forEach((item) => item.classList.add("is-visible"));
  }

  const canHover = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  if (canHover && !reduceMotion) {
    document.querySelectorAll("[data-magnetic]").forEach((button) => {
      let frame = 0;
      button.addEventListener("pointermove", (event) => {
        const rect = button.getBoundingClientRect();
        const x = (event.clientX - rect.left - rect.width / 2) / rect.width;
        const y = (event.clientY - rect.top - rect.height / 2) / rect.height;
        cancelAnimationFrame(frame);
        frame = requestAnimationFrame(() => {
          button.style.transform = `translate(${x * 4}px, ${y * 3}px)`;
        });
      });
      button.addEventListener("pointerleave", () => {
        cancelAnimationFrame(frame);
        button.style.transform = "";
      });
    });

    document.querySelectorAll("[data-tilt]").forEach((card) => {
      let frame = 0;
      card.addEventListener("pointermove", (event) => {
        const rect = card.getBoundingClientRect();
        const x = (event.clientX - rect.left) / rect.width - .5;
        const y = (event.clientY - rect.top) / rect.height - .5;
        cancelAnimationFrame(frame);
        frame = requestAnimationFrame(() => {
          card.style.transform = `perspective(900px) rotateX(${y * -2.2}deg) rotateY(${x * 2.2}deg) translateY(-3px)`;
        });
      });
      card.addEventListener("pointerleave", () => {
        cancelAnimationFrame(frame);
        card.style.transform = "";
      });
    });
  }

  document.addEventListener("visibilitychange", () => {
    body.classList.toggle("is-hidden", document.hidden);
  });

  document.querySelectorAll(".contact-form").forEach((form) => {
    form.addEventListener("submit", () => {
      const button = form.querySelector("button[type='submit']");
      const status = form.querySelector("[data-form-status]");
      if (button) {
        button.disabled = true;
        button.dataset.originalLabel = button.textContent.trim();
        button.textContent = "Sending…";
      }
      if (status) status.textContent = "Sending your message securely…";
    });
  });
})();
