# Security Policy & Architecture Guide
**Course Code**: 20CYS401 — Secure Software Engineering  
**System**: Online Book Review and Recommendation Platform

---

## 1. Security Architecture Principles

This project adheres to the principle of **Defense in Depth**, enforcing security checks across multiple tiers:

```
[ Client Request ]
       │
       ▼
1. Transport & Network Security (HTTPS headers: CSP, X-Frame-Options, nosniff)
       │
       ▼
2. Presentation & Transport Filtering (Synchronizer Token CSRF verification)
       │
       ▼
3. Authentication Gate (Flask-Login HttpOnly session token validation)
       │
       ▼
4. Route-Level Role Authorization (@admin_required decorator)
       │
       ▼
5. Service-Level Object Authorization (review.is_owned_by(user_id) verification)
       │
       ▼
6. Data Access Security (SQLAlchemy ORM parameterized query construction)
       │
       ▼
7. Audit & Accountability (Tamper-evident AuditLog recording with secret scrubbing)
```

---

## 2. Implemented Security Controls

### CTRL-01: Authentication & Session Management
- Passwords are encrypted using **bcrypt** with a salt work factor of 12 rounds.
- Server-side signed session cookies are issued with `HttpOnly=True` and `SameSite=Lax`.
- Session invalidation is performed explicitly upon logout using `session.clear()`.

### CTRL-02: Object-Level Authorization (IDOR Defense)
- Review modification and deletion requests enforce `review.is_owned_by(current_user.id)` in `ReviewService`.
- Prevents horizontal privilege escalation where an attacker modifies another user's review by changing the request payload or URL identifier.

### CTRL-03: Cross-Site Scripting (XSS) Prevention
- Jinja2 template engine autoescaping is active on all `.html` templates.
- User review text and inputs are sanitized to strip harmful ASCII control sequences and null bytes.

### CTRL-04: Robust Input Validation
- Book ratings are strictly validated as integers between 1 and 5. Out-of-bounds ratings are rejected before database querying.
- Text content is subjected to length boundaries (5 to 2000 characters).

### CTRL-05: SQL Injection Prevention
- All database queries are executed via **SQLAlchemy ORM** parameterized query abstractions (`filter()`, `ilike()`).
- No string formatting, string concatenation, or raw SQL queries exist in the codebase.

### CTRL-06: Role-Based Access Control (RBAC)
- All `/admin/*` routes are protected by the `@admin_required` decorator, rejecting non-admin sessions with HTTP 403 Forbidden.

### CTRL-07: Information Disclosure & Error Handling
- Custom error handlers intercept HTTP 400, 403, 404, and 500 responses, returning user-friendly pages without exposing backend stack traces, framework versions, or internal file paths.

### CTRL-08: Tamper-Evident Audit Logging
- Security-critical events (`LOGIN_SUCCESS`, `UNAUTHORIZED_REVIEW_EDIT_ATTEMPT`, `REVIEW_HIDDEN`, `BOOK_CREATED`) are logged with actor details, timestamps, client IP, action type, and status.
- Sensitive credentials (e.g. passwords) are scrubbed automatically prior to persistence.

### CTRL-09: HTTP Response Security Headers
- The following security headers are appended to all HTTP responses:
  - `X-Frame-Options: DENY`
  - `X-Content-Type-Options: nosniff`
  - `Referrer-Policy: strict-origin-when-cross-origin`
  - `Content-Security-Policy: default-src 'self'; style-src 'self' 'unsafe-inline'; font-src 'self';`

### CTRL-10: Hardened Container Runtime
- Multi-stage Docker container runs under an unprivileged user (`UID 10001:10001`).
- Kubernetes manifest drops all capabilities and prohibits root escalation.
