// web/static/script.js
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("analyze-form");
  const urlInput = document.getElementById("url-input");

  const resultSection = document.getElementById("result-section");
  const badge = document.getElementById("status-badge");
  const inputUrlEl = document.getElementById("result-input-url");
  const normalizedUrlEl = document.getElementById("result-normalized-url");
  const hostEl = document.getElementById("result-host");
  const indicatorsEl = document.getElementById("result-indicators");
  const reasonsEl = document.getElementById("result-reasons");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const url = urlInput.value.trim();
    if (!url) return;

    try {
      const response = await fetch("/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        alert("Erro ao analisar a URL.");
        return;
      }

      const data = await response.json();
      updateResult(data);
    } catch (err) {
      console.error(err);
      alert("Erro de conexão com o servidor.");
    }
  });

  function updateResult(data) {
    resultSection.classList.remove("hidden");

    inputUrlEl.textContent = data.input_url || "-";
    normalizedUrlEl.textContent = data.parsed?.normalized || "-";
    hostEl.textContent = data.parsed?.host || "-";

    // Status badge
    badge.textContent = data.status || "-";
    badge.className = "badge";
    if (data.status === "safe") {
      badge.classList.add("badge-safe");
    } else if (data.status === "suspicious") {
      badge.classList.add("badge-suspicious");
    } else if (data.status === "malicious") {
      badge.classList.add("badge-malicious");
    }

    // Indicadores
    const indicators = data.indicators || {};
    const indTexts = [];
    if (indicators.number_letter_substitution) {
      indTexts.push("Substituição de letras por números.");
    }
    if (indicators.many_subdomains) {
      indTexts.push("Uso excessivo de subdomínios.");
    }
    if (indicators.special_chars) {
      indTexts.push("Caracteres especiais suspeitos na URL.");
    }

    indicatorsEl.textContent =
      indTexts.length > 0 ? indTexts.join(" ") : "Nenhum indicador suspeito detectado.";

    // Motivos
    const reasons = data.reasons || [];
    reasonsEl.textContent =
      reasons.length > 0
        ? reasons.join(" ")
        : "Nenhuma razão suspeita adicional identificada.";
  }
});
