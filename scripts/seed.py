import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.book import Book
from app.models.review import Review
from app.models.reading_list import ReadingListItem
from app.core.audit import log_audit_event

app = create_app()

SAMPLE_BOOKS = [
    {
        "title": "Designing Data-Intensive Applications",
        "author": "Martin Kleppmann",
        "genre": "Software Engineering",
        "isbn": "978-1449373320",
        "description": "The big ideas behind reliable, scalable, and maintainable systems in modern cloud architectures.",
        "publication_year": 2017
    },
    {
        "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
        "author": "Robert C. Martin",
        "genre": "Software Engineering",
        "isbn": "978-0132350884",
        "description": "Best practices for writing readable, maintainable, and refactorable code in agile engineering teams.",
        "publication_year": 2008
    },
    {
        "title": "Threat Modeling: Designing for Security",
        "author": "Adam Shostack",
        "genre": "Cybersecurity",
        "isbn": "978-1118809990",
        "description": "Definitive handbook for security engineers on STRIDE, data flow diagrams, and vulnerability threat trees.",
        "publication_year": 2014
    },
    {
        "title": "Security Engineering: A Guide to Building Dependable Distributed Systems",
        "author": "Ross Anderson",
        "genre": "Cybersecurity",
        "isbn": "978-1119642787",
        "description": "Comprehensive treatise on cryptography, access control, distributed systems, and real-world vulnerabilities.",
        "publication_year": 2020
    },
    {
        "title": "The Phoenix Project: A Novel about IT, DevOps, and Helping Your Business Win",
        "author": "Gene Kim, Kevin Behr, George Spafford",
        "genre": "DevOps",
        "isbn": "978-0988262591",
        "description": "A gripping business novel illustrating the Three Ways of DevOps, lean manufacturing, and fast feedback loops.",
        "publication_year": 2013
    },
    {
        "title": "Building Microservices: Designing Fine-Grained Systems",
        "author": "Sam Newman",
        "genre": "Software Engineering",
        "isbn": "978-1492034025",
        "description": "Comprehensive guide to microservices architectures, service boundaries, and secure decoupled communication.",
        "publication_year": 2021
    },
    {
        "title": "The Web Application Hacker's Handbook",
        "author": "Dafydd Stuttard & Marcus Pinto",
        "genre": "Cybersecurity",
        "isbn": "978-1118026472",
        "description": "Essential guide to finding and exploiting web security flaws including IDOR, injection, and broken authentication.",
        "publication_year": 2011
    },
    {
        "title": "Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation",
        "author": "Jez Humble & David Farley",
        "genre": "DevOps",
        "isbn": "978-0321601919",
        "description": "Pioneering principles for automated deployment pipelines, continuous integration, and trunk-based development.",
        "publication_year": 2010
    },
    {
        "title": "Refactoring: Improving the Design of Existing Code",
        "author": "Martin Fowler",
        "genre": "Software Engineering",
        "isbn": "978-0134757599",
        "description": "Catalogue of refactoring patterns that enhance maintainability and reduce technical debt while preserving behavior.",
        "publication_year": 2018
    },
    {
        "title": "Kubernetes: Up and Running",
        "author": "Brendan Burns, Joe Beda, Kelsey Hightower",
        "genre": "Cloud Computing",
        "isbn": "978-1492046530",
        "description": "Practical guide to container orchestration, declarative workloads, pods, services, and secure cluster ops.",
        "publication_year": 2022
    },
    {
        "title": "The Pragmatic Programmer: Your Journey to Mastery",
        "author": "David Thomas & Andrew Hunt",
        "genre": "Software Engineering",
        "isbn": "978-0135957059",
        "description": "Timeless engineering wisdom on software craftsmanship, defense in depth, automated testing, and career evolution.",
        "publication_year": 2019
    },
    {
        "title": "Practical Cryptography in Python",
        "author": "Seth James Nielson",
        "genre": "Cybersecurity",
        "isbn": "978-1484248997",
        "description": "Hands-on guide to implementing symmetric encryption, digital signatures, hashing algorithms, and PKI securely.",
        "publication_year": 2019
    },
    {
        "title": "Site Reliability Engineering: How Google Runs Production Systems",
        "author": "Niall Richard Murphy, Betsy Beyer",
        "genre": "DevOps",
        "isbn": "978-1491929124",
        "description": "Key collection of essays explaining how Google implements SRE, error budgets, telemetry, and automated resilience.",
        "publication_year": 2016
    },
    {
        "title": "Foundations of Information Security",
        "author": "Jason Andress",
        "genre": "Cybersecurity",
        "isbn": "978-1718500044",
        "description": "Straightforward primer on the CIA triad, authentication protocols, risk analysis, and defensive operations.",
        "publication_year": 2019
    },
    {
        "title": "Domain-Driven Design: Tackling Complexity in the Heart of Software",
        "author": "Eric Evans",
        "genre": "Software Engineering",
        "isbn": "978-0321125217",
        "description": "Foundational concepts for modeling ubiquitous language, bounded contexts, and domain entities in complex projects.",
        "publication_year": 2003
    }
]

def seed_database():
    """Idempotently seed the SQLite database with initial users, catalog, reviews, and shelves."""
    with app.app_context():
        db.create_all()

        print("[*] Seeding demonstration users...")
        users = {}
        demo_accounts = [
            ("admin", os.environ.get("ADMIN_DEFAULT_EMAIL", "admin@platform.local"), os.environ.get("ADMIN_DEFAULT_PASSWORD", "AdminPass123!"), True),
            ("alice", "alice@platform.local", "AlicePass123!", False),
            ("bob", "bob@platform.local", "BobPass123!", False)
        ]

        for uname, uemail, upass, is_adm in demo_accounts:
            user = User.query.filter_by(username=uname).first()
            if not user:
                user = User(username=uname, email=uemail, is_admin=is_adm)
                user.set_password(upass)
                db.session.add(user)
                db.session.commit()
                print(f"    + Created user: {uname} (Admin: {is_adm})")
            else:
                print(f"    = User already exists: {uname}")
            users[uname] = user

        print("[*] Seeding book catalog (15 entries)...")
        books = {}
        for b_data in SAMPLE_BOOKS:
            book = Book.query.filter_by(isbn=b_data["isbn"]).first()
            if not book:
                book = Book(**b_data)
                db.session.add(book)
                db.session.commit()
                print(f"    + Created book: '{book.title}'")
            else:
                print(f"    = Book already exists: '{book.title}'")
            books[b_data["isbn"]] = book

        print("[*] Seeding sample ratings & reviews...")
        ddia = books["978-1449373320"]
        threat_book = books["978-1118809990"]
        phoenix_book = books["978-0988262591"]

        # Alice reviews DDIA
        r1 = Review.query.filter_by(book_id=ddia.id, user_id=users["alice"].id).first()
        if not r1:
            r1 = Review(
                book_id=ddia.id,
                user_id=users["alice"].id,
                rating=5,
                content="Exceptional architectural reference! The chapters on consensus algorithms, replication logs, and partitioning provide profound clarity for building fault-tolerant systems."
            )
            db.session.add(r1)

        # Bob reviews Threat Modeling
        r2 = Review.query.filter_by(book_id=threat_book.id, user_id=users["bob"].id).first()
        if not r2:
            r2 = Review(
                book_id=threat_book.id,
                user_id=users["bob"].id,
                rating=5,
                content="Essential reading for cybersecurity analysts. Adam explains STRIDE threat mapping with realistic software engineering scenarios."
            )
            db.session.add(r2)

        # Bob reviews Phoenix Project
        r3 = Review.query.filter_by(book_id=phoenix_book.id, user_id=users["bob"].id).first()
        if not r3:
            r3 = Review(
                book_id=phoenix_book.id,
                user_id=users["bob"].id,
                rating=4,
                content="Entertaining and highly relatable depiction of IT dysfunction transformed through DevOps practices and WIP management."
            )
            db.session.add(r3)

        db.session.commit()
        print("    + Reviews seeded.")

        print("[*] Seeding reading shelves...")
        # Alice reading list
        if not ReadingListItem.query.filter_by(user_id=users["alice"].id, book_id=threat_book.id).first():
            db.session.add(ReadingListItem(user_id=users["alice"].id, book_id=threat_book.id, status="reading"))
        if not ReadingListItem.query.filter_by(user_id=users["alice"].id, book_id=ddia.id).first():
            db.session.add(ReadingListItem(user_id=users["alice"].id, book_id=ddia.id, status="finished"))

        # Bob reading list
        if not ReadingListItem.query.filter_by(user_id=users["bob"].id, book_id=phoenix_book.id).first():
            db.session.add(ReadingListItem(user_id=users["bob"].id, book_id=phoenix_book.id, status="finished"))

        db.session.commit()
        print("    + Reading list shelves seeded.")

        log_audit_event("DATABASE_SEEDED", "System", None, "SUCCESS", "Initial seed data loaded idempotently")
        print("[✓] Database seeding completed successfully!")

if __name__ == '__main__':
    seed_database()
