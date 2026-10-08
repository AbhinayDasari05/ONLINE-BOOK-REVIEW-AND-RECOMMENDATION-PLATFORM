# Online Book Review and Recommendation Platform
## Secure Software Engineering End Semester Laboratory Examination
**Course Code**: 20CYS401  
**Degree / Branch**: B.Tech CSE — Cybersecurity  

---

### System Overview
A secure web platform where users can discover and review books, maintain private reading lists, and submit ratings. Administrators manage the book catalog and moderate inappropriate content. Built with defense-in-depth principles: server-side authentication, strict object-level authorization, input validation, and audit logging.

### Security Focus
- Authentication & Session Hardening (Bcrypt, HttpOnly, SameSite)
- Server-Side Object-Level Authorization (IDOR protection on reviews)
- Review Manipulation Prevention (1 rating per user per book)
- Strict Input Validation & Output Encoding (Anti-XSS, Anti-SQLi)
- Administrator Privilege Control (RBAC, tamper-evident audit logging)
