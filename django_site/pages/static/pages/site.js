(() => {
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  initReveal(prefersReducedMotion);
  initTilt(prefersReducedMotion);
  initMagnetic();
  initWorkflowTabs();
  initMarkdownFlair();
})();

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
    const firstParagraph = block.querySelector("p");
    if (firstParagraph) {
      firstParagraph.classList.add("md-lead");
    }
  });
}
