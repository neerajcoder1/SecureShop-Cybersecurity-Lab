LABS = [
    {
        "id": "secureshop",
        "name": "SecureShop Lab",
        "description": "Practice authentication, authorization, injection testing, and API security controls against a realistic e-commerce application.",
        "category": "Web Security",
        "difficulty": "Beginner",
        "xp_available": 150,
        "challenges_count": 3
    },
    {
        "id": "sqli",
        "name": "Advanced SQL Injection",
        "description": "Test whether application input is safely handled by parameterized database queries in complex search operations.",
        "category": "Injection",
        "difficulty": "Intermediate",
        "xp_available": 500,
        "challenges_count": 5
    },
    {
        "id": "xss",
        "name": "Cross-Site Scripting Lab",
        "description": "Exploit input/output handling flaws to execute arbitrary JavaScript in the context of the application.",
        "category": "Web Security",
        "difficulty": "Intermediate",
        "xp_available": 450,
        "challenges_count": 4
    },
    {
        "id": "auth",
        "name": "Broken Authentication Lab",
        "description": "Exploit weak passwords, insecure password resets, and JWT signature flaws.",
        "category": "Authentication",
        "difficulty": "Intermediate",
        "xp_available": 350,
        "challenges_count": 3
    },
    {
        "id": "api",
        "name": "API Security Lab",
        "description": "Exploit REST API endpoints with BOLA, Mass Assignment, and Asset Management flaws.",
        "category": "API Security",
        "difficulty": "Intermediate",
        "xp_available": 300,
        "challenges_count": 3
    },
    {
        "id": "authz",
        "name": "Authorization Lab",
        "description": "Exploit Missing Function Level Access Control, IDOR modification, and Parameter Tampering.",
        "category": "Authorization",
        "difficulty": "Advanced",
        "xp_available": 450,
        "challenges_count": 3
    },
    {
        "id": "browser",
        "name": "Browser Security Lab",
        "description": "Exploit Open Redirects, CORS misconfigurations, and Cross-Site Request Forgery (CSRF).",
        "category": "Browser Security",
        "difficulty": "Intermediate",
        "xp_available": 350,
        "challenges_count": 3
    },
    {
        "id": "network",
        "name": "Network Security Lab",
        "description": "Exploit Server-Side Request Forgery (SSRF), Command Injection, and Host Header Injection.",
        "category": "Network Security",
        "difficulty": "Advanced",
        "xp_available": 450,
        "challenges_count": 3
    },
    {
        "id": "crypto",
        "name": "Cryptography Lab",
        "description": "Exploit Weak RNG, Insecure Hashing, and Hardcoded Secrets.",
        "category": "Cryptography",
        "difficulty": "Advanced",
        "xp_available": 450,
        "challenges_count": 3
    },
    {
        "id": "logic",
        "name": "Business Logic Lab",
        "description": "Exploit Coupon Abuse, Trusting Client Data, and TOCTOU Race Conditions.",
        "category": "Business Logic",
        "difficulty": "Advanced",
        "xp_available": 450,
        "challenges_count": 3
    }
]

CHALLENGES = {
    "secureshop": [
        {
            "id": 1,
            "title": "Information Disclosure",
            "description": "The application might be leaking sensitive administrative information in its HTTP headers. Inspect the responses from the API.",
            "hint": "Check the HTTP response headers when you fetch the product list.",
            "difficulty": "Beginner",
            "xp": 50,
            "flag": "flag{headers_leak_info}",
            "badge": "🏆 InfoSec Scout"
        },
        {
            "id": 2,
            "title": "IDOR / Broken Access Control",
            "description": "A user's order history should be private. Try to access another user's order (specifically order ID 1).",
            "hint": "Create an order to see how the API fetches them, then manipulate the order_id in the URL to view order #1.",
            "difficulty": "Intermediate",
            "xp": 50,
            "flag": "flag{idor_access_granted}",
            "badge": "🏆 Access Breaker"
        },
        {
            "id": 3,
            "title": "SQL Injection",
            "description": "An older, deprecated search endpoint was left in the code. Find it and bypass the search logic.",
            "hint": "The endpoint is /api/products/search/vulnerable. Try a basic boolean-based payload like ' OR 1=1 --",
            "difficulty": "Advanced",
            "xp": 50,
            "flag": "flag{sqli_union_master}",
            "badge": "🏆 Injection Master"
        }
    ],
    "sqli": [
        {
            "id": 1,
            "title": "Basic SQL Injection",
            "description": "Identify a vulnerable parameter in the search functionality and trigger a generic database error.",
            "hint": "The endpoint is /api/labs/sqli/search?q=. Try inserting a single quote.",
            "difficulty": "Beginner",
            "xp": 50,
            "flag": "flag{sqli_basic_error}",
            "badge": "🏆 SQL Explorer"
        },
        {
            "id": 2,
            "title": "Authentication Bypass",
            "description": "Bypass the login prompt of the legacy admin portal using a tautology.",
            "hint": "The endpoint is /api/labs/sqli/login. Provide a username that always evaluates to true.",
            "difficulty": "Beginner",
            "xp": 100,
            "flag": "flag{sqli_auth_bypass}",
            "badge": "🏆 Gate Crasher"
        },
        {
            "id": 3,
            "title": "UNION-based Injection",
            "description": "Extract the database version using a UNION SELECT statement.",
            "hint": "Match the number of columns returned by the original query in /api/labs/sqli/search.",
            "difficulty": "Intermediate",
            "xp": 100,
            "flag": "flag{sqli_union_version}",
            "badge": "🏆 Union Worker"
        },
        {
            "id": 4,
            "title": "Data Extraction",
            "description": "Find the hidden 'super_secret' product in the database using UNION.",
            "hint": "Try appending UNION SELECT id, name, description, price, stock FROM products WHERE name='super_secret'",
            "difficulty": "Intermediate",
            "xp": 100,
            "flag": "flag{sqli_data_extraction}",
            "badge": "🏆 Data Miner"
        },
        {
            "id": 5,
            "title": "Blind SQL Injection Concept",
            "description": "Inject a payload that would allow inference of data based on response content.",
            "hint": "Try a boolean payload that checks if 1=1 and 1=2 yield different responses.",
            "difficulty": "Advanced",
            "xp": 150,
            "flag": "flag{sqli_blind_concept}",
            "badge": "🏆 Blind Seer"
        }
    ],
    "xss": [
        {
            "id": 1,
            "title": "Reflected XSS",
            "description": "Find a parameter that reflects user input directly into the HTML response.",
            "hint": "Check the /api/labs/xss/search endpoint.",
            "difficulty": "Beginner",
            "xp": 50,
            "flag": "flag{xss_reflected_basic}",
            "badge": "🏆 XSS Apprentice"
        },
        {
            "id": 2,
            "title": "Stored XSS",
            "description": "Inject a persistent payload into a vulnerable guestbook or comment section.",
            "hint": "Use /api/labs/xss/comment to POST a malicious comment.",
            "difficulty": "Intermediate",
            "xp": 100,
            "flag": "flag{xss_stored_persistent}",
            "badge": "🏆 Persistent Threat"
        },
        {
            "id": 3,
            "title": "DOM-based XSS",
            "description": "Manipulate the URL fragment to execute JavaScript in the browser DOM.",
            "hint": "Try adding #<script>alert(1)</script> to a vulnerable page simulator.",
            "difficulty": "Intermediate",
            "xp": 150,
            "flag": "flag{xss_dom_manipulation}",
            "badge": "🏆 DOM Dominator"
        },
        {
            "id": 4,
            "title": "Context-aware XSS",
            "description": "Bypass simple filters by injecting JavaScript directly into an HTML attribute context.",
            "hint": "The endpoint /api/labs/xss/profile reflects your input inside an <input value='...'> tag.",
            "difficulty": "Advanced",
            "xp": 150,
            "flag": "flag{xss_context_attribute}",
            "badge": "🏆 Context Master"
        }
    ],
    "auth": [
        {
            "id": 1,
            "title": "Weak Admin Password",
            "description": "The admin account is using a weak, easily guessable password.",
            "hint": "Try common default passwords on the /api/labs/auth/login endpoint for the username 'admin'.",
            "difficulty": "Beginner",
            "xp": 50,
            "flag": "flag{auth_weak_password}",
            "badge": "🏆 Password Guesser"
        },
        {
            "id": 2,
            "title": "JWT Signature Bypass",
            "description": "The application fails to verify JWT signatures properly if the algorithm is set to 'none'.",
            "hint": "Send a GET request to /api/labs/auth/verify_token with a forged JWT where the header has alg: none and payload has role: admin.",
            "difficulty": "Advanced",
            "xp": 150,
            "flag": "flag{auth_jwt_none_alg}",
            "badge": "🏆 Token Forger"
        },
        {
            "id": 3,
            "title": "Insecure Password Reset",
            "description": "The password reset API trusts user input for routing the reset email.",
            "hint": "POST to /api/labs/auth/reset_password with username='admin' but change the 'email' parameter to your own.",
            "difficulty": "Intermediate",
            "xp": 150,
            "flag": "flag{auth_insecure_reset}",
            "badge": "🏆 Reset Hijacker"
        }
    ],
    "api": [
        {
            "id": 1,
            "title": "BOLA / IDOR",
            "description": "Broken Object Level Authorization allows you to read private data of other users.",
            "hint": "Fetch /api/labs/api/users/1 to see if the admin's data is exposed.",
            "difficulty": "Beginner",
            "xp": 100,
            "flag": "flag{api_bola_access}",
            "badge": "🏆 Object Breaker"
        },
        {
            "id": 2,
            "title": "Mass Assignment",
            "description": "The profile update endpoint blindly accepts all JSON properties mapped to the user model.",
            "hint": "Send a PUT request to /api/labs/api/profile and include '\"role\": \"admin\"' in the JSON body.",
            "difficulty": "Intermediate",
            "xp": 100,
            "flag": "flag{api_mass_assignment}",
            "badge": "🏆 Privilege Escalator"
        },
        {
            "id": 3,
            "title": "Improper Asset Management",
            "description": "An old, deprecated API version is still running without authentication.",
            "hint": "Try accessing the undocumented /api/labs/api/v0/debug endpoint.",
            "difficulty": "Intermediate",
            "xp": 100,
            "flag": "flag{api_improper_assets}",
            "badge": "🏆 Artifact Hunter"
        }
    ],
    "authz": [
        {
            "id": 1,
            "title": "Missing Function Level Access Control",
            "description": "Access a restricted administrative endpoint without actually having an admin token.",
            "hint": "Try sending a GET request to /api/labs/authz/admin_panel.",
            "difficulty": "Intermediate",
            "xp": 150,
            "flag": "flag{authz_missing_flac}",
            "badge": "🏆 Function Bypass"
        },
        {
            "id": 2,
            "title": "IDOR - Modification",
            "description": "Modify another user's support ticket by tampering with the ID.",
            "hint": "Send a PUT request to /api/labs/authz/tickets/1 with a JSON body to modify the admin's ticket.",
            "difficulty": "Intermediate",
            "xp": 150,
            "flag": "flag{authz_idor_modification}",
            "badge": "🏆 Ticket Tamperer"
        },
        {
            "id": 3,
            "title": "Parameter Tampering",
            "description": "Exploit an insecure checkout endpoint by changing the total price of your cart.",
            "hint": "Send a POST request to /api/labs/authz/checkout with '\"total_price\": 0' in the JSON body.",
            "difficulty": "Advanced",
            "xp": 150,
            "flag": "flag{authz_param_tampering}",
            "badge": "🏆 Discount Hacker"
        }
    ],
    "browser": [
        {
            "id": 1,
            "title": "Open Redirect",
            "description": "Exploit a vulnerable redirect endpoint to redirect a victim to an external, malicious site.",
            "hint": "Send a GET request to /api/labs/browser/redirect?url=http://evil.com",
            "difficulty": "Beginner",
            "xp": 100,
            "flag": "flag{browser_open_redirect}",
            "badge": "🏆 Traffic Controller"
        },
        {
            "id": 2,
            "title": "CORS Misconfiguration",
            "description": "Find an endpoint that improperly reflects the Origin header, allowing attackers to steal data via cross-origin requests.",
            "hint": "Send a GET request to /api/labs/browser/cors_data with an 'Origin: http://evil.com' header.",
            "difficulty": "Intermediate",
            "xp": 100,
            "flag": "flag{browser_cors_misconfig}",
            "badge": "🏆 Origin Spoof"
        },
        {
            "id": 3,
            "title": "Cross-Site Request Forgery (CSRF)",
            "description": "Exploit a state-changing endpoint that lacks an Anti-CSRF token.",
            "hint": "Send a POST request to /api/labs/browser/update_email with '\"email\": \"hacker@evil.com\"' but NO csrf_token parameter.",
            "difficulty": "Intermediate",
            "xp": 150,
            "flag": "flag{browser_csrf_bypass}",
            "badge": "🏆 Request Forger"
        }
    ],
    "network": [
        {
            "id": 1,
            "title": "Server-Side Request Forgery (SSRF)",
            "description": "Force the server to request an internal API that is only accessible from the loopback interface.",
            "hint": "POST to /api/labs/network/fetch with '\"url\": \"http://localhost:8000/api/labs/network/internal/secret\"'.",
            "difficulty": "Intermediate",
            "xp": 150,
            "flag": "flag{network_ssrf_internal}",
            "badge": "🏆 Internal Explorer"
        },
        {
            "id": 2,
            "title": "OS Command Injection",
            "description": "Exploit a network diagnostic tool by appending a malicious command payload.",
            "hint": "Send a GET request to /api/labs/network/ping?host=127.0.0.1;whoami",
            "difficulty": "Advanced",
            "xp": 150,
            "flag": "flag{network_command_injection}",
            "badge": "🏆 Shell Popper"
        },
        {
            "id": 3,
            "title": "Host Header Injection",
            "description": "Exploit a password reset endpoint that dynamically generates the reset link based on the HTTP Host header.",
            "hint": "Send a POST request to /api/labs/network/reset_password but change the 'Host' header to 'evil.com'.",
            "difficulty": "Intermediate",
            "xp": 150,
            "flag": "flag{network_host_header}",
            "badge": "🏆 Header Hijacker"
        }
    ],
    "crypto": [
        {
            "id": 1,
            "title": "Weak RNG",
            "description": "Exploit an endpoint that uses an insecure random number generator.",
            "hint": "Call /api/labs/crypto/lottery multiple times to predict the outcome.",
            "difficulty": "Beginner",
            "xp": 100,
            "flag": "flag{crypto_weak_rng}",
            "badge": "🏆 RNG Predictor"
        },
        {
            "id": 2,
            "title": "Insecure Hashing",
            "description": "Exploit an endpoint using an obsolete hashing algorithm (MD5) to verify data integrity.",
            "hint": "POST /api/labs/crypto/hash with '{\"data\": \"admin\"}' and its MD5 hash.",
            "difficulty": "Intermediate",
            "xp": 150,
            "flag": "flag{crypto_md5_collision}",
            "badge": "🏆 Hash Cracker"
        },
        {
            "id": 3,
            "title": "Hardcoded Secrets",
            "description": "Extract a hardcoded encryption key left behind in an API response.",
            "hint": "Check the response headers or body of /api/labs/crypto/encryption_key.",
            "difficulty": "Beginner",
            "xp": 100,
            "flag": "flag{crypto_hardcoded_key}",
            "badge": "🏆 Secret Finder"
        }
    ],
    "logic": [
        {
            "id": 1,
            "title": "Coupon Code Abuse",
            "description": "Apply a $10 off coupon recursively to achieve a negative balance.",
            "hint": "Send GET /api/labs/logic/apply_coupon?code=SAVE10 multiple times.",
            "difficulty": "Intermediate",
            "xp": 150,
            "flag": "flag{logic_coupon_abuse}",
            "badge": "🏆 Discount Abuser"
        },
        {
            "id": 2,
            "title": "Trusting Client Data",
            "description": "Submit a negative quantity to the shopping cart to decrease the total price.",
            "hint": "POST /api/labs/logic/cart with '{\"item_id\": 1, \"quantity\": -5}'.",
            "difficulty": "Intermediate",
            "xp": 150,
            "flag": "flag{logic_negative_quantity}",
            "badge": "🏆 Negative Balance"
        },
        {
            "id": 3,
            "title": "Race Condition (TOCTOU)",
            "description": "Exploit a Time-of-Check to Time-of-Use flaw in a simulated fund transfer.",
            "hint": "POST /api/labs/logic/transfer_funds multiple times concurrently.",
            "difficulty": "Advanced",
            "xp": 200,
            "flag": "flag{logic_race_condition}",
            "badge": "🏆 Speed Racer"
        }
    ]
}
