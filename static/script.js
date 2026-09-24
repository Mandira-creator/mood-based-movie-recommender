const emotionGrid = document.getElementById("emotionGrid");
const textForm = document.getElementById("textForm");
const textInput = document.getElementById("textInput");
const resultArea = document.getElementById("resultArea");

let emotions = [];

async function loadEmotions() {
  const res = await fetch("/api/emotions");
  const data = await res.json();
  emotions = data.emotions;

  emotionGrid.innerHTML = emotions.map(e => `
    <button class="emotion-btn" data-key="${e.key}">
      <span class="e">${e.emoji}</span>
      <span>${e.label}</span>
    </button>
  `).join("");

  emotionGrid.querySelectorAll(".emotion-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      emotionGrid.querySelectorAll(".emotion-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      textInput.value = "";
      recommend({ emotion: btn.dataset.key });
    });
  });
}

textForm.addEventListener("submit", (ev) => {
  ev.preventDefault();
  const text = textInput.value.trim();
  if (!text) return;
  emotionGrid.querySelectorAll(".emotion-btn").forEach(b => b.classList.remove("active"));
  recommend({ text });
});

async function recommend(payload) {
  resultArea.innerHTML = `<div class="status">Finding something good…</div>`;
  try {
    const res = await fetch("/api/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `Request failed (${res.status})`);
    }
    const data = await res.json();
    renderResults(data);
  } catch (err) {
    resultArea.innerHTML = `<div class="status error">${escapeHtml(err.message)}</div>`;
  }
}

function renderResults(data) {
  const confidenceNote = data.source === "text"
    ? (data.confidence > 0
        ? `(detected from what you typed, confidence ${(data.confidence * 100).toFixed(0)}%)`
        : `(couldn't detect a clear mood — defaulting to something upbeat)`)
    : "";

  const header = `
    <div class="result-header">
      <span class="emoji">${data.emoji}</span>
      <span>Recommending movies for <strong>${data.emotion_label}</strong> ${confidenceNote}</span>
    </div>
  `;

  if (!data.movies.length) {
    resultArea.innerHTML = header + `<div class="status">No movies found — try a different mood.</div>`;
    return;
  }

  const cards = data.movies.map(m => `
    <div class="movie-card">
      ${m.poster_url
        ? `<img src="${m.poster_url}" alt="${escapeHtml(m.title)} poster" loading="lazy" />`
        : `<div class="no-poster">${escapeHtml(m.title)}</div>`}
      <div class="info">
        <p class="title">${escapeHtml(m.title)}</p>
        <p class="meta">⭐ ${m.rating?.toFixed(1) ?? "–"} · ${(m.release_date || "").slice(0, 4) || "–"}</p>
      </div>
    </div>
  `).join("");

  resultArea.innerHTML = header + `<div class="movie-grid">${cards}</div>`;
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str ?? "";
  return div.innerHTML;
}

loadEmotions();
