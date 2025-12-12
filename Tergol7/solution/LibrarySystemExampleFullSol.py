class Book:
    """
    Base class demonstrating:
    - Encapsulation
    - Special methods: __str__, __len__, __eq__
    - Properties (get + set for pages)
    """

    def __init__(self, title, author, pages):
        self._title = title
        self._author = author
        self._pages = pages

    # ===== Encapsulation: read-only property for title =====
    @property
    def title(self):
        return self._title

    # pages: getter + setter with validation
    @property
    def pages(self):
        return self._pages

    @pages.setter
    def pages(self, value):
        """
        Setter with validation:
        - value must be int
        - value > 0
        - value <= 3000
        """
        if not isinstance(value, int):
            raise ValueError("Pages must be an integer")
        if value <= 0:
            raise ValueError("Pages must be positive")
        if value > 3000:
            raise ValueError("Pages cannot be greater than 3000")
        self._pages = value

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
        self._weight = weight  # grams

    def __str__(self):
        """Polymorphism: override __str__"""
        return f"[Printed] {self.title} - {self.pages} pages"


class EBook(Book):
    def __init__(self, title, author, pages, filesize):
        super().__init__(title, author, pages)
        self._filesize = filesize  # MB

    def __str__(self):
        return f"[E-Book] {self.title} - {self.pages} pages"


class AudioBook(Book):
    """
    New subclass:
    - adds duration in minutes
    - overrides __str__
    - (optionally) overrides __len__ to return duration instead of pages
    """

    def __init__(self, title, author, pages, duration_minutes):
        super().__init__(title, author, pages)
        self._duration_minutes = duration_minutes

    def __str__(self):
        return f"[Audio] {self.title} - {self.pages} pages - {self._duration_minutes} minutes"

    def __len__(self):
        """
        Design choice:
        For AudioBook, len(book) returns duration in minutes
        instead of number of pages.
        """
        return self._duration_minutes


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

    def total_pages(self):
        """
        Returns total 'size' of all books.
        For regular books: number of pages.
        For AudioBook (in this implementation): duration in minutes,
        because we overrode __len__ there.
        """
        return sum(len(b) for b in self._books)

    def find_by_title(self, title):
        """
        Returns a list of all books whose title matches the given string.
        """
        return [b for b in self._books if b.title == title]

    def __contains__(self, book):
        """
        Allows: book in lib
        """
        return book in self._books


# ===== DEMO =====
if __name__ == "__main__":
    # Original books
    b1 = PrintedBook("1984", "George Orwell", 328, 300)
    b2 = EBook("1984", "George Orwell", 328, 3)
    b3 = PrintedBook("The Hobbit", "Tolkien", 310, 280)

    # New AudioBook
    b4 = AudioBook("1984", "George Orwell", 328, 600)

    # Test __str__ (polymorphism)
    print("=== __str__ demo ===")
    print(b1)
    print(b2)
    print(b4)

    # Test __len__ for different types
    print("\n=== __len__ demo ===")
    print("Pages in b3 (PrintedBook):", len(b3))
    print("Duration in b4 (AudioBook):", len(b4), "minutes")

    # Test __eq__
    print("\n=== __eq__ demo ===")
    print("Are b1 and b2 equal?", b1 == b2)
    print("Are b1 and b3 equal?", b1 == b3)

    # Test pages setter (valid + invalid)
    print("\n=== pages setter demo ===")
    print("Original pages in b1:", b1.pages)
    b1.pages = 250
    print("Updated pages in b1:", b1.pages)

    print("\nTrying to set invalid pages (-10):")
    try:
        b1.pages = -10
    except ValueError as e:
        print("Error:", e)

    print("\nTrying to set invalid pages (100000):")
    try:
        b1.pages = 100000
    except ValueError as e:
        print("Error:", e)

    print("\nTrying to set invalid pages ('abc'):")
    try:
        b1.pages = "abc"
    except ValueError as e:
        print("Error:", e)

    # Library using __len__, __str__, total_pages, find_by_title, __contains__
    print("\n=== Library demo ===")
    lib = Library("Fantasy Library")
    lib.add_book(b1)
    lib.add_book(b2)
    lib.add_book(b3)
    lib.add_book(b4)

    print("Number of books in library:", len(lib))
    print("Total pages/duration (sum of len(book)):", lib.total_pages())
    print("\nLibrary content:")
    print(lib)

    # find_by_title demo
    print("\n=== find_by_title('1984') ===")
    found = lib.find_by_title("1984")
    for book in found:
        print("Found:", book)

    # __contains__ demo
    print("\n=== __contains__ demo ===")
    if b1 in lib:
        print("b1 is in the library")
    else:
        print("b1 is NOT in the library")

    fake_book = PrintedBook("Fake", "Nobody", 100, 200)
    if fake_book in lib:
        print("fake_book is in the library")
    else:
        print("fake_book is NOT in the library")
