<td width="40%" align="center">
 <img width="900" height="260" alt="cybersecurity-tools(1)" src="https://github.com/user-attachments/assets/6abd98d8-fc99-41ca-afc2-65b10c5b10d0" />

</td>

<h1 align="center">SecureShop Cybersecurity Testing Lab</h1>

<p align="center">
  <strong>Authorized Web Application Security Testing & Education</strong>
</p>

<p align="center">
  <a href="https://secure-shop-cybersecurity-lab.vercel.app">
    <img src="https://img.shields.io/badge/Live%20Frontend-Vercel-black?style=for-the-badge&logo=vercel" alt="Live Frontend">
  </a>
  <a href="https://secureshop-cybersecurity-lab.onrender.com">
    <img src="https://img.shields.io/badge/API-Render-46E3B7?style=for-the-badge&logo=render" alt="Backend API">
  </a>
</p>

---

A deliberately security-focused e-commerce application designed for **authorized cybersecurity testing, penetration-testing practice, and web application security education**.

SecureShop provides a realistic environment where security learners can practice identifying vulnerabilities, validating security controls, analyzing HTTP traffic, and understanding how secure implementations defend against common web attacks.

> [!WARNING]
> **Authorized Testing Only:** Only test this application when you have explicit authorization. Do not use the techniques described here against websites, APIs, accounts, or systems that you do not own or have permission to assess.

## 💻 Tech Stack
- **Backend:** Python, FastAPI, SQLite
- **Frontend:** Vanilla JavaScript, HTML5, CSS3 (Custom 3D Neumorphic Dark Theme)
- **Deployment:** Render (API), Vercel (Frontend)

## 🎯 Key Features
- **Interactive Web Terminal:** Test APIs directly from the browser using a simulated terminal. Practice commands like `curl` and `sqlmap` to validate challenges before submission.
- **Realistic E-Commerce Workflow:** A fully functional storefront with products, carts, orders, and reviews.
- **Dedicated Workspaces:** Track your progress as you work through specific vulnerability categories.
- **Built-in Vulnerabilities & Protections:** Configured to allow for testing of SQLi, XSS, BOLA/IDOR, and JWT manipulation in a safe, sandboxed environment.

---

## Why SecureShop?

Cybersecurity skills require hands-on practice, but many learners face barriers such as
lab costs, complicated setup requirements, or limited access to realistic web applications.

**SecureShop Cybersecurity Testing Lab** was created as a free and open-source alternative
for practicing web application security in a realistic e-commerce environment.

### What makes SecureShop useful?

- **Free to use**
- **Open source**
- **Browser-accessible**
- **Realistic e-commerce workflow**
- **Designed for authorized security testing**
- **No paid lab subscription required**
- **Practice common web and API security concepts**
- **Use professional tools such as Burp Suite and OWASP ZAP**
- **Learn both offensive testing and defensive implementation**

The goal is simple:

> **Learn → Test → Understand → Secure**

SecureShop is intended for students, developers, cybersecurity learners,
and security enthusiasts who want a practical environment for learning
web application security.

 ---

 ## Free Cybersecurity Practice Lab

SecureShop is built around the idea that practical cybersecurity education
should be accessible.

Instead of only reading about vulnerabilities, learners can interact with
a real application, inspect HTTP requests, test authentication and
authorization controls, analyze API behavior, and understand how secure
implementations defend against common attacks.

**Cost:** Free  
**Source:** Open Source  
**Access:** Web Browser + Local Deployment  
**Purpose:** Cybersecurity Education & Authorized Testing 

---

## 🚀 Local Installation & Setup

Want to run the lab locally for offline practice or to contribute to the codebase? Follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/neerajcoder1/SecureShop-Cybersecurity-Lab.git
   cd SecureShop-Cybersecurity-Lab
   ```

2. **Set up the backend environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Run the API server:**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

4. **Launch the frontend:**
   Use any local web server (like VS Code Live Server or Python's `http.server`) to serve the `/frontend` directory on port 5500.
   ```bash
   # In a new terminal window
   cd frontend
   python -m http.server 5500
   ```
   Navigate to `http://localhost:5500` in your browser.

---

## 📂 Project Structure

```text
SecureShop-Cybersecurity-Lab/
├── backend/          # FastAPI server, database models, and API logic
│   ├── main.py       # API endpoints and route definitions
│   ├── auth.py       # JWT and password hashing (Bcrypt) logic
│   ├── database.py   # SQLite database connection and queries
│   └── models.py     # Pydantic data models
├── frontend/         # Pure HTML/CSS/JS frontend (Dark Hacker UI)
│   ├── index.html    # Landing page and dashboard
│   ├── workspace.html# Interactive terminal and challenge environment
│   ├── app.js        # Core frontend logic and API interactions
│   └── app.css       # Neumorphic styling and responsive layouts
└── requirements.txt  # Python dependencies
```

---
 
# Resources & Further Learning

## Web Application Security

- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
  - Comprehensive methodology for web application security testing.

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
  - Learn about the most critical web application security risks.

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
  - Learn common API security risks and testing concepts.

## Security Testing Tools

- [Burp Suite Documentation](https://portswigger.net/burp/documentation)
  - HTTP interception, request analysis, and web security testing.

- [OWASP ZAP Documentation](https://www.zaproxy.org/docs/)
  - Open-source web application security testing.

- [Postman Learning Center](https://learning.postman.com/)
  - REST API testing and API development.

## Web Security Concepts

- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
  - Understand SQL injection and defensive techniques.

- [OWASP Cross-Site Scripting](https://owasp.org/www-community/attacks/xss/)
  - Understand XSS and secure output handling.

- [OWASP IDOR / Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
  - Learn object-level authorization and access-control failures.

- [MDN HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)
  - Learn HTTP requests, responses, headers, methods, and status codes.

- [MDN CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS)
  - Understand browser cross-origin security.

## API & Authentication

- [JWT Introduction](https://jwt.io/introduction/)
  - Understand JSON Web Tokens and their structure.

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
  - Learn the backend framework used by SecureShop.

- [SQLite Documentation](https://sqlite.org/docs.html)
  - Understand the database used in the local lab.

---

# Suggested Learning Path

```text
HTTP Fundamentals
       ↓
Web Application Architecture
       ↓
OWASP Top 10
       ↓
Burp Suite / OWASP ZAP
       ↓
Authentication
       ↓
Authorization & IDOR
       ↓
SQL Injection
       ↓
XSS
       ↓
API Security
       ↓
JWT
       ↓
Business Logic Testing
       ↓
Security Reporting


```

--- 
# What You Can Practice

```text


| Security Area         | What You Can Practice                     |
| --------------------- | ----------------------------------------- |
| **SQL Injection**     | Test whether user input is safely handled |
| **Authentication**    | Test login and registration controls      |
| **Authorization**     | Test access-control enforcement           |
| **IDOR**              | Test object-level authorization           |
| **XSS**               | Test input/output handling                |
| **API Security**      | Test REST API endpoints                   |
| **JWT**               | Analyze authentication tokens             |
| **Input Validation**  | Test unexpected or malformed input        |
| **CORS**              | Analyze cross-origin access               |
| **Business Logic**    | Test application workflows                |
| **HTTP**              | Inspect requests and responses            |
| **Database Security** | Understand parameterized queries          |
| **Security Headers**  | Inspect browser security controls         |

```
 ---
 ## Project Roadmap

SecureShop is the first lab in a growing open-source cybersecurity learning platform.

### Phase 1 — SecureShop Lab Foundation
**CURRENT — Building Now**

Professional UI/UX, interactive testing environment, security documentation, and the core SecureShop cybersecurity lab.

---

### Phase 2 — Interactive Challenge Engine
**COMING NEXT**

Turn security testing into structured challenges with:

- Interactive objectives
- Challenge scenarios
- Flags
- Automated validation
- Hints
- Difficulty levels
- Progress tracking

---

### Phase 3 — More Security Labs
**ON THE HORIZON**

Expand beyond SecureShop with dedicated labs for:

- SQL Injection
- XSS
- IDOR
- Authentication
- JWT
- API Security
- CORS
- File Upload Security
- Command Injection
- Web Reconnaissance

---

### Phase 4 — Cybersecurity Learning Platform
**IN THE PIPELINE**

Build the platform layer:

- Learning paths
- User progress
- XP and achievements
- Badges
- Leaderboards
- Challenge history
- Beginner → Advanced tracks

---

### Phase 5 — Open-Source Security Ecosystem
**LONG-TERM VISION**

Create a community-driven cybersecurity practice ecosystem:

- Community-created labs
- Lab contributions
- CTF-style environments
- Advanced security challenges
- Educational resources
- Contributor recognition


