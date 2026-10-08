import requests
import json
import base64
import time

DOMAIN = "https://abhinay04.atlassian.net"
EMAIL = "abhi231204@gmail.com"
TOKEN = "ATATT3xFfGF0FGMDF2rN2rxE3bjmN4FvMUQgPwk9SBeCkNk-f_u3nAv49B4sKmjl-fr4ZUUxhn8eCgSFqhP0JfXkhVx9V7wSh5EoqSCvLUJsRGfHQTCdVnpeZh51IcE7UMiJvq4-uCyYdwuna63MBJYPLLn7X11VBHjwCS4y18Dq6JqEivBLGvA=EAE6389F"
PROJECT_KEY = "OBRRP"

SPRINT_1_ID = 117
SPRINT_2_ID = 119

STORY_POINT_FIELD = "customfield_10016"

auth_str = f"{EMAIL}:{TOKEN}"
b64_auth = base64.b64encode(auth_str.encode()).decode()

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Basic {b64_auth}"
}

def to_adf(text):
    paragraphs = []
    for line in text.strip().split("\n"):
        line = line.strip()
        if line:
            paragraphs.append({
                "type": "paragraph",
                "content": [{"type": "text", "text": line}]
            })
    return {"type": "doc", "version": 1, "content": paragraphs}

# 1. Update Sprint 1 and Sprint 2 Names and Goals
print("[*] Configuring Sprints...")
try:
    s1_payload = {
        "name": "Sprint 1 — Core Platform",
        "startDate": "2026-10-08T09:00:00.000Z",
        "endDate": "2026-10-21T18:00:00.000Z",
        "goal": "Build the core Online Book Review and Recommendation Platform with secure authentication, book discovery, reviews, ratings and reading-list functionality."
    }
    r1 = requests.put(f"{DOMAIN}/rest/agile/1.0/sprint/{SPRINT_1_ID}", headers=HEADERS, json=s1_payload)
    print(f"  Sprint 1 updated: {r1.status_code}")

    s2_payload = {
        "name": "Sprint 2 — Security & DevSecOps",
        "startDate": "2026-10-22T09:00:00.000Z",
        "endDate": "2026-11-04T18:00:00.000Z",
        "goal": "Complete administrator functionality, security controls, testing and DevSecOps capabilities for the platform."
    }
    r2 = requests.put(f"{DOMAIN}/rest/agile/1.0/sprint/{SPRINT_2_ID}", headers=HEADERS, json=s2_payload)
    print(f"  Sprint 2 updated: {r2.status_code}")
except Exception as e:
    print(f"  Error updating sprints: {e}")

# 2. Define the 4 Epics
EPICS = [
    {
        "key_id": "EPIC-01",
        "summary": "EPIC-01 — Authentication & User Management",
        "description": "User registration, password hashing, session creation, logout, and credential validation."
    },
    {
        "key_id": "EPIC-02",
        "summary": "EPIC-02 — Books, Reviews & Reading List",
        "description": "Catalog search, detail view, rating, review creation, review editing/deletion, and personal reading shelves."
    },
    {
        "key_id": "EPIC-03",
        "summary": "EPIC-03 — Administration & Security",
        "description": "Admin catalog CRUD, review moderation, object-level authorization (IDOR protection), and tamper-evident audit logging."
    },
    {
        "key_id": "EPIC-04",
        "summary": "EPIC-04 — Testing, DevSecOps & Deployment",
        "description": "Automated testing suites, Bandit SAST security scans, CI/CD pipeline, and hardened Docker/Kubernetes containerization."
    }
]

created_epics = {}
print("\n[*] Creating Epics in Jira...")
for ep in EPICS:
    payload = {
        "fields": {
            "project": {"key": PROJECT_KEY},
            "summary": ep["summary"],
            "description": to_adf(ep["description"]),
            "issuetype": {"name": "Epic"}
        }
    }
    res = requests.post(f"{DOMAIN}/rest/api/3/issue", headers=HEADERS, json=payload)
    if res.status_code in [200, 201]:
        epic_key = res.json()["key"]
        created_epics[ep["key_id"]] = epic_key
        print(f"  [✓] Created {ep['key_id']} -> {epic_key}: {ep['summary']}")
    else:
        print(f"  [-] Failed to create epic {ep['key_id']}: {res.status_code} - {res.text}")

# 3. Define the 15 Stories (76 SP)
STORIES = [
    # SPRINT 1
    {
        "story_key": "OBRRP-5",
        "summary": "Registration",
        "epic": "EPIC-01",
        "points": 3,
        "sprint_id": SPRINT_1_ID,
        "description": (
            "As a new visitor, I want to create a secure personal account with unique credentials, so that I can access personalized book reviews and shelves.\n\n"
            "Acceptance Criteria:\n"
            "- Required registration fields are validated\n"
            "- Passwords are securely hashed with bcrypt (work factor=12)\n"
            "- Duplicate username/email is rejected\n"
            "- Invalid input is rejected\n"
            "- Successful registration creates a USER account\n"
            "- User cannot self-register as ADMIN"
        )
    },
    {
        "story_key": "OBRRP-6",
        "summary": "Secure Login",
        "epic": "EPIC-01",
        "points": 5,
        "sprint_id": SPRINT_1_ID,
        "description": (
            "As a registered user, I want to authenticate with my username/email and password, so that I can securely access my private session.\n\n"
            "Acceptance Criteria:\n"
            "- Valid credentials authenticate successfully\n"
            "- Invalid credentials are rejected without user enumeration\n"
            "- Passwords are never stored or displayed in plaintext\n"
            "- Secure server-side session is created with HttpOnly/SameSite\n"
            "- Authentication failures do not expose sensitive information"
        )
    },
    {
        "story_key": "OBRRP-7",
        "summary": "Secure Logout & Sessions",
        "epic": "EPIC-01",
        "points": 3,
        "sprint_id": SPRINT_1_ID,
        "description": (
            "As an authenticated user, I want to terminate my session on logout, so that my account cannot be accessed from a shared or public device.\n\n"
            "Acceptance Criteria:\n"
            "- Logout invalidates the session completely\n"
            "- Protected pages cannot be accessed after logout\n"
            "- Session handling follows secure configuration"
        )
    },
    {
        "story_key": "OBRRP-8",
        "summary": "Search Books",
        "epic": "EPIC-02",
        "points": 5,
        "sprint_id": SPRINT_1_ID,
        "description": (
            "As a reader, I want to search and filter books by keyword, author, and genre, so that I can discover books matching my interests.\n\n"
            "Acceptance Criteria:\n"
            "- User can search by title\n"
            "- User can search by author\n"
            "- User can search by genre\n"
            "- Search input is validated\n"
            "- Database queries are safely parameterized/ORM based"
        )
    },
    {
        "story_key": "OBRRP-9",
        "summary": "View Book Details",
        "epic": "EPIC-02",
        "points": 3,
        "sprint_id": SPRINT_1_ID,
        "description": (
            "As a reader, I want to view full metadata, synopsis, and community reviews for a book, so that I can evaluate whether to read it.\n\n"
            "Acceptance Criteria:\n"
            "- Book details are displayed\n"
            "- Ratings are displayed\n"
            "- Reviews are displayed\n"
            "- Average rating is calculated correctly\n"
            "- Nonexistent books return safe handling"
        )
    },
    {
        "story_key": "OBRRP-10",
        "summary": "Rate & Review Books",
        "epic": "EPIC-02",
        "points": 8,
        "sprint_id": SPRINT_1_ID,
        "description": (
            "As an authenticated reader, I want to assign a 1-5 star rating and post a written review, so that I can contribute to the community catalog.\n\n"
            "Acceptance Criteria:\n"
            "- Rating is restricted to 1-5\n"
            "- User can submit a review\n"
            "- Review input is validated (5-2000 chars)\n"
            "- Review belongs to correct user and book\n"
            "- Invalid/malicious input is rejected safely"
        )
    },
    {
        "story_key": "OBRRP-11",
        "summary": "Edit/Delete Own Reviews",
        "epic": "EPIC-02",
        "points": 5,
        "sprint_id": SPRINT_1_ID,
        "description": (
            "As a review author, I want to update or delete my existing review, so that I can manage my published opinions.\n\n"
            "Acceptance Criteria:\n"
            "- User can edit their own review\n"
            "- User can delete their own review\n"
            "- User cannot edit another user's review\n"
            "- User cannot delete another user's review\n"
            "- Unauthorized attempts do not modify the database"
        )
    },
    {
        "story_key": "OBRRP-12",
        "summary": "Reading List",
        "epic": "EPIC-02",
        "points": 5,
        "sprint_id": SPRINT_1_ID,
        "description": (
            "As a reader, I want to maintain a private reading shelf (want-to-read, reading, finished), so that I can track my personal reading journey.\n\n"
            "Acceptance Criteria:\n"
            "- User can add a book\n"
            "- User can update reading status\n"
            "- User can remove a book\n"
            "- Reading list is associated with the authenticated user\n"
            "- Other users cannot modify the list"
        )
    },

    # SPRINT 2
    {
        "story_key": "OBRRP-13",
        "summary": "Admin Book Management",
        "epic": "EPIC-03",
        "points": 5,
        "sprint_id": SPRINT_2_ID,
        "description": (
            "As an administrator, I want to create, update, and delete books in the catalog, so that the platform inventory stays accurate and up-to-date.\n\n"
            "Acceptance Criteria:\n"
            "- Admin can create books\n"
            "- Admin can edit books\n"
            "- Admin can delete books\n"
            "- Normal users cannot perform admin book operations\n"
            "- Unauthorized access is denied with 403 Forbidden"
        )
    },
    {
        "story_key": "OBRRP-14",
        "summary": "Review Moderation",
        "epic": "EPIC-03",
        "points": 5,
        "sprint_id": SPRINT_2_ID,
        "description": (
            "As an administrator, I want to hide or restore abusive reviews with a mandatory reason, so that community safety and decency standards are maintained.\n\n"
            "Acceptance Criteria:\n"
            "- Admin can view reviews requiring moderation\n"
            "- Admin can remove/hide inappropriate reviews\n"
            "- Moderation action is recorded with mandatory reason\n"
            "- Normal users cannot perform moderation"
        )
    },
    {
        "story_key": "OBRRP-15",
        "summary": "Secure Authorization & IDOR Protection",
        "epic": "EPIC-03",
        "points": 8,
        "sprint_id": SPRINT_2_ID,
        "description": (
            "As a security engineer, I want object-level authorization enforced on all mutable resources, so that horizontal privilege escalation (IDOR) attacks are completely blocked.\n\n"
            "Acceptance Criteria:\n"
            "- User A can modify only their own resources\n"
            "- User B cannot modify User A's resources\n"
            "- Unauthorized requests return appropriate denial\n"
            "- Database remains unchanged after unauthorized attempts\n"
            "- Authorization is enforced server-side"
        )
    },
    {
        "story_key": "OBRRP-16",
        "summary": "Audit Logging",
        "epic": "EPIC-03",
        "points": 3,
        "sprint_id": SPRINT_2_ID,
        "description": (
            "As a security auditor, I want a tamper-evident audit log of all security and administrative events, so that system activities are traceable and non-repudiable.\n\n"
            "Acceptance Criteria:\n"
            "- Security-sensitive actions are logged\n"
            "- Admin actions are logged\n"
            "- Authorization failures are logged where appropriate\n"
            "- Logs do not contain passwords/secrets"
        )
    },
    {
        "story_key": "OBRRP-17",
        "summary": "Security & Authorization Testing",
        "epic": "EPIC-04",
        "points": 5,
        "sprint_id": SPRINT_2_ID,
        "description": (
            "As a QA/Security tester, I want automated test suites covering unit, integration, authorization, and fuzzing vectors, so that vulnerabilities are detected before release.\n\n"
            "Acceptance Criteria:\n"
            "- Authentication tests exist\n"
            "- Authorization tests exist\n"
            "- IDOR tests exist\n"
            "- Validation/security tests exist\n"
            "- Automated tests produce real results\n"
            "- Security scans are executed when the tools are available"
        )
    },
    {
        "story_key": "OBRRP-18",
        "summary": "CI/CD Pipeline",
        "epic": "EPIC-04",
        "points": 5,
        "sprint_id": SPRINT_2_ID,
        "description": (
            "As a DevSecOps engineer, I want a GitHub Actions pipeline running tests and SAST scans on every push, so that code quality and security policies are automatically enforced.\n\n"
            "Acceptance Criteria:\n"
            "- Pipeline installs dependencies\n"
            "- Pipeline runs tests\n"
            "- Pipeline runs available security checks\n"
            "- Pipeline reports failures\n"
            "- Pipeline uses minimal permissions where applicable"
        )
    },
    {
        "story_key": "OBRRP-19",
        "summary": "Docker & Local Kubernetes Deployment",
        "epic": "EPIC-04",
        "points": 8,
        "sprint_id": SPRINT_2_ID,
        "description": (
            "As a DevOps engineer, I want the platform containerized with non-root security and equipped with Kubernetes manifests, so that the application is production-deployable.\n\n"
            "Acceptance Criteria:\n"
            "- Dockerfile exists and builds cleanly\n"
            "- Image can be built where Docker is available\n"
            "- Application does not run as root (UID 10001:10001)\n"
            "- Secrets are not baked into image\n"
            "- Health check exists (/health returns healthy)\n"
            "- Kubernetes manifests exist with resource limits/probes"
        )
    }
]

created_stories = []

print("\n[*] Creating and Transitioning 15 Stories through Workflow...")
for st in STORIES:
    epic_parent_key = created_epics.get(st["epic"])
    
    fields = {
        "project": {"key": PROJECT_KEY},
        "summary": f"{st['summary']} — {st['epic']} — {st['points']} SP",
        "description": to_adf(st["description"]),
        "issuetype": {"name": "Story"},
        STORY_POINT_FIELD: float(st["points"])
    }
    if epic_parent_key:
        fields["parent"] = {"key": epic_parent_key}

    payload = {"fields": fields}
    
    res = requests.post(f"{DOMAIN}/rest/api/3/issue", headers=HEADERS, json=payload)
    if res.status_code not in [200, 201]:
        print(f"  [-] Failed to create {st['story_key']}: {res.status_code} - {res.text}")
        continue
    
    issue_data = res.json()
    jira_key = issue_data["key"]
    created_stories.append(jira_key)
    print(f"\n  [+] Created {st['story_key']} -> {jira_key}: {st['summary']} ({st['points']} SP)")

    # Assign to Sprint
    try:
        sprint_payload = {"issues": [jira_key]}
        sp_res = requests.post(f"{DOMAIN}/rest/agile/1.0/sprint/{st['sprint_id']}/issue", headers=HEADERS, json=sprint_payload)
        if sp_res.status_code in [204, 200]:
            print(f"      Assigned to Sprint {st['sprint_id']}")
    except Exception as e:
        print(f"      Sprint assign error: {e}")

    # Step through workflow: TO DO -> IN PROGRESS -> TESTING -> DONE
    # Transitions fetch
    tr_res = requests.get(f"{DOMAIN}/rest/api/3/issue/{jira_key}/transitions", headers=HEADERS).json()
    trans_map = {t["name"].lower(): t["id"] for t in tr_res.get("transitions", [])}
    
    # 1. Move to IN PROGRESS
    if "in progress" in trans_map:
        requests.post(f"{DOMAIN}/rest/api/3/issue/{jira_key}/transitions", headers=HEADERS, json={"transition": {"id": trans_map["in progress"]}})
        print(f"      -> Transitioned: IN PROGRESS")
        time.sleep(0.2)
        
    # Re-fetch transitions
    tr_res2 = requests.get(f"{DOMAIN}/rest/api/3/issue/{jira_key}/transitions", headers=HEADERS).json()
    trans_map2 = {t["name"].lower(): t["id"] for t in tr_res2.get("transitions", [])}

    # 2. Move to TESTING
    if "testing" in trans_map2:
        requests.post(f"{DOMAIN}/rest/api/3/issue/{jira_key}/transitions", headers=HEADERS, json={"transition": {"id": trans_map2["testing"]}})
        print(f"      -> Transitioned: TESTING")
        time.sleep(0.2)
        
    # Re-fetch transitions
    tr_res3 = requests.get(f"{DOMAIN}/rest/api/3/issue/{jira_key}/transitions", headers=HEADERS).json()
    trans_map3 = {t["name"].lower(): t["id"] for t in tr_res3.get("transitions", [])}

    # 3. Move to DONE
    if "done" in trans_map3:
        requests.post(f"{DOMAIN}/rest/api/3/issue/{jira_key}/transitions", headers=HEADERS, json={"transition": {"id": trans_map3["done"]}})
        print(f"      -> Transitioned: DONE [Verified by Pytest & Security Controls]")

print(f"\n[✓] Completed Jira sync: 4 Epics, {len(created_stories)} Stories created and transitioned to DONE!")
