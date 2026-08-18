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
    },
    {
        "id": "graphql",
        "name": "GraphQL Security Lab",
        "description": "Exploit Introspection, BOLA in Resolvers, and Query Batching.",
        "category": "GraphQL Security",
        "difficulty": "Advanced",
        "xp_available": 450,
        "challenges_count": 3
    },
    {
        "id": "adv_inject",
        "name": "Advanced Injection Lab",
        "description": "Exploit Server-Side Template Injection (SSTI), XXE, and Blind Command Injection.",
        "category": "Advanced Injection",
        "difficulty": "Expert",
        "xp_available": 600,
        "challenges_count": 3
    },
    {
        "id": "file_upload",
        "name": "Insecure File Uploads",
        "description": "Exploit basic extension bypass, content-type spoofing, and path traversal.",
        "category": "File Uploads",
        "difficulty": "Advanced",
        "xp_available": 450,
        "challenges_count": 3
    },
    {
        "id": "nosql",
        "name": "NoSQL Injection Lab",
        "description": "Exploit authentication bypass with $ne, data extraction with $regex, and $in operators.",
        "category": "NoSQL Injection",
        "difficulty": "Expert",
        "xp_available": 600,
        "challenges_count": 3
    },
    {
        "id": "ssrf",
        "name": "Server-Side Request Forgery",
        "description": "Exploit basic internal access, blind port scanning, and cloud metadata theft.",
        "category": "SSRF",
        "difficulty": "Advanced",
        "xp_available": 450,
        "challenges_count": 3
    },
    {
        "id": "deserialization",
        "name": "Insecure Deserialization",
        "description": "Exploit Python pickle RCE, YAML deserialization, and JWT None algorithm.",
        "category": "Insecure Deserialization",
        "difficulty": "Expert",
        "xp_available": 600,
        "challenges_count": 3
    },
    {
        "id": "oauth",
        "name": "OAuth & SSO Security",
        "description": "Exploit flawed state validation, redirect URI manipulation, and implicit flow.",
        "category": "OAuth Security",
        "difficulty": "Advanced",
        "xp_available": 450,
        "challenges_count": 3
    },
    {
        "id": "cors",
        "name": "CORS Misconfigurations",
        "description": "Bypass Cross-Origin Resource Sharing via reflected origins, null, and regex bypasses.",
        "category": "CORS Misconfigurations",
        "difficulty": "Intermediate",
        "xp_available": 450,
        "challenges_count": 3
    },
    {
        "id": "cmd_injection",
        "name": "Command Injection",
        "description": "Execute arbitrary OS commands via basic concatenation, blind injection, and filter bypass.",
        "category": "Command Injection",
        "difficulty": "Expert",
        "xp_available": 600,
        "challenges_count": 3
    },
    {
        "id": "ssti",
        "name": "Server-Side Template Injection",
        "description": "Exploit Jinja2 templates to evaluate math, dump env vars, and execute code via __subclasses__.",
        "category": "SSTI",
        "difficulty": "Expert",
        "xp_available": 600,
        "challenges_count": 3
    },
    {
        "id": "xxe",
        "name": "XML External Entity (XXE)",
        "description": "Exploit XML parsers to read local files, trigger SSRF, and execute DoS attacks.",
        "category": "XXE Injection",
        "difficulty": "Advanced",
        "xp_available": 450,
        "challenges_count": 3
    },
    {
        "id": "host_header",
        "name": "Host Header Injection",
        "description": "Exploit blind trust in the Host header for password resets, cache poisoning, and routing.",
        "category": "Host Header Injection",
        "difficulty": "Advanced",
        "xp_available": 450,
        "challenges_count": 3
    },
    {
        "id": "api_sec",
        "name": "Advanced API Security",
        "description": "Exploit Mass Assignment, HTTP Parameter Pollution, and deprecated API endpoints.",
        "category": "API Security",
        "difficulty": "Intermediate",
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
    ],
    "graphql": [
        {
            "id": 1,
            "title": "Introspection Enabled",
            "description": "Dump the entire GraphQL API schema to find hidden endpoints.",
            "hint": "POST to /api/labs/graphql with query '{ __schema { types { name } } }'.",
            "difficulty": "Intermediate",
            "xp": 150,
            "flag": "flag{graphql_introspection}",
            "badge": "🏆 Schema Dumper"
        },
        {
            "id": 2,
            "title": "BOLA in Resolvers",
            "description": "Query a user by ID to extract the admin's private flag.",
            "hint": "POST to /api/labs/graphql with query '{ user(id: 1) { email flag } }'.",
            "difficulty": "Advanced",
            "xp": 200,
            "flag": "flag{graphql_bola_resolver}",
            "badge": "🏆 Node Crawler"
        },
        {
            "id": 3,
            "title": "Query Batching (Rate Limit Bypass)",
            "description": "Send an array of queries in a single request to brute-force an OTP.",
            "hint": "POST an array of queries to /api/labs/graphql: [{'query': '{ verifyOTP(code: \"1234\") }'}, ...]",
            "difficulty": "Expert",
            "xp": 250,
            "flag": "flag{graphql_query_batching}",
            "badge": "🏆 Batch Attacker"
        }
    ],
    "adv_inject": [
        {
            "id": 1,
            "title": "Server-Side Template Injection (SSTI)",
            "description": "Exploit a vulnerable template renderer to evaluate mathematical expressions.",
            "hint": "Send GET /api/labs/adv_inject/template?name={{7*7}}",
            "difficulty": "Advanced",
            "xp": 200,
            "flag": "flag{adv_inject_ssti}",
            "badge": "🏆 Template Hacker"
        },
        {
            "id": 2,
            "title": "XML External Entity (XXE)",
            "description": "Exploit an insecure XML parser to read internal files.",
            "hint": "POST XML to /api/labs/adv_inject/xml with a SYSTEM entity.",
            "difficulty": "Expert",
            "xp": 250,
            "flag": "flag{adv_inject_xxe}",
            "badge": "🏆 Entity Exploiter"
        },
        {
            "id": 3,
            "title": "Blind Command Injection",
            "description": "Exploit an asynchronous ping service using time-based blind injection.",
            "hint": "POST to /api/labs/adv_inject/ping_async with a sleep payload.",
            "difficulty": "Expert",
            "xp": 250,
            "flag": "flag{adv_inject_blind_cmd}",
            "badge": "🏆 Time Lord"
        }
    ],
    "file_upload": [
        {
            "id": 1,
            "title": "Basic Extension Bypass",
            "description": "Upload a PHP web shell to an endpoint that fails to check file extensions.",
            "hint": "Upload a file named shell.php to /api/labs/file_upload/basic.",
            "difficulty": "Intermediate",
            "xp": 150,
            "flag": "flag{upload_basic_bypass}",
            "badge": "🏆 Shell Uploader"
        },
        {
            "id": 2,
            "title": "Content-Type Bypass",
            "description": "Bypass validation by altering the Content-Type header of a malicious upload.",
            "hint": "Upload shell.php to /api/labs/file_upload/content_type, but change Content-Type to image/jpeg in Burp.",
            "difficulty": "Advanced",
            "xp": 200,
            "flag": "flag{upload_content_type_spoof}",
            "badge": "🏆 MIME Spoofer"
        },
        {
            "id": 3,
            "title": "Path Traversal Upload",
            "description": "Overwrite system files by injecting path traversal characters into the filename.",
            "hint": "Upload to /api/labs/file_upload/path_traversal with filename ../../../etc/cron.d/malware.",
            "difficulty": "Expert",
            "xp": 250,
            "flag": "flag{upload_path_traversal}",
            "badge": "🏆 Traversal Master"
        }
    ],
    "nosql": [
        {
            "id": 1,
            "title": "Authentication Bypass ($ne)",
            "description": "Bypass the login by using the MongoDB Not-Equal operator.",
            "hint": "POST to /api/labs/nosql/auth_bypass with {\"username\": \"admin\", \"password\": {\"$ne\": \"wrong\"}}.",
            "difficulty": "Intermediate",
            "xp": 150,
            "flag": "flag{nosql_auth_bypass}",
            "badge": "🏆 $ne Hacker"
        },
        {
            "id": 2,
            "title": "Data Extraction ($regex)",
            "description": "Use Regular Expressions to blindly extract the flag character-by-character.",
            "hint": "POST to /api/labs/nosql/regex with {\"username\": \"admin\", \"reset_token\": {\"$regex\": \"^flag{a.*\"}}.",
            "difficulty": "Advanced",
            "xp": 200,
            "flag": "flag{nosql_regex_extract}",
            "badge": "🏆 Regex Ninja"
        },
        {
            "id": 3,
            "title": "Array Operator Bypass ($in)",
            "description": "Bypass ID validation by injecting an array operator.",
            "hint": "POST to /api/labs/nosql/array with {\"doc_id\": {\"$in\": [1, 2, 3]}}.",
            "difficulty": "Advanced",
            "xp": 200,
            "flag": "flag{nosql_array_bypass}",
            "badge": "🏆 Array Injector"
        }
    ],
    "ssrf": [
        {
            "id": 1,
            "title": "Basic Internal SSRF",
            "description": "Exploit a URL fetching feature to access an internal admin endpoint.",
            "hint": "POST to /api/labs/ssrf/fetch with {\"url\": \"http://localhost:8000/api/internal-admin\"}.",
            "difficulty": "Intermediate",
            "xp": 150,
            "flag": "flag{ssrf_basic_internal}",
            "badge": "🏆 Internal Scanner"
        },
        {
            "id": 2,
            "title": "Blind SSRF",
            "description": "Exploit a blind SSRF to verify if a service is running on the internal network.",
            "hint": "POST to /api/labs/ssrf/blind with {\"url\": \"http://localhost:8000\"}. (Any successful connection works)",
            "difficulty": "Advanced",
            "xp": 200,
            "flag": "flag{ssrf_blind_ping}",
            "badge": "🏆 Blind Spotter"
        },
        {
            "id": 3,
            "title": "Cloud Metadata Exfiltration",
            "description": "Trick the server into fetching its simulated AWS IAM security credentials.",
            "hint": "POST to /api/labs/ssrf/fetch with {\"url\": \"http://169.254.169.254/latest/meta-data/iam/security-credentials/\"}.",
            "difficulty": "Expert",
            "xp": 250,
            "flag": "flag{ssrf_cloud_metadata}",
            "badge": "🏆 Cloud Stealer"
        }
    ],
    "deserialization": [
        {
            "id": 1,
            "title": "Python Pickle RCE",
            "description": "Exploit an insecure endpoint that unpickles user-supplied base64 data.",
            "hint": "POST to /api/labs/deserialization/pickle with a malicious base64-encoded pickle object.",
            "difficulty": "Expert",
            "xp": 250,
            "flag": "flag{deserialization_pickle_rce}",
            "badge": "🏆 Pickle Rick"
        },
        {
            "id": 2,
            "title": "YAML Deserialization",
            "description": "Exploit the insecure yaml.load() function to execute code.",
            "hint": "POST to /api/labs/deserialization/yaml with yaml payload containing !!python/object/apply:os.system.",
            "difficulty": "Advanced",
            "xp": 200,
            "flag": "flag{deserialization_yaml_rce}",
            "badge": "🏆 YAML Hacker"
        },
        {
            "id": 3,
            "title": "JWT 'None' Algorithm",
            "description": "Forge a JWT token by changing the algorithm to 'None' and stripping the signature.",
            "hint": "POST to /api/labs/deserialization/jwt_none with {\"token\": \"eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VybmFtZSI6ImFkbWluIn0.\"} (Notice the trailing dot and no signature).",
            "difficulty": "Intermediate",
            "xp": 150,
            "flag": "flag{deserialization_jwt_none}",
            "badge": "🏆 Token Forger II"
        }
    ],
    "oauth": [
        {
            "id": 1,
            "title": "Flawed State Parameter",
            "description": "Exploit a missing or unvalidated state parameter to launch an OAuth CSRF attack.",
            "hint": "GET /api/labs/oauth/login?code=hacker_code without a state parameter.",
            "difficulty": "Intermediate",
            "xp": 150,
            "flag": "flag{oauth_flawed_state}",
            "badge": "🏆 State Manipulator"
        },
        {
            "id": 2,
            "title": "Redirect URI Manipulation",
            "description": "Exploit an insecure regex validation to steal the OAuth authorization code.",
            "hint": "GET /api/labs/oauth/callback?redirect_uri=https://trusted.com.attacker.com",
            "difficulty": "Advanced",
            "xp": 200,
            "flag": "flag{oauth_redirect_bypass}",
            "badge": "🏆 URI Stealer"
        },
        {
            "id": 3,
            "title": "Implicit Flow Token Leak",
            "description": "Simulate stealing an access token leaked in the URL fragment via Referer headers.",
            "hint": "GET /api/labs/oauth/implicit with an 'Origin: attacker.com' header to simulate a cross-origin leak.",
            "difficulty": "Expert",
            "xp": 250,
            "flag": "flag{oauth_implicit_leak}",
            "badge": "🏆 Fragment Stealer"
        }
    ],
    "cors": [
        {
            "id": 1,
            "title": "Reflected Origin",
            "description": "Bypass CORS by exploiting a server that blindly reflects any Origin header.",
            "hint": "GET /api/labs/cors/reflected with 'Origin: https://malicious.com'.",
            "difficulty": "Intermediate",
            "xp": 150,
            "flag": "flag{cors_reflected_origin}",
            "badge": "🏆 Origin Reflector"
        },
        {
            "id": 2,
            "title": "Null Origin Trusted",
            "description": "Bypass CORS by supplying the 'null' origin.",
            "hint": "GET /api/labs/cors/null with 'Origin: null'.",
            "difficulty": "Intermediate",
            "xp": 150,
            "flag": "flag{cors_null_origin}",
            "badge": "🏆 Null Trusted"
        },
        {
            "id": 3,
            "title": "Prefix/Suffix Regex Bypass",
            "description": "Bypass a flawed origin check that only verifies if the domain starts with a trusted string.",
            "hint": "GET /api/labs/cors/prefix with 'Origin: https://trusted.com.attacker.com'.",
            "difficulty": "Advanced",
            "xp": 200,
            "flag": "flag{cors_prefix_bypass}",
            "badge": "🏆 Regex Evader"
        }
    ],
    "cmd_injection": [
        {
            "id": 1,
            "title": "Basic Command Concatenation",
            "description": "Inject an OS command via a semicolon (;) or ampersand (&&).",
            "hint": "POST to /api/labs/cmd/ping with {\"ip\": \"127.0.0.1; whoami\"}",
            "difficulty": "Intermediate",
            "xp": 150,
            "flag": "flag{cmd_basic_concat}",
            "badge": "🏆 Shell Hacker"
        },
        {
            "id": 2,
            "title": "Blind Time-Based Injection",
            "description": "Exploit blind command injection by making the server sleep.",
            "hint": "POST to /api/labs/cmd/blind with {\"ip\": \"127.0.0.1; sleep 5\"}",
            "difficulty": "Advanced",
            "xp": 200,
            "flag": "flag{cmd_blind_sleep}",
            "badge": "🏆 Time Lord"
        },
        {
            "id": 3,
            "title": "Filter Bypass (${IFS})",
            "description": "Bypass a filter that blocks spaces and semicolons.",
            "hint": "POST to /api/labs/cmd/filter with {\"ip\": \"127.0.0.1|cat${IFS}/etc/passwd\"}",
            "difficulty": "Expert",
            "xp": 250,
            "flag": "flag{cmd_filter_bypass}",
            "badge": "🏆 Filter Evader"
        }
    ],
    "ssti": [
        {
            "id": 1,
            "title": "Template Math Evaluation",
            "description": "Prove template injection by evaluating a mathematical expression.",
            "hint": "POST to /api/labs/ssti/math with {\"template\": \"{{ 7 * 7 }}\"}",
            "difficulty": "Intermediate",
            "xp": 150,
            "flag": "flag{ssti_basic_math}",
            "badge": "🏆 Template Math"
        },
        {
            "id": 2,
            "title": "Environment Variable Dump",
            "description": "Dump the server's environment variables or configuration.",
            "hint": "POST to /api/labs/ssti/env with {\"template\": \"{{ config.items() }}\"}",
            "difficulty": "Advanced",
            "xp": 200,
            "flag": "flag{ssti_env_dump}",
            "badge": "🏆 Env Stealer"
        },
        {
            "id": 3,
            "title": "RCE via __subclasses__",
            "description": "Achieve Remote Code Execution by traversing the Python MRO.",
            "hint": "POST to /api/labs/ssti/rce with a payload using ''.__class__.__mro__[1].__subclasses__() to run os.popen.",
            "difficulty": "Expert",
            "xp": 250,
            "flag": "flag{ssti_rce_subclasses}",
            "badge": "🏆 SSTI Master"
        }
    ],
    "xxe": [
        {
            "id": 1,
            "title": "Local File Inclusion (LFI)",
            "description": "Read a local file using a custom external XML entity.",
            "hint": "POST XML to /api/labs/xxe/lfi defining an entity <!ENTITY xxe SYSTEM 'file:///etc/passwd'> and echoing it.",
            "difficulty": "Intermediate",
            "xp": 150,
            "flag": "flag{xxe_basic_lfi}",
            "badge": "🏆 XML Reader"
        },
        {
            "id": 2,
            "title": "Billion Laughs (DoS)",
            "description": "Attempt to exhaust server memory using nested XML entities.",
            "hint": "POST a classic Billion Laughs XML payload to /api/labs/xxe/dos.",
            "difficulty": "Expert",
            "xp": 250,
            "flag": "flag{xxe_billion_laughs}",
            "badge": "🏆 Laughing Hacker"
        },
        {
            "id": 3,
            "title": "SSRF via XXE",
            "description": "Force the XML parser to fetch an internal URL.",
            "hint": "POST XML to /api/labs/xxe/ssrf with <!ENTITY xxe SYSTEM 'http://169.254.169.254/latest/meta-data/'>.",
            "difficulty": "Advanced",
            "xp": 200,
            "flag": "flag{xxe_ssrf_fetch}",
            "badge": "🏆 XML Fetcher"
        }
    ],
    "host_header": [
        {
            "id": 1,
            "title": "Password Reset Poisoning",
            "description": "Exploit blind trust in the Host header to poison a password reset link.",
            "hint": "POST to /api/labs/host/reset with a custom 'Host: attacker.com' header.",
            "difficulty": "Intermediate",
            "xp": 150,
            "flag": "flag{host_reset_poison}",
            "badge": "🏆 Host Manipulator"
        },
        {
            "id": 2,
            "title": "Web Cache Poisoning",
            "description": "Inject your Host header into a cached response to affect other users.",
            "hint": "GET /api/labs/host/cache with 'Host: attacker.com'. Notice how it is reflected in a script tag.",
            "difficulty": "Advanced",
            "xp": 200,
            "flag": "flag{host_cache_poison}",
            "badge": "🏆 Cache Poisoner"
        },
        {
            "id": 3,
            "title": "Internal Routing Bypass",
            "description": "Bypass a reverse proxy by supplying an internal virtual host.",
            "hint": "GET /api/labs/host/internal with 'Host: internal-admin.local'.",
            "difficulty": "Advanced",
            "xp": 200,
            "flag": "flag{host_routing_bypass}",
            "badge": "🏆 Routing Evader"
        }
    ],
    "api_sec": [
        {
            "id": 1,
            "title": "Mass Assignment",
            "description": "Elevate your privileges by injecting an unexpected parameter into a JSON payload.",
            "hint": "POST to /api/labs/api_sec/mass_assignment with {\"username\": \"test\", \"is_admin\": true}",
            "difficulty": "Intermediate",
            "xp": 150,
            "flag": "flag{api_mass_assignment}",
            "badge": "🏆 Mass Assigner"
        },
        {
            "id": 2,
            "title": "HTTP Parameter Pollution (HPP)",
            "description": "Bypass a security filter by supplying duplicate parameters.",
            "hint": "GET /api/labs/api_sec/hpp?id=safe&id=malicious (Different parsers process duplicate keys differently).",
            "difficulty": "Advanced",
            "xp": 200,
            "flag": "flag{api_hpp_bypass}",
            "badge": "🏆 Polluter"
        },
        {
            "id": 3,
            "title": "Improper Asset Management",
            "description": "Find and exploit a deprecated, insecure API version.",
            "hint": "Send a GET request to /api/v1/labs/api_sec/deprecated instead of the main API.",
            "difficulty": "Intermediate",
            "xp": 150,
            "flag": "flag{api_deprecated_v1}",
            "badge": "🏆 Archaeologist"
        }
    ]
}
