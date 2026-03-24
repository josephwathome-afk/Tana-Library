import json
import os


class Book:
    def __init__(self, title: str, author: str, isbn: str, pages: int = 0, available: bool = True):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.pages = pages
        self.available = available

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "pages": self.pages,
            "available": self.available,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        return cls(
            title=data["title"],
            author=data["author"],
            isbn=data["isbn"],
            pages=data.get("pages", 0),
            available=data.get("available", True),
        )

    def borrow(self):
        if not self.available:
            raise ValueError(f"'{self.title}' is already borrowed.")
        self.available = False

    def return_book(self):
        if self.available:
            raise ValueError(f"'{self.title}' was not borrowed.")
        self.available = True

    def __str__(self):
        status = "Available" if self.available else "Borrowed"
        return f"{self.title} by {self.author} [{status}]"


class Library:
    def __init__(self, storage_path: str = "books.json"):
        self.storage_path = storage_path
        self.books: dict[str, Book] = {}
        self._load()

    # ── Persistence ──────────────────────────────────────────────────────────

    def _load(self):
        """Load books from JSON file on startup."""
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                data: dict = json.load(f)
            self.books = {isbn: Book.from_dict(book) for isbn, book in data.items()}

    def _save(self):
        """Persist current books to JSON file."""
        with open(self.storage_path, "w") as f:
            json.dump(
                {isbn: book.to_dict() for isbn, book in self.books.items()},
                f,
                indent=2,
            )

    # ── CRUD ─────────────────────────────────────────────────────────────────

    def add_book(self, book: Book):
        if book.isbn in self.books:
            raise KeyError("A book with this ISBN already exists.")
        self.books[book.isbn] = book
        self._save()

    def remove_book(self, isbn: str):
        if isbn not in self.books:
            raise KeyError("Book not found.")
        del self.books[isbn]
        self._save()

    def find_book(self, title: str) -> list[Book]:
        """Return all books whose title matches (case-insensitive)."""
        return [b for b in self.books.values() if b.title.lower() == title.lower()]

    def list_books(self) -> list[str]:
        return [str(b) for b in self.books.values()]