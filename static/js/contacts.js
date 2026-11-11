// Копирование email, счётчик символов, отправка формы и валидация
document.addEventListener("DOMContentLoaded", () => {
  initCopyEmail();
  initMessageCounter();
  initAjaxSubmit();
});

// Фокус на ошибках — после полной загрузки, чтобы браузер не сбросил его
if (document.readyState === "complete") {
  focusFormErrors();
} else {
  window.addEventListener("load", focusFormErrors);
}

function initCopyEmail() {
  const triggers = document.querySelectorAll("[data-copy-email]");
  if (!triggers.length) return;

  triggers.forEach((trigger) => {
    const row = trigger.closest(".contact-row");
    if (!row) return;
    const btn = row.querySelector("button[data-copy-email]");
    const iconCopy = btn.querySelector("[data-icon-copy]");
    const iconCheck = btn.querySelector("[data-icon-check]");
    const status = row.querySelector("[data-copy-status]");
    let resetTimer;

    function showCopy() {
      if (iconCopy) iconCopy.classList.remove("hidden");
      if (iconCheck) iconCheck.classList.add("hidden");
      trigger.setAttribute("aria-label", "Скопировать адрес почты");
      if (status) {
        status.classList.add("hidden");
        status.textContent = "";
      }
    }
    function showCheck() {
      if (iconCopy) iconCopy.classList.add("hidden");
      if (iconCheck) iconCheck.classList.remove("hidden");
      trigger.setAttribute("aria-label", "Адрес скопирован");
      if (status) {
        status.textContent = "Адрес скопирован";
        status.classList.remove("hidden");
      }
    }

    async function copyText(text) {
      if (navigator.clipboard && window.isSecureContext) {
        try {
          await navigator.clipboard.writeText(text);
          return;
        } catch (e) {
          // нет разрешения — пробуем legacy-способ ниже
        }
      }
      const ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.position = "absolute";
      ta.style.left = "-9999px";
      document.body.appendChild(ta);
      ta.select();
      const copied = document.execCommand("copy");
      document.body.removeChild(ta);
      if (!copied) throw new Error("copy failed");
    }

    trigger.addEventListener("click", async (e) => {
      if (trigger.tagName === "A") e.preventDefault();
      const text = trigger.getAttribute("data-copy-email") || "";
      if (!text) return;
      try {
        await copyText(text);
        showCheck();
      } catch (err) {
        showCopy();
      }
      clearTimeout(resetTimer);
      resetTimer = setTimeout(showCopy, 2000);
    });
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
      counter.classList.toggle("text-alert", length >= max);
      counter.classList.toggle("text-ink-mute", length < max);
    }
    resize();
  }

  message.addEventListener("input", update);
  update();
}

function initAjaxSubmit() {
  const form = document.getElementById("contact-form");
  if (!form) return;

  const btn = form.querySelector("[data-submit]");
  const label = btn.querySelector("[data-submit-label]");
  const spinner = btn.querySelector("[data-spinner]");
  const successPanel = document.getElementById("contact-success");
  const errorsBox = document.getElementById("form-errors");

  function clearFieldErrors() {
    form.querySelectorAll("[data-field-error]").forEach((el) => {
      el.textContent = "";
      el.classList.add("hidden");
    });
    form.querySelectorAll('[aria-invalid="true"]').forEach((el) => {
      el.removeAttribute("aria-invalid");
    });
    form.querySelectorAll(".border-alert").forEach((el) => {
      el.classList.remove("border-alert");
    });
    if (errorsBox) errorsBox.classList.add("hidden");
  }

  function showFieldError(fieldId, message) {
    const el = document.getElementById(`${fieldId}-error`);
    const input = document.getElementById(fieldId);
    if (el) {
      el.textContent = message;
      el.classList.remove("hidden");
    }
    if (input) {
      input.setAttribute("aria-invalid", "true");
      input.classList.add("border-alert");
    }
  }

  function showGeneralError(message) {
    if (errorsBox) {
      errorsBox.classList.remove("hidden");
      const list = errorsBox.querySelector("ul");
      if (list) list.innerHTML = `<li>${message}</li>`;
      errorsBox.focus();
    }
  }

  function setLoading(loading) {
    btn.disabled = loading;
    if (loading) {
      btn.setAttribute("aria-busy", "true");
    } else {
      btn.removeAttribute("aria-busy");
    }
    if (label) label.textContent = loading ? "Отправляем…" : "Отправить сообщение";
    if (spinner) spinner.classList.toggle("hidden", !loading);
  }

  function showSuccess() {
    setLoading(false);
    if (successPanel) {
      successPanel.classList.remove("hidden");
      successPanel.focus();
    }
  }

  function resetFormState() {
    setLoading(false);
    if (successPanel) successPanel.classList.add("hidden");
  }

  // «Написать ещё»: просто скрываем подтверждение и возвращаемся к полям
  if (successPanel) {
    const again = successPanel.querySelector("a");
    if (again) {
      again.addEventListener("click", (e) => {
        e.preventDefault();
        successPanel.classList.add("hidden");
        const nameField = form.querySelector("#id_name");
        if (nameField) nameField.focus();
      });
    }
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    clearFieldErrors();

    const name = document.getElementById("id_name");
    const email = document.getElementById("id_email");
    const message = document.getElementById("id_message");

    let invalid = false;

    if (!name || !name.value.trim()) {
      showFieldError("id_name", "Укажите, пожалуйста, ваше имя.");
      invalid = true;
    }
    if (!email || !email.value.trim()) {
      showFieldError("id_email", "Укажите email для ответа.");
      invalid = true;
    } else if (email.validity && email.validity.typeMismatch) {
      showFieldError("id_email", "Проверьте правильность адреса электронной почты.");
      invalid = true;
    }
    if (!message || !message.value.trim()) {
      showFieldError("id_message", "Напишите, пожалуйста, ваше сообщение.");
      invalid = true;
    }

    if (invalid) {
      showGeneralError("Проверьте выделенные поля");
      const firstInvalid = form.querySelector('[aria-invalid="true"]');
      if (firstInvalid) firstInvalid.focus();
      return;
    }

    const formData = new FormData(form);
    setLoading(true);

    try {
      const res = await fetch(form.action, {
        method: "POST",
        body: formData,
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          Accept: "application/json",
        },
        credentials: "same-origin",
      });

      if (res.ok) {
        const data = await res.json();
        if (data.ok) {
          showSuccess();
          form.reset();
          const counter = document.querySelector("[data-counter]");
          if (counter) counter.textContent = "0 / 2000";
          if (message) {
            message.style.height = "auto";
          }
          return;
        }
      }

      const data = await res.json();
      const errors = data.errors || {};
      let firstField = null;
      for (const [field, list] of Object.entries(errors)) {
        const input = document.getElementById(field);
        if (input && Array.isArray(list) && list.length) {
          showFieldError(field, list[0].message);
          if (!firstField) firstField = input;
        }
      }
      if (Object.keys(errors).length && !firstField) {
        showGeneralError("Проверьте выделенные поля");
      } else if (firstField) {
        firstField.focus();
      } else {
        showGeneralError("Не удалось отправить сообщение. Попробуйте ещё раз.");
      }
    } catch (err) {
      showGeneralError("Не удалось отправить сообщение. Попробуйте ещё раз.");
    } finally {
      setLoading(false);
    }
  });

  // При возврате по кнопке «назад» сбрасываем состояние
  window.addEventListener("pageshow", () => {
    resetFormState();
  });
}

function focusFormErrors() {
  const box = document.getElementById("form-errors");
  if (box) box.focus();
}
