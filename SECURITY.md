# Security Policy

## Course Code: 20CYS401 — Secure Software Engineering

### Supported Versions
| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

### Core Security Principles Implemented
1. **Rule A (Review Ownership)**: A user can ONLY edit/delete their own reviews. Server-side object authorization is strictly enforced.
2. **Rule B (Admin RBAC)**: Only verified administrators can create/modify books and moderate reviews.
3. **Rule C (CSRF Protection)**: All state-changing POST/PUT/DELETE actions must carry valid CSRF protection.
4. **Rule D (Input Validation)**: All client input is validated, stripped of forbidden sequences, and length-checked.
5. **Rule E (Password Security)**: Passwords are salted and hashed using Bcrypt before storage.
6. **Rule F (Zero Committed Secrets)**: No credentials, API tokens, or session keys in repository.
7. **Rule G (Server-Side Checks)**: All business logic and security policies reside on the server.
8. **Rule H (Log Sanitization)**: Passwords and sensitive tokens are scrubbed from log pipelines.
9. **Rule I (Generic Error Pages)**: No stack traces or database schema errors exposed to clients.
10. **Rule J (Secure Defaults)**: Production deployments use HTTPS, hardened security headers, and isolated roles.
