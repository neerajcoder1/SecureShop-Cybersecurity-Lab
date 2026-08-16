const API_BASE = "https://secureshop-cybersecurity-lab.onrender.com/api";

function getToken() {
  return localStorage.getItem("token");
}

function setToken(token) {
  localStorage.setItem("token", token);
}

function logout() {
  localStorage.removeItem("token");
  window.location.href = "/login.html";
}

function updateNav() {
  const token = getToken();
  const nav = document.getElementById("main-nav");
  if (!nav) return;

  const themeBtn = `<a href="#" onclick="toggleTheme(); return false;" class="btn-nav" style="border:none; padding:0.4rem; font-size:1.2rem;" title="Toggle Theme">🌓</a>`;

  if (token) {
    nav.innerHTML = `
            <a href="/index.html">Home</a>
            <a href="/labs.html">Labs</a>
            <a href="/docs.html">Docs</a>
            <a href="/dashboard.html">Dashboard</a>
            <a href="/profile.html">Profile</a>
            <a href="#" onclick="logout()" class="btn-nav">Logout</a>
            ${themeBtn}
        `;
  } else {
    nav.innerHTML = `
            <a href="/index.html">Home</a>
            <a href="/labs.html">Labs</a>
            <a href="/security.html">Testing Guide</a>
            <a href="/docs.html">Docs</a>
            <a href="https://github.com/neerajcoder1/SecureShop-Cybersecurity-Lab" target="_blank">GitHub</a>
            <a href="/login.html" class="btn-nav">Login / Register</a>
            ${themeBtn}
        `;
  }
}

// SECURE: This function uses textContent instead of innerHTML to prevent XSS
function safeCreateElement(tag, text, className) {
  const el = document.createElement(tag);
  if (text) el.textContent = text;
  if (className) el.className = className;
  return el;
}

async function fetchWithAuth(url, options = {}) {
  const token = getToken();

  if (!token) {
    window.location.href = "/login.html";
    return;
  }

  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
    ...options.headers,
  };

  const response = await fetch(url, { ...options, headers });

  if (response.status === 401) {
    logout();
  }

  return response;
}

function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Initialize theme immediately to prevent flashing
initTheme();

document.addEventListener("DOMContentLoaded", () => {
  updateNav();
});
