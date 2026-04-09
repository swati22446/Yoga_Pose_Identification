/* ══════════════════════════════════════════════════════════════════════════════
   main.js — YogaLens
   Handles: navbar scroll-spy · hamburger · image drop zone · upload form
══════════════════════════════════════════════════════════════════════════════ */

document.addEventListener("DOMContentLoaded", () => {
  /* ── Navbar: scroll-spy active link ───────────────────────────────────────── */
  const navLinks = document.querySelectorAll(".nav-link");
  const sections = document.querySelectorAll("section[id]");

  function updateActiveLink() {
    let current = "";
    sections.forEach((s) => {
      if (window.scrollY >= s.offsetTop - 90) current = s.id;
    });
    navLinks.forEach((a) => {
      a.classList.remove("active");
      if (
        a.getAttribute("href") === "#" + current ||
        a.getAttribute("href") === "/#" + current
      ) {
        a.classList.add("active");
      }
    });
  }

  window.addEventListener("scroll", updateActiveLink, { passive: true });
  updateActiveLink();

  /* ── Navbar: hamburger toggle (mobile) ────────────────────────────────────── */
  const hamburger = document.getElementById("nav-hamburger");
  const navList = document.getElementById("nav-links");

  if (hamburger && navList) {
    hamburger.addEventListener("click", () => {
      navList.classList.toggle("open");
    });
    // Close on link click
    navList.querySelectorAll("a").forEach((a) => {
      a.addEventListener("click", () => navList.classList.remove("open"));
    });
  }

  /* ── Model cards: touch/click toggle on mobile ────────────────────────────── */
  document.querySelectorAll(".model-card").forEach((card) => {
    card.addEventListener("click", () => {
      // Toggle an 'active' class so mobile users can see the back
      card.classList.toggle("flipped");
    });
  });

  /* ── Contact form ─────────────────────────────────────────────────────────── */
  const contactForm = document.getElementById("contact-form");
  const formSuccess = document.getElementById("form-success");

  if (contactForm) {
    contactForm.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!contactForm.checkValidity()) {
        contactForm.reportValidity();
        return;
      }
      if (formSuccess) {
        formSuccess.hidden = false;
        contactForm.reset();
        setTimeout(() => {
          formSuccess.hidden = true;
        }, 5000);
      }
    });
  }

  /* ── Image upload: drop zone ─────────────────────────────────────────────── */
  const fileInput = document.getElementById("file-input");
  if (!fileInput) return; // Not on a page with the upload form

  const dropZone = document.getElementById("drop-zone");
  const previewWrap = document.getElementById("preview-wrap");
  const previewImg = document.getElementById("preview-img");
  const previewName = document.getElementById("preview-name");
  const btnSubmit = document.getElementById("btn-submit");
  const uploadForm = document.getElementById("upload-form");

  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("drag-over");
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("drag-over");
  });

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("drag-over");
    const file = e.dataTransfer.files[0];
    if (file) applyFile(file);
  });

  fileInput.addEventListener("change", () => {
    if (fileInput.files[0]) applyFile(fileInput.files[0]);
  });

  function applyFile(file) {
    const dt = new DataTransfer();
    dt.items.add(file);
    fileInput.files = dt.files;

    const reader = new FileReader();
    reader.onload = (ev) => {
      previewImg.src = ev.target.result;
      previewWrap.hidden = false;
      previewName.textContent = file.name;
    };
    reader.readAsDataURL(file);

    if (btnSubmit) btnSubmit.disabled = false;
  }

  if (uploadForm) {
    uploadForm.addEventListener("submit", () => {
      if (btnSubmit) {
        btnSubmit.disabled = true;
        btnSubmit.textContent = "Analysing…";
      }
    });
  }
});
