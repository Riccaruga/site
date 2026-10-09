// Копирование email в буфер обмена (clipboard + fallback), фидбек только иконкой
document.addEventListener("DOMContentLoaded", () => {
  const btn = document.querySelector("[data-copy-email]");
  if (!btn) return;
  const iconCopy = btn.querySelector("[data-icon-copy]");
  const iconCheck = btn.querySelector("[data-icon-check]");

  function showCopy() {
    if (iconCopy) iconCopy.classList.remove("hidden");
    if (iconCheck) iconCheck.classList.add("hidden");
    btn.setAttribute("aria-label", "Скопировать адрес почты");
  }
  function showCheck() {
    if (iconCopy) iconCopy.classList.add("hidden");
    if (iconCheck) iconCheck.classList.remove("hidden");
    btn.setAttribute("aria-label", "Адрес скопирован");
  }

  async function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return;
    }
    // Fallback для HTTP / старых браузеров
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "absolute";
    ta.style.left = "-9999px";
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    document.body.removeChild(ta);
  }

  btn.addEventListener("click", async () => {
    const text = btn.getAttribute("data-copy-email") || "";
    if (!text) return;
    try {
      await copyText(text);
      showCheck();
    } catch (e) {
      // тихо: оставляем иконку копирования
      showCopy();
    }
    setTimeout(showCopy, 2000);
  });
});
