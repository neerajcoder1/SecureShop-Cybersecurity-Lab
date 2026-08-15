
# SecureShop Lab

SecureShop Lab is a local cybersecurity learning application designed to demonstrate **secure coding practices** in Python FastAPI. It contrasts vulnerable coding patterns (described in documentation) with robust, secure implementations.

**IMPORTANT:** This application is intentionally designed to be a safe, secure reference. It runs exclusively on `127.0.0.1`.

## Features
- Secure Authentication (bcrypt hashing, JWT tokens)
- Prevention of SQL Injection via strict Parameterized Queries
- Protection against IDOR (Insecure Direct Object Reference)
- XSS prevention via safe DOM APIs (Vanilla JS `textContent`)

## Setup Instructions

1. Ensure you have Python 3.9+ installed.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the backend server. The database will initialize automatically:
   ```bash
   uvicorn backend.main:app --host 127.0.0.1 --port 8000
   ```

## Application URLs
- **Web App:** [http://127.0.0.1:8000/static/index.html](http://127.0.0.1:8000/static/index.html)
- **Security Docs:** [http://127.0.0.1:8000/static/security.html](http://127.0.0.1:8000/static/security.html)
- **API Swagger Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Inspecting with Burp Suite

To audit the HTTP requests using Burp Suite:
1. Open Burp Suite and ensure the proxy listener is running (usually `127.0.0.1:8080`).
2. Configure your browser to use Burp Suite as an HTTP proxy, or use Burp's embedded browser.
3. Navigate to `http://127.0.0.1:8000/static/index.html`.
4. Register a new user, log in, and interact with the application.
5. In Burp Suite's `Proxy > HTTP history` tab, you can inspect the API requests.
6. Notice that payloads sent (e.g., `' OR '1'='1` in the search) are safely neutralized by the backend's parameterized queries.

## Running Tests
To run the automated security checks:
```bash
pytest tests/
```
=======
# Lab-Testing-Injection-
>>>>>>> e5e3cae08e240735f1517aa90acdf0964c23de78
