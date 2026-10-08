# Phase 6: UI Screens and Workflow Documentation
**Course Code**: 20CYS401 | **Project**: Online Book Review and Recommendation Platform

---

## 6.1 Overview of Connected UI Screens

The application features 6 core server-rendered screens implemented via Jinja2 templates in `app/templates/`, styled uniformly with responsive custom CSS in `app/static/css/style.css`.

All forms enforce strict CSRF protection via hidden token validation (`Flask-WTF`), input sanitization on form submission, and contextual auto-escaping across all variable interpolations.

---

## 6.2 Screen Inventory and Navigation Mapping

```mermaid
graph TD
    S1[Screen 1: Login & Register\n/login, /register]
    S2[Screen 2: Book Catalog & Search\n/]
    S3[Screen 3: Book Details & Reviews\n/books/{id}]
    S4[Screen 4: Personal Reading List\n/my-shelf]
    S5[Screen 5: Admin Catalog Management\n/admin/books]
    S6[Screen 6: Admin Review Moderation & Audit\n/admin/moderation]

    S1 -->|Authenticate| S2
    S2 -->|Select Book| S3
    S3 -->|Add to Shelf| S4
    S3 -->|Submit Review| S3
    S2 -->|Admin Link| S5
    S5 -->|Moderation Tab| S6
    S4 -->|Browse More| S2
```

---

## 6.3 Detailed Screen Specifications

### Screen 1: Authentication (`/login`, `/register`)
- **Template**: `app/templates/auth/login_register.html`
- **Associated Route**: `app/routes/auth.py`
- **Functionality**:
  - Combined tabbed interface for User Registration and User Login.
  - Client and server-side validation for minimum password length (≥8 chars) and email structure.
  - CSRF protection embedded in each independent POST form.
  - Safe error messaging preventing user enumeration.

### Screen 2: Catalog & Search (`/`)
- **Template**: `app/templates/catalog/search.html`
- **Associated Route**: `app/routes/catalog.py`
- **Functionality**:
  - Filter by keyword (Title/Author), specific Genre dropdown, or sort order.
  - Book card grid displaying cover placeholders, average ratings (1–5 stars), and review counts.
  - Parameterized ORM queries (`SearchService`) eliminating SQL injection risks.

### Screen 3: Book Details, Ratings & Reviews (`/books/<int:book_id>`)
- **Template**: `app/templates/catalog/detail.html`
- **Associated Route**: `app/routes/catalog.py`, `app/routes/reviews.py`, `app/routes/reading_list.py`
- **Functionality**:
  - Complete metadata display: ISBN, publication year, author, description.
  - Shelf selector widget: Quick-add book to "Want to Read", "Currently Reading", or "Finished".
  - Review submission form (1–5 star radio/select, 5–2000 character review body).
  - List of community reviews (excluding reviews hidden by moderation).
  - Owner-exclusive Edit and Delete buttons on reviews authored by the currently logged-in user.

### Screen 4: Personal Reading List (`/my-shelf`)
- **Template**: `app/templates/reading_list/index.html`
- **Associated Route**: `app/routes/reading_list.py`
- **Functionality**:
  - Grouped view of user's personal shelf items.
  - Inline dropdown to update reading status without leaving the page.
  - One-click removal from shelf.
  - Filtered strictly by `current_user.id` enforcing private access boundaries.

### Screen 5: Administrator Catalog Management (`/admin/books`)
- **Template**: `app/templates/admin/books.html`
- **Associated Route**: `app/routes/admin.py`
- **Functionality**:
  - Guarded by `@admin_required` decorator (RBAC).
  - Form to add new books to the global catalog (Title, Author, Genre, ISBN, Description, Year).
  - Tabular list of existing books with inline edit and delete actions.
  - Audit logging of all catalog mutations (`BOOK_CREATED`, `BOOK_UPDATED`, `BOOK_DELETED`).

### Screen 6: Administrator Review Moderation & Audit Logs (`/admin/moderation`)
- **Template**: `app/templates/admin/moderation.html`
- **Associated Route**: `app/routes/admin.py`
- **Functionality**:
  - Complete moderation queue showing all user reviews across all books.
  - "Hide Review" action requiring a mandatory moderation reason (e.g., spam, abusive language).
  - "Restore Review" action to unhide previously moderated reviews.
  - Real-time audit log table tracking the last 50 security and administrative actions in the platform.
