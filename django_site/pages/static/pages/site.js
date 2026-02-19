(() => {
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  initReveal(prefersReducedMotion);
  initHeaderNavToggle();
  initTilt(prefersReducedMotion);
  initMagnetic();
  initContactModal();
  initWorkflowTabs();
  initMarkdownFlair();
  initPostReadingUi();
})();

function initHeaderNavToggle() {
  const shellTop = document.querySelector(".shell-top");
  const toggle = document.querySelector("[data-nav-toggle]");
  const links = document.querySelector("[data-nav-links]");
  if (!shellTop || !toggle || !links) {
    return;
  }

  const setOpen = (open) => {
    shellTop.classList.toggle("is-nav-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  };

  toggle.addEventListener("click", () => {
    const currentlyOpen = shellTop.classList.contains("is-nav-open");
    setOpen(!currentlyOpen);
  });

  document.addEventListener("click", (event) => {
    if (!shellTop.classList.contains("is-nav-open")) {
      return;
    }
    if (shellTop.contains(event.target)) {
      return;
    }
    setOpen(false);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      setOpen(false);
    }
  });
}

function initReveal(prefersReducedMotion) {
  const targets = Array.from(document.querySelectorAll("[data-reveal]"));
  if (!targets.length) {
    return;
  }

  if (prefersReducedMotion || !("IntersectionObserver" in window)) {
    targets.forEach((el) => el.classList.add("is-visible"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }
        entry.target.classList.add("is-visible");
        obs.unobserve(entry.target);
      });
    },
    { threshold: 0.15, rootMargin: "0px 0px -8% 0px" },
  );

  targets.forEach((target, index) => {
    target.style.transitionDelay = `${Math.min(index * 55, 360)}ms`;
    observer.observe(target);
  });
}

function initTilt(prefersReducedMotion) {
  if (prefersReducedMotion || window.matchMedia("(pointer: coarse)").matches) {
    return;
  }

  const cards = Array.from(document.querySelectorAll(".js-tilt"));
  cards.forEach((card) => {
    const isHeroPanel = card.classList.contains("hero-panel");
    const maxRotateX = isHeroPanel ? 6 : 2.2;
    const maxRotateY = isHeroPanel ? 7 : 2.6;

    let currentRotateX = 0;
    let currentRotateY = 0;
    let targetRotateX = 0;
    let targetRotateY = 0;
    let rafId = 0;
    let isHovering = false;
    const ease = 0.24;

    const render = () => {
      currentRotateX += (targetRotateX - currentRotateX) * ease;
      currentRotateY += (targetRotateY - currentRotateY) * ease;

      card.style.transform =
        `perspective(1000px) rotateX(${currentRotateX.toFixed(2)}deg) rotateY(${currentRotateY.toFixed(2)}deg)`;

      const settled =
        Math.abs(currentRotateX - targetRotateX) < 0.03 &&
        Math.abs(currentRotateY - targetRotateY) < 0.03;

      if (!isHovering && settled) {
        currentRotateX = 0;
        currentRotateY = 0;
        card.style.transform = "";
        rafId = 0;
        return;
      }

      if (isHovering || !settled) {
        rafId = requestAnimationFrame(render);
      } else {
        rafId = 0;
      }
    };

    const ensureLoop = () => {
      if (rafId) {
        return;
      }
      rafId = requestAnimationFrame(render);
    };

    const onMove = (event) => {
      const rect = card.getBoundingClientRect();
      const px = (event.clientX - rect.left) / rect.width;
      const py = (event.clientY - rect.top) / rect.height;

      targetRotateX = (0.5 - py) * maxRotateX;
      targetRotateY = (px - 0.5) * maxRotateY;
      ensureLoop();
    };

    const onEnter = () => {
      isHovering = true;
      ensureLoop();
    };

    const reset = () => {
      isHovering = false;
      targetRotateX = 0;
      targetRotateY = 0;
      ensureLoop();
    };

    card.addEventListener("pointerenter", onEnter);
    card.addEventListener("pointermove", onMove);
    card.addEventListener("pointerleave", reset);
    card.addEventListener("blur", reset);
  });
}

function initMagnetic() {
  const buttons = Array.from(document.querySelectorAll(".js-magnetic"));
  buttons.forEach((button) => {
    const inner = button.querySelector("span");
    if (!inner) {
      return;
    }

    let latestDx = 0;
    let latestDy = 0;
    let framePending = false;

    const render = () => {
      framePending = false;
      inner.style.transform = `translate(${latestDx.toFixed(1)}px, ${latestDy.toFixed(1)}px)`;
    };

    const queueRender = () => {
      if (framePending) {
        return;
      }
      framePending = true;
      requestAnimationFrame(render);
    };

    const onMove = (event) => {
      const rect = button.getBoundingClientRect();
      latestDx = (event.clientX - rect.left - rect.width / 2) * 0.15;
      latestDy = (event.clientY - rect.top - rect.height / 2) * 0.15;
      queueRender();
    };

    const reset = () => {
      inner.style.transform = "translate(0, 0)";
    };

    button.addEventListener("pointermove", onMove);
    button.addEventListener("pointerleave", reset);
  });
}

function initContactModal() {
  const modal = document.querySelector("[data-contact-modal]");
  const openButtons = Array.from(document.querySelectorAll("[data-contact-open]"));
  const closeButtons = Array.from(document.querySelectorAll("[data-contact-close]"));
  if (!modal || !openButtons.length) {
    return;
  }

  let closeTimer = null;
  const closeDurationMs = 280;

  const openModal = () => {
    if (closeTimer) {
      window.clearTimeout(closeTimer);
      closeTimer = null;
    }
    modal.hidden = false;
    document.body.style.overflow = "hidden";
    requestAnimationFrame(() => {
      modal.classList.add("is-open");
      const firstField = modal.querySelector(".contact-input, .contact-textarea");
      if (firstField) {
        firstField.focus();
      }
    });
  };

  const closeModal = () => {
    modal.classList.remove("is-open");
    document.body.style.overflow = "";
    closeTimer = window.setTimeout(() => {
      modal.hidden = true;
      closeTimer = null;
    }, closeDurationMs);
  };

  openButtons.forEach((button) => button.addEventListener("click", openModal));
  closeButtons.forEach((button) => button.addEventListener("click", closeModal));

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !modal.hidden) {
      closeModal();
    }
  });

  if (modal.hasAttribute("data-contact-open-on-load")) {
    openModal();
  }
}

function initWorkflowTabs() {
  const buttons = Array.from(document.querySelectorAll(".workflow-tabs button[data-step]"));
  const panes = Array.from(document.querySelectorAll("[data-step-pane]"));

  if (!buttons.length || !panes.length) {
    return;
  }

  const activate = (step) => {
    buttons.forEach((button) => {
      const active = button.dataset.step === step;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-selected", active ? "true" : "false");
    });

    panes.forEach((pane) => {
      pane.hidden = pane.dataset.stepPane !== step;
    });
  };

  buttons.forEach((button) => {
    button.addEventListener("click", () => activate(button.dataset.step));
  });
}

function initMarkdownFlair() {
  const blocks = Array.from(document.querySelectorAll(".markdown-body"));
  blocks.forEach((block) => {
    const firstParagraph =
      block.querySelector(".post-main-content > p") ||
      block.querySelector(".post-body-content > p") ||
      block.querySelector("p:not(.meta)");
    if (firstParagraph) {
      firstParagraph.classList.add("md-lead");
      const firstChar = (firstParagraph.textContent || "").trim().charAt(0).toUpperCase();
      if (["I", "J", "L", "T"].includes(firstChar)) {
        firstParagraph.classList.add("md-lead--narrow-initial");
      }
    }
  });
}

function initPostReadingUi() {
  const progressBar = document.querySelector(".reading-progress-bar");
  const tocLinks = Array.from(document.querySelectorAll(".post-section-nav a[href^='#']"));
  if (!progressBar && !tocLinks.length) {
    return;
  }

  const findScroller = () => document.querySelector(".scroll-root .simplebar-content-wrapper");
  let scroller = findScroller();
  let boundScroller = null;
  const getScrollTop = () => (scroller ? scroller.scrollTop : window.scrollY || window.pageYOffset || 0);
  const getScrollMax = () => {
    if (scroller) {
      return Math.max(1, scroller.scrollHeight - scroller.clientHeight);
    }
    return Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
  };

  const headingPairs = tocLinks
    .map((link) => {
      const id = link.getAttribute("href")?.slice(1) || "";
      const heading = id ? document.getElementById(id) : null;
      if (!heading) {
        return null;
      }
      return { link, heading };
    })
    .filter(Boolean);

  const update = () => {
    if (progressBar) {
      const ratio = Math.min(1, Math.max(0, getScrollTop() / getScrollMax()));
      progressBar.style.transform = `scaleX(${ratio.toFixed(4)})`;
    }

    if (!headingPairs.length) {
      return;
    }

    const activationLine = 170;
    const currentLine = getScrollTop() + activationLine;
    const scrollerTop = scroller ? scroller.getBoundingClientRect().top : 0;
    let activeLink = headingPairs[0].link;

    headingPairs.forEach(({ link, heading }) => {
      const headingTop = scroller
        ? heading.getBoundingClientRect().top - scrollerTop + getScrollTop()
        : heading.getBoundingClientRect().top + getScrollTop();
      if (headingTop <= currentLine) {
        activeLink = link;
      }
    });

    headingPairs.forEach(({ link }) => {
      const active = link === activeLink;
      link.classList.toggle("is-active", active);
      link.setAttribute("aria-current", active ? "true" : "false");
    });
  };

  const bindScrollTarget = () => {
    scroller = findScroller();
    if (scroller && scroller !== boundScroller) {
      if (boundScroller) {
        boundScroller.removeEventListener("scroll", update);
      }
      scroller.addEventListener("scroll", update, { passive: true });
      boundScroller = scroller;
    }
  };

  bindScrollTarget();
  window.addEventListener("resize", update, { passive: true });
  window.addEventListener("scroll", update, { passive: true });
  setTimeout(bindScrollTarget, 120);
  setTimeout(bindScrollTarget, 500);
  setTimeout(bindScrollTarget, 1200);
  update();
}
