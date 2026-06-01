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
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (formNote) formNote.hidden = false;
      form.reset();
      form.querySelector("button[type=submit]")?.blur();
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
  const revealEls = document.querySelectorAll(".reveal, .service-card, .approach-card");
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
})();
