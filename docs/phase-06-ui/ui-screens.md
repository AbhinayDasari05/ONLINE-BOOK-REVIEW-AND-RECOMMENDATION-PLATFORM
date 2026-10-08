# Phase 6: UI Screens and Interactive Experience Documentation
**Course Code**: 20CYS401 | **Project**: Online Book Review and Recommendation Platform

---

## 6.1 Overview of Connected UI Screens & Interactive Features

The platform features an interactive, modern user interface built using semantic HTML5, custom responsive CSS design (`app/static/css/style.css`), Jinja2 templating, and vanilla JavaScript for dynamic interactions.

### Key Interactive Features:
1. **Interactive AI Assistant Widget ("BookShield AI")**:
   - Floating action button (FAB) in the bottom-right corner with a pulse indicator.
   - Expandable conversational chat drawer with quick suggestion chips (Thrillers, Cybersecurity, Sci-Fi, Classics, Security Info).
   - Instant book recommendations based on genres and platform assistance.
2. **Dynamic Live Search Suggestions**:
   - Predictive auto-completion dropdown that activates when typing in the search bar.
   - One-click book suggestion insertion with title, author, and category icons.
3. **Genre Quick-Filter Chips & Stats Dashboard**:
   - Overview metrics displaying Total Books, Total Genres, and Community Reviews.
   - One-click genre filter pills (Cybersecurity, Sci-Fi, Fiction, etc.).
4. **Rich Book Cards**:
   - Distinctive gradient covers and thematic book emojis.
   - Dynamic star rating visualizer and review count badges.
5. **Interactive Rating & Review Form**:
   - Interactive 5-star radio picker with dynamic sentiment labels ("Poor", "Average", "Excellent").
   - Live character counter for review content (5–2000 characters).
6. **Authentication Enhancements**:
   - Live password strength indicator bar with color transitions.
   - Real-time password confirmation match checker and username format validation.
   - Show/hide password visibility toggle buttons.

---

## 6.2 Screen Inventory and Navigation Mapping

```mermaid
graph TD
    S1[Screen 1: Login & Register\n/login, /register\nPassword Strength & Match Checker]
    S2[Screen 2: Book Catalog & Search\n/\nLive Search, Genre Chips, AI Assistant]
    S3[Screen 3: Book Details & Reviews\n/books/{id}\nStar Picker, AI Recs, Shelf Widget]
    S4[Screen 4: Personal Reading List\n/my-shelf\nInteractive Shelf Toggles]
    S5[Screen 5: Admin Catalog Management\n/admin/books\nInline CRUD Forms]
    S6[Screen 6: Admin Review Moderation & Audit\n/admin/moderation\nQueue & Real-time Audit Log]

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
- **Route**: `app/routes/auth.py`
- **Interactions**:
  - Live client-side password strength meter (`checkStrength()`).
  - Password confirmation matcher (`checkMatch()`).
  - Username alphanumeric whitelist verification (`checkUser()`).
  - Show/hide password eye toggle buttons (`togglePwd()`).

### Screen 2: Catalog & Search (`/`)
- **Template**: `app/templates/catalog/search.html`
- **Route**: `app/routes/catalog.py`
- **Interactions**:
  - Live auto-complete suggestion box (`suggestionsList`).
  - Genre pill selector filters.
  - Interactive book card hover animations and direct navigation.
  - Quick-action AI recommendation drawer trigger.

### Screen 3: Book Details, Ratings & Reviews (`/books/<int:book_id>`)
- **Template**: `app/templates/catalog/detail.html`
- **Route**: `app/routes/catalog.py`, `app/routes/reviews.py`, `app/routes/reading_list.py`
- **Interactions**:
  - Hover-reactive star rating picker with qualitative label feedbacks.
  - Real-time review text length character counter.
  - Interactive reading status selector (`want-to-read`, `reading`, `finished`).
  - Contextual AI recommendations based on the current book's genre.

### Screen 4: Personal Reading List (`/my-shelf`)
- **Template**: `app/templates/reading_list/index.html`
- **Route**: `app/routes/reading_list.py`
- **Interactions**:
  - Filter and review personal books with inline status update dropdown.

### Screen 5: Administrator Catalog Management (`/admin/books`)
- **Template**: `app/templates/admin/books.html`
- **Route**: `app/routes/admin.py`
- **Interactions**:
  - Add and delete catalog items with server-side validation.

### Screen 6: Administrator Review Moderation & Audit Logs (`/admin/moderation`)
- **Template**: `app/templates/admin/moderation.html`
- **Route**: `app/routes/admin.py`
- **Interactions**:
  - Hide/restore review buttons with audit trail tracking.
