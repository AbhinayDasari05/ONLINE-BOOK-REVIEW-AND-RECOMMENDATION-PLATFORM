# Phase 10: Jira Board & Workflow Execution Evidence
**Course Code**: 20CYS401 — Secure Software Engineering  
**Project**: Online Book Review and Recommendation Platform  

---

## 1. Exact Board Columns & Workflow States

The project board implements the four-column agile engineering workflow:

```
[ TO DO ] ──► [ IN PROGRESS ] ──► [ TESTING ] ──► [ DONE ]
```

### Transition Criteria:
1. **TO DO → IN PROGRESS**: Moved only when development/implementation starts.
2. **IN PROGRESS → TESTING**: Moved only after core code is written and unit verification is ready.
3. **TESTING → DONE**: Moved only after:
   - Automated tests pass.
   - Acceptance criteria are fully verified.
   - Security verification (authorization, input validation, SAST) passes.
   - Evidence is recorded.

---

## 2. Story Lifecycle Trajectory & Real Verification

| Story Key | Summary | Story Points | State History | Final Status | Verification Test / Control |
|---|---|---|---|---|---|
| **OBRRP-5** | Registration | 3 SP | TO DO → IN PROGRESS → TESTING → DONE | **DONE** | `test_unit_auth.py`, `test_integration_auth.py` (CTRL-01) |
| **OBRRP-6** | Secure Login | 5 SP | TO DO → IN PROGRESS → TESTING → DONE | **DONE** | `test_unit_auth.py`, `test_integration_auth.py` (CTRL-01) |
| **OBRRP-7** | Secure Logout & Sessions | 3 SP | TO DO → IN PROGRESS → TESTING → DONE | **DONE** | `test_integration_auth.py::test_login_and_logout_session_invalidation` |
| **OBRRP-8** | Search Books | 5 SP | TO DO → IN PROGRESS → TESTING → DONE | **DONE** | `test_unit_search.py`, `test_fuzzing.py` (CTRL-05) |
| **OBRRP-9** | View Book Details | 3 SP | TO DO → IN PROGRESS → TESTING → DONE | **DONE** | `test_fuzzing.py::test_invalid_resource_ids`, `test_e2e_workflow.py` |
| **OBRRP-10** | Rate & Review Books | 8 SP | TO DO → IN PROGRESS → TESTING → DONE | **DONE** | `test_unit_validation.py`, `test_integration_reviews.py` (CTRL-03, CTRL-04) |
| **OBRRP-11** | Edit/Delete Own Reviews | 5 SP | TO DO → IN PROGRESS → TESTING → DONE | **DONE** | `test_authorization.py::test_user_b_cannot_edit_user_a_review` (CTRL-02) |
| **OBRRP-12** | Reading List | 5 SP | TO DO → IN PROGRESS → TESTING → DONE | **DONE** | `test_e2e_workflow.py`, `test_authorization.py` (CTRL-02) |
| **OBRRP-13** | Admin Book Management | 5 SP | TO DO → IN PROGRESS → TESTING → DONE | **DONE** | `test_authorization.py::test_normal_user_denied_admin_routes` (CTRL-06) |
| **OBRRP-14** | Review Moderation | 5 SP | TO DO → IN PROGRESS → TESTING → DONE | **DONE** | `test_authorization.py::test_admin_user_granted_admin_routes` (CTRL-06) |
| **OBRRP-15** | Secure Authorization & IDOR | 8 SP | TO DO → IN PROGRESS → TESTING → DONE | **DONE** | `test_authorization.py`, `test_idor_vulnerability_proof.py` (CTRL-02) |
| **OBRRP-16** | Audit Logging | 3 SP | TO DO → IN PROGRESS → TESTING → DONE | **DONE** | `app/core/audit.py`, `/admin/moderation` audit log display (CTRL-08) |
| **OBRRP-17** | Security & Auth Testing | 5 SP | TO DO → IN PROGRESS → TESTING → DONE | **DONE** | 23/23 tests passing + Bandit SAST scan (0 High, 0 Medium) |
| **OBRRP-18** | CI/CD Pipeline | 5 SP | TO DO → IN PROGRESS → TESTING → DONE | **DONE** | `.github/workflows/ci.yml` validation |
| **OBRRP-19** | Docker & K8s Deployment | 8 SP | TO DO → IN PROGRESS → TESTING → DONE | **DONE** | Container runtime verified on Port 5050 with UID 10001 (CTRL-10) |

---

## 3. Current Board Snapshot

- **TO DO**: 0 stories (0 SP)
- **IN PROGRESS**: 0 stories (0 SP)
- **TESTING**: 0 stories (0 SP)
- **DONE**: 15 stories (76 SP)
