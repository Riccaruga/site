// Копирование email, счётчик символов и состояние отправки формы
document.addEventListener("DOMContentLoaded", () => {
  initCopyEmail();
  initMessageCounter();
  initSubmitState();
});

// Фокус на ошибках — после полной загрузки, чтобы браузер не сбросил его
if (document.readyState === "complete") {
  focusFormErrors();
} else {
  window.addEventListener("load", focusFormErrors);
}

function initCopyEmail() {
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
}

function initMessageCounter() {
  const message = document.getElementById("id_message");
  const counter = document.querySelector("[data-counter]");
  if (!message) return;

  const max = Number(message.getAttribute("maxlength")) || 2000;

  function resize() {
    message.style.height = "auto";
    const height = Math.min(message.scrollHeight, 480);
    message.style.height = `${height}px`;
    message.style.overflowY = message.scrollHeight > 480 ? "auto" : "hidden";
  }

  function update() {
    if (counter) {
      const length = message.value.length;
      counter.textContent = `${length} / ${max}`;
      counter.classList.toggle("text-red-600", length >= max);
      counter.classList.toggle("text-stone-400", length < max);
    }
    resize();
  }

  message.addEventListener("input", update);
  update();
}

function initSubmitState() {
  const form = document.getElementById("contact-form");
  if (!form) return;

  const btn = form.querySelector("[data-submit]");
  if (!btn) return;

  const label = btn.querySelector("[data-submit-label]");
  const spinner = btn.querySelector("[data-spinner]");

  function setLoading(loading) {
    btn.disabled = loading;
    if (loading) {
      btn.setAttribute("aria-busy", "true");
    } else {
      btn.removeAttribute("aria-busy");
    }
    if (label) label.textContent = loading ? "Отправка…" : "Отправить сообщение";
    if (spinner) spinner.classList.toggle("hidden", !loading);
  }

  form.addEventListener("submit", () => setLoading(true));

  // При возврате по кнопке «назад» из кэша сбрасываем состояние
  window.addEventListener("pageshow", () => setLoading(false));
}

function focusFormErrors() {
  const box = document.getElementById("form-errors");
  if (box) box.focus();
}
