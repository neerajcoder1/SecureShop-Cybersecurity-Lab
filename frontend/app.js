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

  if (token) {
    nav.innerHTML = `
            <a href="/index.html">Home</a>
            <a href="/profile.html">Profile & Orders</a>
            <a href="/security.html">Security Docs</a>
            <a href="#" onclick="logout()">Logout</a>
        `;
  } else {
    nav.innerHTML = `
            <a href="/index.html">Home</a>
            <a href="/security.html">Security Docs</a>
            <a href="/login.html">Login</a>
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

document.addEventListener("DOMContentLoaded", () => {
  updateNav();
});
