# Phase 13: Containerization & Kubernetes Deployment
**Course Code**: 20CYS401 — Secure Software Engineering  
**Project**: Online Book Review and Recommendation Platform  

---

## 1. Hardened Dockerfile Architecture

The container runtime uses a multi-stage build pattern (`docker/Dockerfile`):
- **Base Image**: `python:3.11-slim`
- **Builder Stage**: Compiles dependencies in isolated cache layer.
- **Runtime Stage**:
  - Unprivileged non-root user `appuser` (`UID 10001:10001`).
  - Read-write restricted instance folder for SQLite.
  - Active healthcheck probe inspecting `http://localhost:5000/health`.
  - Zero hardcoded secrets or environment credentials in image layers.

---

## 2. Local Docker Compose Verification

- **Compose Configuration**: `docker-compose.yml`
- **Port Mapping**: `5050:5000` (mapped to host port 5050 to prevent macOS AirPlay port 5000 conflicts).
- **Health Verification**:
  ```bash
  curl http://localhost:5050/health
  ```
  Returns:
  ```json
  {"database":"connected","service":"secure-book-review-platform","status":"healthy"}
  ```

---

## 3. Kubernetes Manifests

Located in `k8s/`:
- `namespace.yaml`: Isolated namespace `bookplatform`.
- `deployment.yaml`: Enforces `runAsNonRoot: true`, `readOnlyRootFilesystem: false`, CPU/Memory resource bounds, and liveness/readiness HTTP probes on `/health`.
- `service.yaml`: ClusterIP internal service exposure.
