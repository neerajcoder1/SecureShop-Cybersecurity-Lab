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
            <a href="/videos.html">Tutorials</a>
            <a href="/dashboard.html">Dashboard</a>
            <a href="/profile.html">Profile</a>
            <a href="#" onclick="logout()" class="btn-nav">Logout</a>
            ${themeBtn}
        `;
  } else {
    nav.innerHTML = `
            <a href="/index.html">Home</a>
            <a href="/labs.html">Labs</a>
            <a href="/docs.html">Docs</a>
            <a href="/videos.html">Tutorials</a>
            <a href="https://github.com/neerajcoder1/SecureShop-Cybersecurity-Lab" target="_blank">GitHub</a>
            <a href="/login.html" class="btn-nav">Login / Register</a>
            ${themeBtn}
        `;
  }

  // Inject Mobile Toggle if not present
  const header = document.querySelector('header');
  if (header && !document.querySelector('.mobile-toggle')) {
      const toggle = document.createElement('button');
      toggle.className = 'mobile-toggle';
      toggle.innerHTML = '☰';
      toggle.onclick = () => nav.classList.toggle('active');
      header.insertBefore(toggle, nav);
  }
}

function injectFooter() {
  if (document.querySelector('footer')) return; // Already exists
  const footer = document.createElement('footer');
  footer.innerHTML = `
    <div class="footer-grid">
        <div>
            <div class="logo mb-1"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="logo-icon"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><polyline points="8 10 11 13 8 16"></polyline><line x1="13" y1="16" x2="16" y2="16"></line></svg> SecureShop Cybersecurity Lab</div>
            <p class="text-muted">Open-source cybersecurity practice environment.</p>
        </div>
        <div class="footer-links">
            <a href="/labs.html">Labs</a>
            <a href="/docs.html">Documentation</a>
            <a href="/videos.html">Tutorials</a>
            <a href="https://github.com/neerajcoder1/SecureShop-Cybersecurity-Lab" target="_blank">GitHub</a>
        </div>
    </div>
    <div class="footer-warning">
        Only use this platform for authorized security testing.
    </div>
  `;
  document.body.appendChild(footer);
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
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Initialize theme immediately to prevent flashing
initTheme();

document.addEventListener("DOMContentLoaded", () => {
  updateNav();
  injectFooter();
});

// Toast Notification System
function showToast(message, type = 'success') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  
  const formattedMsg = message.replace(/\n/g, '<br>');
  toast.innerHTML = formattedMsg;

  container.appendChild(toast);

  setTimeout(() => {
    toast.classList.add('fade-out');
    toast.addEventListener('animationend', () => toast.remove());
  }, 4000);
}

// Clear History
async function clearHistory() {
  if (!confirm("Are you sure you want to clear your entire operations history?")) return;
  try {
    const res = await fetchWithAuth(`${API_BASE}/orders`, { method: "DELETE" });
    if (res && res.ok) {
      showToast("[+] History wiped successfully.", "success");
      setTimeout(() => window.location.reload(), 1000);
    } else {
      showToast("[-] Failed to clear history.", "error");
    }
  } catch (e) {
    showToast("[-] Network error while clearing history.", "error");
  }
}
