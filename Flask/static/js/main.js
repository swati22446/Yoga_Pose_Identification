/* ══════════════════════════════════════════════════════════════════════════════
   main.js — Input page: drag-and-drop, preview, submit handling
   Output page is fully server-rendered by Jinja2, no JS needed there.
══════════════════════════════════════════════════════════════════════════════ */

document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("file-input");
  if (!fileInput) return; // Not on input page — exit early

  const dropZone = document.getElementById("drop-zone");
  const previewWrap = document.getElementById("preview-wrap");
  const previewImg = document.getElementById("preview-img");
  const previewName = document.getElementById("preview-name");
  const btnSubmit = document.getElementById("btn-submit");
  const form = document.getElementById("upload-form");

  /* ── Drag events ── */
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

  /* ── File input change ── */
  fileInput.addEventListener("change", () => {
    if (fileInput.files[0]) applyFile(fileInput.files[0]);
  });

  /* ── Apply file: show preview, enable submit ── */
  function applyFile(file) {
    // Transfer to input element (required after drag-drop)
    const dt = new DataTransfer();
    dt.items.add(file);
    fileInput.files = dt.files;

    // Preview
    const reader = new FileReader();
    reader.onload = (ev) => {
      previewImg.src = ev.target.result;
      previewWrap.hidden = false;
      previewName.textContent = file.name;
    };
    reader.readAsDataURL(file);

    btnSubmit.disabled = false;
  }

  /* ── Loading state on submit ── */
  form.addEventListener("submit", () => {
    btnSubmit.disabled = true;
    btnSubmit.textContent = "Analysing…";
  });
});
