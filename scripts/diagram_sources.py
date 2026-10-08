# Mermaid Diagrams for Online Book Review and Recommendation Platform
# Course Code: 20CYS401 — Secure Software Engineering

DIAGRAMS = {
    "01_use_case_diagram": """
graph TD
    USER((USER))
    ADMIN((ADMINISTRATOR))
    ANON((Anonymous Visitor))

    subgraph "Online Book Review Platform System Boundary"
        UC01[Register Account]
        UC02[Login / Session Auth]
        UC03[Logout / Invalidate Session]
        UC04[Search Books Parameterized]
        UC05[View Book Details & Aggregated Ratings]
        UC06[Submit Rating 1-5 Stars]
        UC07[Write Book Review]
        UC08[Edit Own Review CTRL-02]
        UC09[Delete Own Review CTRL-02]
        UC10[Maintain Reading Shelf]
        UC11[Admin: Manage Book Catalog]
        UC12[Admin: Moderate Reviews]
        UC13[Admin: View Security Audit Logs]
    end

    ANON --> UC01
    ANON --> UC02
    ANON --> UC04
    ANON --> UC05

    USER --> UC02
    USER --> UC03
    USER --> UC04
    USER --> UC05
    USER --> UC06
    USER --> UC07
    USER --> UC08
    USER --> UC09
    USER --> UC10

    ADMIN --> UC03
    ADMIN --> UC04
    ADMIN --> UC05
    ADMIN --> UC11
    ADMIN --> UC12
    ADMIN --> UC13

    UC08 -.->|extends| UC07
    UC09 -.->|extends| UC07
    UC12 -.->|includes| UC13
""",

    "02_er_diagram": """
erDiagram
    USERS {
        int id PK
        string username UK
        string email UK
        string password_hash
        boolean is_admin
        datetime created_at
    }

    BOOKS {
        int id PK
        string title
        string author
        string genre
        string isbn UK
        text description
        int publication_year
        datetime created_at
    }

    REVIEWS {
        int id PK
        int book_id FK
        int user_id FK
        int rating
        text content
        boolean is_moderated
        string moderation_reason
        int moderated_by FK
        datetime created_at
        datetime updated_at
    }

    READING_LIST_ITEMS {
        int id PK
        int user_id FK
        int book_id FK
        string status
        datetime added_at
        datetime updated_at
    }

    AUDIT_LOGS {
        int id PK
        datetime timestamp
        int user_id FK
        string username
        string action
        string resource_type
        string resource_id
        string ip_address
        string status
        text details
    }

    USERS ||--o{ REVIEWS : "authors"
    USERS ||--o{ READING_LIST_ITEMS : "maintains"
    USERS ||--o{ AUDIT_LOGS : "generates"
    BOOKS ||--o{ REVIEWS : "has"
    BOOKS ||--o{ READING_LIST_ITEMS : "included in"
    USERS ||--o{ REVIEWS : "moderates"
""",

    "03_dfd_level_0": """
graph LR
    E1((USER Actor))
    E2((ADMINISTRATOR Actor))
    E3((Web Browser Client))

    subgraph "Online Book Review Platform [Trust Boundary]"
        P0[Book Review Platform System Process]
        D01[(D01: SQLite Database Instance)]
    end

    E1 -->|Search, Rate, Review, Shelf Ops| E3
    E2 -->|Manage Catalog, Moderate, View Audits| E3
    E3 -->|HTTPS Requests + CSRF Tokens| P0
    P0 -->|HTML / JSON Responses + Security Headers| E3
    P0 -->|Parameterized Queries / Read / Write| D01
    D01 -->|Persisted Entities| P0
""",

    "04_dfd_level_1": """
graph TD
    E1((USER))
    E2((ADMINISTRATOR))

    subgraph "Secure Application Trust Boundary"
        P01[P1: Authenticate & Session Management]
        P02[P2: Search & Filter Books]
        P03[P3: Book Details & Rating Aggregator]
        P04[P4: Review Mutations & IDOR Verification]
        P05[P5: Personal Reading Shelf Manager]
        P06[P6: Admin Catalog & Moderation Gateway]
        P07[P7: Tamper-Evident Audit Logging Subsystem]

        D01[(D1: Users Store)]
        D02[(D2: Books Catalog Store)]
        D03[(D3: Reviews & Ratings Store)]
        D04[(D4: Reading Lists Store)]
        D05[(D5: Audit Logs Store)]
    end

    E1 -->|Credentials| P01
    P01 -->|Signed Session Cookie| E1
    P01 -->|Verify Bcrypt Hash| D01
    P01 -->|Log Auth Event| P07

    E1 -->|Search Terms| P02
    P02 -->|Parameterized ORM Query| D02
    D02 -->|Matching Books| P02

    P03 -->|Render Details & Reviews| E1
    P03 -->|Read| D02
    P03 -->|Read| D03

    E1 -->|Rating 1-5 & Review Content| P04
    P04 -->|Verify Ownership CTRL-02| D01
    P04 -->|Persist Review| D03
    P04 -->|Log Review Event| P07

    E1 -->|Shelf Operations| P05
    P05 -->|Verify Ownership| D01
    P05 -->|Update Shelf| D04
    P05 -->|Log Shelf Event| P07

    E2 -->|Admin Requests| P06
    P06 -->|Verify @admin_required RBAC| D01
    P06 -->|CRUD Catalog| D02
    P06 -->|Moderate Review| D03
    P06 -->|Log Admin Event| P07

    P07 -->|Sanitized Audit Entry| D05
""",

    "05_trust_boundary_diagram": """
graph TD
    subgraph "External Untrusted Zone"
        B1[Web Browser Client]
        AT1[Threat Actor / Attacker]
    end

    subgraph "Edge & Network Perimeter"
        SEC_HDR[Security Headers Filter: CSP, X-Frame-Options, nosniff]
        CSRF_GATE[CSRF Token Verification Gate]
    end

    subgraph "Application Trust Boundary"
        subgraph "Authentication & Session Tier"
            AUTH[Flask-Login HttpOnly Cookie Validator + Bcrypt]
        end
        subgraph "Authorization Tier"
            RBAC[Role-Based Access Control: @admin_required]
            OBJ_AUTH[Object-Level Ownership Validator: review.is_owned_by]
        end
        subgraph "Business Services Tier"
            SERVICES[UserService, BookService, SearchService, ReviewService]
        end
        subgraph "Data Access Tier"
            ORM[SQLAlchemy ORM Parameterized Bindings]
        end
        subgraph "Audit Subsystem"
            AUDIT[Tamper-Evident Audit Logger with Credential Scrubbing]
        end
    end

    subgraph "Storage Trust Boundary"
        DB[(Encrypted / Non-Root Local SQLite Database)]
    end

    B1 -->|HTTPS Requests| SEC_HDR
    AT1 -.->|Attempted IDOR, SQLi, XSS| SEC_HDR
    SEC_HDR --> CSRF_GATE
    CSRF_GATE --> AUTH
    AUTH --> RBAC
    AUTH --> OBJ_AUTH
    RBAC --> SERVICES
    OBJ_AUTH --> SERVICES
    SERVICES --> ORM
    SERVICES --> AUDIT
    ORM --> DB
    AUDIT --> DB
""",

    "06_system_architecture": """
graph TD
    CLIENT[Browser Client / Web Browser]

    subgraph "Presentation Layer"
        BP_AUTH[auth.py Blueprint]
        BP_CAT[catalog.py Blueprint]
        BP_REV[reviews.py Blueprint]
        BP_RL[reading_list.py Blueprint]
        BP_ADM[admin.py Blueprint]
        BP_HLTH[health.py Blueprint]
        TEMPLATES[Jinja2 Server-Rendered Templates + Autoescaping]
    end

    subgraph "Security Cross-Cutting Layer"
        SEC_COOKIES[HttpOnly & SameSite Session Cookies]
        CSRF_PROT[Flask-WTF Synchronizer CSRF Protection]
        RBAC_DEC[@admin_required Server-Side Decorator]
        SEC_HEADERS[Security Headers Middleware CSP, X-Frame-Options]
        AUDIT_SYS[Tamper-Evident Audit Event Logger]
    end

    subgraph "Service Layer Business Logic"
        SRV_USER[UserService]
        SRV_BOOK[BookService]
        SRV_SRCH[SearchService]
        SRV_REV[ReviewService with CTRL-02 Ownership Checks]
        SRV_RL[ReadingListService]
    end

    subgraph "Data Access & Persistence Layer"
        ORM_MODELS[SQLAlchemy Models: User, Book, Review, ReadingListItem, AuditLog]
        SQLITE_DB[(SQLite Database instance/book_platform.db)]
    end

    CLIENT --> BP_AUTH
    CLIENT --> BP_CAT
    CLIENT --> BP_REV
    CLIENT --> BP_RL
    CLIENT --> BP_ADM
    CLIENT --> BP_HLTH

    BP_AUTH --> SEC_COOKIES
    BP_ADM --> RBAC_DEC
    BP_REV --> CSRF_PROT
    BP_RL --> CSRF_PROT

    BP_AUTH --> SRV_USER
    BP_CAT --> SRV_SRCH
    BP_CAT --> SRV_BOOK
    BP_REV --> SRV_REV
    BP_RL --> SRV_RL
    BP_ADM --> SRV_BOOK
    BP_ADM --> SRV_REV

    SRV_USER --> ORM_MODELS
    SRV_BOOK --> ORM_MODELS
    SRV_SRCH --> ORM_MODELS
    SRV_REV --> ORM_MODELS
    SRV_RL --> ORM_MODELS
    SRV_REV --> AUDIT_SYS
    SRV_BOOK --> AUDIT_SYS

    AUDIT_SYS --> ORM_MODELS
    ORM_MODELS --> SQLITE_DB
""",

    "07_attack_tree_atk01": """
graph TD
    ROOT[ATK-01: Unauthorized Modification of Book Review and Rating]

    P1[Path 1: Insecure Direct Object Reference IDOR]
    P2[Path 2: Cross-Site Request Forgery CSRF]
    P3[Path 3: Account Takeover Credential Abuse]
    P4[Path 4: Database Injection SQLi]

    ROOT --> P1
    ROOT --> P2
    ROOT --> P3
    ROOT --> P4

    P1 --> I1[Discover Review ID of Target Author]
    P1 --> I2[Send HTTP POST to /reviews/ID/edit]
    P1 --> I3[Server Omits Ownership Check]

    P2 --> C1[Target User Has Active Valid Session]
    P2 --> C2[Target Visits Malicious Third-Party Page]
    P2 --> C3[Server Accepts Request Without CSRF Token]

    P3 --> A1[Credential Stuffing / Password Brute Force]
    P3 --> A2[Session Hijacking via Stored XSS]

    P4 --> S1[Find Raw String Concatenated Query]
    P4 --> S2[Execute Arbitrary UPDATE/DELETE Statements]

    classDef mitigated fill:#d4edda,stroke:#28a745,stroke-width:2px;
    classDef blocked fill:#f8d7da,stroke:#dc3545,stroke-width:2px;

    class I3,C3,A1,A2,S1,S2 blocked;
    class P1,P2,P3,P4 mitigated;
""",

    "08_deployment_architecture": """
graph LR
    subgraph "Client Environment"
        CLIENT_BROWSER[Web Browser on Port 5050]
    end

    subgraph "Docker Container runtime UID 10001"
        WEB_APP[Flask 3.1 Gunicorn/Werkzeug Service]
        HEALTH_EP[Healthcheck Probe /health]
        SQLITE_VOL[(Volume Mounted SQLite instance/)]
    end

    subgraph "Kubernetes Cluster bookplatform Namespace"
        K8S_DEP[Deployment Replicas: 2 runAsNonRoot: true]
        K8S_SVC[Service ClusterIP Port 80:5000]
        K8S_CM[ConfigMap bookplatform-config]
        K8S_SEC[Secret bookplatform-secret]
        K8S_PROBES[Liveness & Readiness Probes /health]
    end

    CLIENT_BROWSER -->|HTTP Port 5050| WEB_APP
    WEB_APP --> HEALTH_EP
    WEB_APP --> SQLITE_VOL

    K8S_DEP --> K8S_SVC
    K8S_DEP --> K8S_CM
    K8S_DEP --> K8S_SEC
    K8S_DEP --> K8S_PROBES
"""
}
