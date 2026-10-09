// Простой лайтбокс + переключение миниатюр + свайп-закрытие для mobile
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

  function openBox(src) {
    if (!box || !boxImg) return;
    boxImg.src = src;
    box.classList.remove("hidden");
    box.classList.add("flex");
  }
  function closeBox() {
    if (!box) return;
    box.classList.add("hidden");
    box.classList.remove("flex");
  }

  if (main && box && boxImg) {
    main.addEventListener("click", () => openBox(main.src));
    box.addEventListener("click", closeBox);
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeBox();
    });
    // Свайп вниз для закрытия на тачскринах
    let startY = null;
    box.addEventListener("touchstart", (e) => {
      if (e.touches.length === 1) startY = e.touches[0].clientY;
    }, {passive: true});
    box.addEventListener("touchend", (e) => {
      if (startY === null) return;
      const endY = e.changedTouches[0].clientY;
      if (endY - startY > 60) closeBox();
      startY = null;
    }, {passive: true});
  }

  // Закрыть бургер-меню после клика по ссылке (mobile <details>)
  document.querySelectorAll("details.md\\:hidden a").forEach((a) => {
    a.addEventListener("click", () => {
      const d = a.closest("details");
      if (d) d.removeAttribute("open");
    });
  });
});
