# design library management system
# library, book management, lending, submitting, user management (librarian, member)

# Base abstract class for all users
from abc import ABC, abstractmethod
from typing import List


class Book:
    def __init__(self, book_id: int, name: str, author: str, genre: str, edition: str):
        self.book_id = book_id
        self.name = name
        self.author = author
        self.genre = genre
        self.edition = edition


class BookItem:
    def __init__(self, item_id: int, book: Book):
        self.item_id = item_id
        self.book = book
        self.is_available = True


class Catalog:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Catalog, cls).__new__(cls)
            cls._instance.books = {}
        return cls._instance

    def add_book(self, book: Book):
        self.books[book.name] = book

    def search_book(self, name: str):
        return self.books.get(name)


class User(ABC):
    def __init__(self, user_id, name, address):
        self.user_id = user_id
        self.name = name
        self.address = address

    @abstractmethod
    def search_book(self, catalog: Catalog, name: str):
        pass


class Member(User):
    def __init__(self, user_id, name, address):
        super().__init__(user_id, name, address)
        self.borrowed_books: List[BookItem] = []

    def search_book(self, catalog: Catalog, name: str):
        books = catalog.search_book(name)
        return books

    def borrow_book(self, book: BookItem):
        if len(self.borrowed_books) >= 5 or not book.is_available:
            return False
        book.is_available = True
        self.borrowed_books.append(book)
        return True

    def return_book(self, book: BookItem):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.is_available = True
            return True
        return False


class LibraryBranch:
    def __init__(self, branch_id, address):
        self.branch_id = branch_id
        self.address = address
        self.book_items: List[BookItem] = []


class Librarian(User):
    def __init__(self, user_id, name, address):
        super().__init__(user_id, name, address)

    def search_book(self, catalog: Catalog, name: str):
        books = catalog.search_book(name)
        return books

    @staticmethod
    def add_book(book_item: BookItem, branch: LibraryBranch):
        branch.book_items.append(book_item)

    @staticmethod
    def remove_book(book_item: BookItem, branch: LibraryBranch):
        if book_item in branch.book_items:
            branch.book_items.remove(book_item)


if __name__ == "__main__":
    catalog = Catalog()

    book = Book(1, "design patterns", "peter", "tech", "2nd edition")

    catalog.add_book(book)

    book_item1 = BookItem(1, book)
    book_item2 = BookItem(2, book)

    member = Member(1, "manoj", "103")
    librarian = Librarian(1, "Admin", "102")

    branch = LibraryBranch(1, "bangalore, btm layout")
    librarian.add_book(book_item1, branch)
    librarian.add_book(book_item2, branch)

    success = member.borrow_book(book_item1)
    print(f"borrowing book {success}")

    success = member.return_book(book_item1)
    print(f"returned book {success}")
