class Book:
    """
    Base class demonstrating:
    - Encapsulation
    - Special methods: __str__, __len__, __eq__
    """

    def __init__(self, title, author, pages):
        self._title = title
        self._author = author
        self._pages = pages

    # Encapsulation: read-only properties
    @property
    def title(self):
        return self._title

    @property
    def pages(self):
        return self._pages

    # ===== Special Methods =====

    def __str__(self):
        """Human-readable string"""
        return f"{self._title} by {self._author}"

    def __len__(self):
        """Allows: len(book) -> number of pages"""
        return self._pages

    def __eq__(self, other):
        """Books are equal if title and author match"""
        if isinstance(other, Book):
            return (self._title == other._title) and (self._author == other._author)
        return False


# ===== SUBCLASSES for Inheritance + Polymorphism =====

class PrintedBook(Book):
    def __init__(self, title, author, pages, weight):
        super().__init__(title, author, pages)
        self._weight = weight

    def __str__(self):
        """Polymorphism: override __str__"""
        return f"[Printed] {self.title} - {self.pages} pages"


class EBook(Book):
    def __init__(self, title, author, pages, filesize):
        super().__init__(title, author, pages)
        self._filesize = filesize

    def __str__(self):
        return f"[E-Book] {self.title} - {self.pages} pages"


# ===== Library Class Using __len__ and __str__ =====

class Library:
    def __init__(self, name):
        self._name = name
        self._books = []

    def add_book(self, book):
        self._books.append(book)

    def __len__(self):
        """Returns number of books in the library"""
        return len(self._books)

    def __str__(self):
        """Human-readable listing of books"""
        output = f"Library: {self._name}\n"
        for b in self._books:
            output += f" - {str(b)}\n"
        return output.strip()




# ===== DEMO =====
if __name__ == "__main__":
    b1 = PrintedBook("1984", "George Orwell", 328, 300)
    b2 = EBook("1984", "George Orwell", 328, 3)
    b3 = PrintedBook("The Hobbit", "Tolkien", 310, 280)

    # Test __str__
    print(b1)
    print(b2)

    # Test __len__
    print("Pages in b3:", len(b3))

    # Test __eq__
    print("Are b1 and b2 equal?", b1 == b2)

    # Library using __len__ and __str__
    lib = Library("Fantasy Library")
    lib.add_book(b1)
    lib.add_book(b3)

    print("\nNumber of books:", len(lib))
    print(lib)
