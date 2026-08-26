(function () {
  const header = document.querySelector(".site-header");
  const brandLogo = document.querySelector(".brand-logo");
  const navToggle = document.querySelector(".nav-toggle");
  const siteNav = document.querySelector(".site-nav");
  const form = document.getElementById("contact-form");
  const formNote = document.getElementById("form-note");
  const yearEl = document.getElementById("year");

  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  function updateHeader() {
    if (!header) return;
    const scrolled = window.scrollY > 40;
    header.classList.toggle("scrolled", scrolled);

    if (brandLogo && brandLogo.dataset.logoDark && brandLogo.dataset.logoLight) {
      brandLogo.src = scrolled ? brandLogo.dataset.logoDark : brandLogo.dataset.logoLight;
    }
  }

  window.addEventListener("scroll", updateHeader, { passive: true });
  updateHeader();

  if (navToggle && siteNav) {
    navToggle.addEventListener("click", () => {
      const open = navToggle.getAttribute("aria-expanded") === "true";
      navToggle.setAttribute("aria-expanded", String(!open));
      navToggle.setAttribute("aria-label", open ? "Open menu" : "Close menu");
      siteNav.classList.toggle("open", !open);
    });

    siteNav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        navToggle.setAttribute("aria-expanded", "false");
        navToggle.setAttribute("aria-label", "Open menu");
        siteNav.classList.remove("open");
      });
    });
  }

  if (form) {
    const formError = document.getElementById("form-error");
    const submitBtn = document.getElementById("form-submit-btn");
    const formEndpoint = form.getAttribute("action");

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (!formEndpoint) return;

      if (formNote) formNote.hidden = true;
      if (formError) formError.hidden = true;

      const originalLabel = submitBtn?.textContent;
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = "Sending…";
      }

      const payload = Object.fromEntries(new FormData(form).entries());

      try {
        const res = await fetch(formEndpoint, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          body: JSON.stringify(payload),
        });

        if (!res.ok) throw new Error("Form submit failed");

        if (formNote) formNote.hidden = false;
        form.reset();
      } catch {
        if (formError) formError.hidden = false;
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = originalLabel || "Submit enquiry";
        }
        submitBtn?.blur();
      }
    });
  }

  /* Carousel */
  const carousel = document.querySelector("[data-carousel]");
  if (carousel) {
    const slides = carousel.querySelectorAll(".carousel-slide");
    const dots = carousel.querySelectorAll("[data-carousel-dot]");
    const prevBtn = carousel.querySelector("[data-carousel-prev]");
    const nextBtn = carousel.querySelector("[data-carousel-next]");
    let index = 0;
    let timer;
    const interval = 6000;

    function goTo(i) {
      index = (i + slides.length) % slides.length;
      slides.forEach((slide, n) => {
        slide.classList.toggle("is-active", n === index);
      });
      dots.forEach((dot, n) => {
        dot.setAttribute("aria-selected", n === index ? "true" : "false");
      });
    }

    function next() {
      goTo(index + 1);
    }

    function startAutoplay() {
      stopAutoplay();
      timer = setInterval(next, interval);
    }

    function stopAutoplay() {
      if (timer) clearInterval(timer);
    }

    prevBtn?.addEventListener("click", () => {
      goTo(index - 1);
      startAutoplay();
    });

    nextBtn?.addEventListener("click", () => {
      next();
      startAutoplay();
    });

    dots.forEach((dot) => {
      dot.addEventListener("click", () => {
        goTo(Number(dot.dataset.carouselDot));
        startAutoplay();
      });
    });

    carousel.addEventListener("mouseenter", stopAutoplay);
    carousel.addEventListener("mouseleave", startAutoplay);
    carousel.addEventListener("focusin", stopAutoplay);
    carousel.addEventListener("focusout", startAutoplay);

    startAutoplay();
  }

  /* Scroll reveal */
  const revealEls = document.querySelectorAll(".reveal, .service-card, .approach-card, .blog-card, .faq-item");
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -48px 0px" }
  );

  revealEls.forEach((el) => revealObserver.observe(el));

  /* FAQ (rendered from content/faq.json, editable via the /admin CMS) */
  const faqList = document.getElementById("faq-list");
  if (faqList) {
    const escapeHtml = (text) =>
      String(text || "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");

    // Renders the small Markdown subset the CMS's answer field allows:
    // **bold**, *italic*, and [label](url) links. Mirrors inline_markdown()
    // in scripts/generate-blog.py.
    const renderInlineMarkdown = (text) => {
      let out = escapeHtml(text);
      out = out.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
      out = out.replace(/(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)/g, "<em>$1</em>");
      out = out.replace(/(?<!\w)_(.+?)_(?!\w)/g, "<em>$1</em>");
      out = out.replace(/\[(.+?)\]\((.+?)\)/g, (_m, label, url) => `<a href="${escapeHtml(url)}">${label}</a>`);
      return out;
    };
    const stripMarkdown = (text) => String(text || "").replace(/[*_]/g, "").replace(/\[(.+?)\]\(.+?\)/g, "$1");

    fetch("content/faq.json")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to load FAQ data");
        return res.json();
      })
      .then((data) => {
        const items = data && data.items;
        if (!Array.isArray(items) || !items.length) return;

        faqList.innerHTML = items
          .map(
            (item) => `
          <details class="faq-item">
            <summary class="faq-question">${escapeHtml(item.question)}</summary>
            <div class="faq-answer">
              <p>${renderInlineMarkdown(item.answer)}</p>
            </div>
          </details>`
          )
          .join("");

        faqList.querySelectorAll(".faq-item").forEach((el) => revealObserver.observe(el));

        const faqSchema = {
          "@context": "https://schema.org",
          "@type": "FAQPage",
          "@id": "https://quadiqadvisory.com/#faq",
          mainEntity: items.map((item) => ({
            "@type": "Question",
            name: item.question,
            acceptedAnswer: {
              "@type": "Answer",
              text: stripMarkdown(item.answer),
            },
          })),
        };

        const schemaScript = document.createElement("script");
        schemaScript.type = "application/ld+json";
        schemaScript.textContent = JSON.stringify(faqSchema);
        document.head.appendChild(schemaScript);
      })
      .catch(() => {
        /* leave the section empty if content/faq.json fails to load */
      });
  }
})();
