# Contributing to SecureShop Cybersecurity Lab

First off, thank you for considering contributing to SecureShop! This is an open-source project designed to provide a safe, legal environment for developers and security enthusiasts to practice web application security.

## Technology Stack & Architecture

To keep this project highly accessible, lightweight, and easy for beginners to run locally, we strictly enforce the following technology stack in this repository:

- **Frontend:** Vanilla HTML, CSS (Custom variables), and JavaScript. No build steps required.
- **Backend:** Python (FastAPI/Flask) REST API.
- **Database:** SQLite.

### 🚫 Why No React, Angular, or Node.js?
We purposefully avoid using heavy frontend frameworks (like React, Vue, or Angular) or Node.js in the main repository. We want users to be able to clone the project, double-click an `.html` file, and instantly start learning without having to run `npm install` or configure complex build tools like Webpack or Vite. 

## How You Can Contribute

We welcome contributions in the following areas:
1. **New Security Labs:** Adding new vulnerable endpoints (in Python) and corresponding UI challenges (in HTML/JS).
2. **UI/UX Improvements:** Enhancing the dark-theme terminal aesthetic using CSS and Vanilla JS.
3. **Documentation:** Improving the `docs.html` guide with better theory and command explanations.
4. **Bug Fixes:** Resolving existing UI bugs or backend logic errors.

## What if I want to use React or the MERN Stack?

That is highly encouraged, but **not in this repository!**

Because SecureShop uses a decoupled REST API backend, the frontend is completely separate from the database logic. If you are a React developer and want to build a "SecureShop React Frontend", please do the following:

1. Create a brand new, separate GitHub repository (e.g., `YourName/SecureShop-React`).
2. Build your React/MERN frontend to interact with our existing Python API endpoints.
3. Open an issue in this repository to let us know! We would love to link to your community project in our `README.md` to show off your work.

## Pull Request Process

1. Fork the repository and create your branch from `main`.
2. Ensure your code does not break existing lab logic.
3. If you've changed the UI, ensure it adheres to the existing "terminal hacker" design aesthetic (dark mode `#0d1117`, green/blue accents).
4. Submit a PR with a clear description of what you've changed and why.

Thank you for helping make web security education accessible!
