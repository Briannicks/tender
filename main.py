from models.book import Book, BookCollection
from utils.auth import AuthManager
from utils.decorators import admin_required, login_required
from utils.validators import not_empty


class BookCLI:
    def __init__(self, users_file="data/users.json", books_file="data/books.json"):
        self.auth = AuthManager(users_file)
        self.collection = BookCollection(books_file)
        self.current_user = None

    def run(self):
        print("\nBOOK COLLECTION MANAGER")

        while True:
            if self.current_user is None:
                self.guest_menu()
            else:
                self.user_menu()

    def guest_menu(self):
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            self.register()
        elif choice == "2":
            self.login()
        elif choice == "3":
            print("Goodbye!")
            raise SystemExit
        else:
            print("Invalid option. Please choose 1, 2 or 3.")

    def user_menu(self):
        print(f"\nWelcome, {self.current_user.name} ({self.current_user.role})")
        print("1. View books")
        print("2. Add book")
        print("3. Search books")
        print("4. Update book status")

        if self.current_user.role == "admin":
            print("5. Delete book")
            print("6. Logout")
        else:
            print("5. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            self.view_books()
        elif choice == "2":
            self.add_book()
        elif choice == "3":
            self.search_books()
        elif choice == "4":
            self.update_status()
        elif choice == "5" and self.current_user.role == "admin":
            self.delete_book()
        elif choice == "5" and self.current_user.role == "user":
            self.logout()
        elif choice == "6" and self.current_user.role == "admin":
            self.logout()
        else:
            print("Invalid option.")

    def register(self):
        print("\nREGISTER")
        name = input("Name: ").strip()
        email = input("Email: ").strip()
        password = input("Password: ")
        role = input("Role (user/admin): ").strip().lower() or "user"

        try:
            self.current_user = self.auth.register(name, email, password, role)
            print("Registration successful. You are now logged in.")
        except ValueError as error:
            print(f"Registration failed: {error}")

    def login(self):
        print("\nLOGIN")
        email = input("Email: ").strip()
        password = input("Password: ")

        user = self.auth.login(email, password)

        if user:
            self.current_user = user
            print("Login successful.")
        else:
            print("Invalid email or password.")

    def logout(self):
        self.current_user = None
        print("You have logged out.")

    @login_required
    def view_books(self):
        books = self.collection.view_books()
        self.display_books(books)

    @login_required
    def add_book(self):
        print("\nADD BOOK")
        title = input("Title: ").strip()
        author = input("Author: ").strip()
        genre = input("Genre: ").strip()

        if not all([not_empty(title), not_empty(author), not_empty(genre)]):
            print("Title, author and genre are required.")
            return

        book = Book(
            title=title,
            author=author,
            genre=genre,
            status="Available",
            added_by=self.current_user.email,
        )

        self.collection.add_book(book)
        print("Book added successfully.")

    @login_required
    def search_books(self):
        search_text = input("Search by title or author: ").strip()

        if not not_empty(search_text):
            print("Search text cannot be empty.")
            return

        books = self.collection.search_books(search_text)
        self.display_books(books)

    @login_required
    def update_status(self):
        title = input("Book title: ").strip()
        status = input("New status (Available/Reading/Read): ").strip()

        if not all([not_empty(title), not_empty(status)]):
            print("Title and status are required.")
            return

        if self.collection.update_status(title, status):
            print("Book status updated.")
        else:
            print("Book not found.")

    @admin_required
    def delete_book(self):
        title = input("Book title to delete: ").strip()

        if self.collection.delete_book(title):
            print("Book deleted.")
        else:
            print("Book not found.")

    @staticmethod
    def display_books(books):
        if not books:
            print("No books found.")
            return

        print("\nBOOKS")
        for number, book in enumerate(books, start=1):
            print(
                f"{number}. {book.title} | {book.author} | "
                f"{book.genre} | {book.status}"
            )


if __name__ == "__main__":
    try:
        BookCLI().run()
    except KeyboardInterrupt:
        print("\nApplication closed.")
