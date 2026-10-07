// Простой лайтбокс + переключение миниатюр
document.addEventListener("DOMContentLoaded", () => {
  const main = document.getElementById("main-image");
  const box = document.getElementById("lightbox");
  const boxImg = document.getElementById("lightbox-img");

  document.querySelectorAll(".thumb").forEach((t) => {
    t.addEventListener("click", () => {
      if (main) main.src = t.dataset.full;
      document.querySelectorAll(".thumb").forEach((x) => x.classList.remove("selected"));
      t.classList.add("selected");
    });
  });

  if (main && box && boxImg) {
    main.addEventListener("click", () => {
      boxImg.src = main.src;
      box.classList.remove("hidden");
      box.classList.add("flex");
    });
    box.addEventListener("click", () => {
      box.classList.add("hidden");
      box.classList.remove("flex");
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        box.classList.add("hidden");
        box.classList.remove("flex");
      }
    });
  }
});
