# Phase 15: Logging, Monitoring, and Auditing Architecture
**Course Code**: 20CYS401 | **Project**: Online Book Review and Recommendation Platform

---

## 15.1 Logging and Auditing Implementation

The platform implements a dedicated, tamper-evident audit logging subsystem (`app/core/audit.py` and `app/models/audit_log.py`).

### Event Schema:
- `timestamp`: UTC datetime recording exact event occurrence.
- `user_id`: ID of the authenticated user (or NULL for unauthenticated actors).
- `username`: Captured actor identifier for non-repudiation.
- `action`: Standardized event code (e.g., `LOGIN_SUCCESS`, `UNAUTHORIZED_REVIEW_EDIT_ATTEMPT`, `REVIEW_HIDDEN`).
- `resource_type`: Affected domain entity (`user`, `book`, `review`, `reading_list`).
- `resource_id`: Primary key identifier of the affected entity.
- `ip_address`: Remote IP address of the client request (`request.remote_addr`).
- `status`: Outcome of the action (`SUCCESS`, `FAILED`, `DENIED`).
- `details`: Contextual metadata with sensitive credential scrubbing.

### Sensitive Data Scrubbing
`app/core/audit.py` automatically scrubs passwords, API keys, and session tokens before logging:
```python
FORBIDDEN_KEYS = {"password", "secret", "token", "key", "credential"}
```

---

## 15.2 Health Probes and Monitoring

- **Endpoint**: `/health` (`app/routes/health.py`)
- **Probe Response**: Returns HTTP 200 with JSON payload `{"status": "healthy", "database": "connected"}`.
- **Probe Logic**: Actively queries the database (`SELECT 1`) to ensure both web server responsiveness and database connectivity.
- **Kubernetes Integration**: Configured in `k8s/deployment.yaml` with both `livenessProbe` and `readinessProbe`.
