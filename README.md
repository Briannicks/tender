# Book Collection Manager CLI

## A Beginner-Friendly Python OOP Course Project

The **Book Collection Manager** is a simple command-line application written in Python. It allows people to create accounts, log in, and manage a shared collection of books.

The project is intentionally small. Its main purpose is to demonstrate the Python concepts required in the assignment without adding unnecessary frameworks, databases, or advanced patterns.

The application demonstrates:

- Classes and objects
- Inheritance
- Encapsulation
- Multiple interacting classes
- Modular Python files
- JSON file persistence
- Registration and login
- Password hashing
- User and Admin roles
- Decorators
- Input validation
- Error handling
- Interactive CLI menus

---

# 1. Short Project Proposal

## Project title

**Book Collection Manager CLI**

## Problem

A student, book lover, or small reading group may want a simple way to keep a digital record of books without using a full web application or database system.

The Book Collection Manager provides a command-line solution where users can register, log in, add books, view books, search for books, and update their reading status. Administrators have one extra permission: they can delete books.

The project focuses on learning Python programming and Object-Oriented Programming rather than building a large production system.

## Target users

The target users are:

- Students
- Book lovers
- Reading clubs
- Small personal libraries
- Beginner Python programmers learning OOP

## Core features

The application supports:

1. User registration
2. User login
3. Password hashing
4. User and Admin roles
5. Adding books
6. Viewing books
7. Searching books
8. Updating a book's status
9. Deleting books for Admin users
10. Saving users and books in JSON files

## Main entities

The main entities are:

- `User`
- `Admin`
- `Book`
- `BookCollection`
- `AuthManager`

The two main data entities are `User` and `Book`.

---

# 2. Planned Classes

| Class | Purpose |
|---|---|
| `User` | Represents a normal application user |
| `Admin` | Represents an administrator and inherits from `User` |
| `Book` | Represents one book |
| `BookCollection` | Manages the collection of books and book persistence |
| `AuthManager` | Handles registration and login |
| `BookCLI` | Controls the menus and user interaction |

The most important inheritance relationship is:

```text
User
  ^
  |
Admin
```

`Admin` is a specialized type of `User`.

The main object interactions are:

```text
BookCLI
   |
   +---- AuthManager ---- User / Admin
   |
   +---- BookCollection ---- Book
```

`BookCLI` coordinates the other objects.

---

# 3. Storage Plan

The project uses JSON files rather than a database.

```text
data/
├── users.json
└── books.json
```

`users.json` stores registered users.

Example:

```json
[
    {
        "name": "Jane",
        "email": "jane@example.com",
        "password_hash": "hashed-value-here",
        "role": "user"
    }
]
```

`books.json` stores books.

Example:

```json
[
    {
        "title": "Things Fall Apart",
        "author": "Chinua Achebe",
        "genre": "Fiction",
        "status": "Available",
        "added_by": "jane@example.com"
    }
]
```

The application reads these files when information is needed and writes back to them when data changes.

---

# 4. Authentication Strategy

The authentication system follows this simple flow:

```text
Registration
    |
    v
Validate input
    |
    v
Hash password
    |
    v
Save user to users.json
```

Login follows this flow:

```text
Email + Password
       |
       v
Find email in users.json
       |
       v
Hash entered password
       |
       v
Compare hashes
       |
   +---+---+
   |       |
 Match   No match
   |       |
 Login   Reject
```

The plain password is not stored in the JSON file.

For simplicity, the project uses Python's built-in `hashlib.sha256()` function.

> **Learning note:** SHA-256 demonstrates password hashing clearly, but production applications should use a password-specific hashing algorithm such as Argon2, bcrypt, or PBKDF2 with a salt. Also, this teaching project allows a person to choose `admin` during registration so role-based access can be demonstrated easily. A real application should not allow public users to make themselves administrators.

---

# 5. Git Workflow Plan

A simple Git workflow is enough for this project.

Start the repository:

```bash
git init
git add .
git commit -m "Initial project setup"
```

Possible feature branches:

```text
main
 |
 +--- feature-auth
 |
 +--- feature-books
 |
 +--- feature-cli
```

Example authentication workflow:

```bash
git checkout -b feature-auth
git add .
git commit -m "Add user authentication"
git checkout main
git merge feature-auth
```

The same approach can be used for books and the CLI.

A simple commit history could look like:

```text
Initial project setup
Add user authentication
Add book management
Add CLI menus
Add documentation
```

---

# 6. Project Folder Structure

```text
book_collection_cli/
│
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   └── book.py
│
├── utils/
│   ├── __init__.py
│   ├── auth.py
│   ├── decorators.py
│   ├── storage.py
│   └── validators.py
│
├── data/
│   ├── users.json
│   └── books.json
│
└── tests/
    ├── __init__.py
    ├── test_auth.py
    ├── test_books.py
    ├── test_cli.py
    └── test_decorators.py
```

The production application remains small. The `tests/` folder is separate and is only used to confirm that the application behaves correctly.

---

# 7. How to Run the Application

## Requirement

Install Python 3.

Check Python:

```bash
python --version
```

No external package is required.

Move into the project folder:

```bash
cd book_collection_cli
```

Run:

```bash
python main.py
```

On some systems the command may be:

```bash
python3 main.py
```

---

# 8. CLI Experience

When the program starts, a guest sees:

```text
BOOK COLLECTION MANAGER

1. Register
2. Login
3. Exit
```

After a normal user logs in:

```text
Welcome, Jane (user)
1. View books
2. Add book
3. Search books
4. Update book status
5. Logout
```

An Admin sees:

```text
Welcome, Admin (admin)
1. View books
2. Add book
3. Search books
4. Update book status
5. Delete book
6. Logout
```

The extra Admin option demonstrates role-based access control.

---

# 9. Coursebook: Understanding the Code

The rest of this README explains the project file by file.

---

# 10. `models/user.py`

This file contains the `User` and `Admin` classes.

## Importing hashlib

```python
import hashlib
```

`hashlib` is part of Python's standard library. It provides hashing algorithms.

We use it to turn a password such as:

```text
secret123
```

into a hash such as:

```text
fcf730b6d95236ec...
```

The original password is therefore not saved directly.

## The User class

```python
class User:
```

A class is a blueprint for creating objects.

For example:

```python
user = User(...)
```

creates one `User` object.

## Constructor

```python
def __init__(self, name, email, password_hash, role="user"):
```

`__init__()` runs automatically whenever a new object is created.

It receives:

- `name`
- `email`
- `password_hash`
- `role`

The default role is `user`.

```python
self.name = name
self.email = email
self.__password_hash = password_hash
self.role = role
```

`self` refers to the current object.

If Jane is created, her object may conceptually contain:

```text
name  -> Jane
email -> jane@example.com
role  -> user
```

## Encapsulation

Notice:

```python
self.__password_hash
```

The two underscores make the attribute private through Python name mangling.

Instead of other parts of the program freely changing the password hash, the `User` class controls how it is accessed.

This demonstrates **encapsulation**.

## Password hashing

```python
@staticmethod
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
```

`@staticmethod` means the method belongs logically to the class but does not need a particular User object.

This can therefore be called as:

```python
User.hash_password("secret123")
```

`password.encode()` converts the text password to bytes.

`hashlib.sha256(...)` hashes those bytes.

`.hexdigest()` converts the hash to readable hexadecimal text that can be stored in JSON.

## Checking a password

```python
def check_password(self, password):
    return self.__password_hash == self.hash_password(password)
```

When someone logs in, the application does not decrypt the stored password.

Instead it:

1. Takes the password typed by the user.
2. Hashes it again.
3. Compares the new hash with the stored hash.

If they match, the password is correct.

## Property

```python
@property
def password_hash(self):
    return self.__password_hash
```

A property provides controlled read access to the private value.

The value can be read as:

```python
user.password_hash
```

but the class does not provide a normal setter that allows arbitrary replacement.

## Converting a user to a dictionary

```python
def to_dict(self):
```

JSON stores dictionaries and lists, not custom Python objects directly.

Therefore a `User` object must be converted to a dictionary before it can be saved.

The result looks like:

```python
{
    "name": self.name,
    "email": self.email,
    "password_hash": self.__password_hash,
    "role": self.role,
}
```

## Admin inheritance

```python
class Admin(User):
```

This means `Admin` inherits from `User`.

Therefore an Admin already has:

- a name
- an email
- a password hash
- password checking
- dictionary conversion

We do not repeat that code.

This is both **inheritance** and **DRY programming**.

The Admin constructor contains:

```python
super().__init__(name, email, password_hash, role="admin")
```

`super()` calls the parent `User` constructor.

The only special change is that the role becomes `admin`.

---

# 11. `models/book.py`

This file contains the `Book` and `BookCollection` classes.

## Book class

```python
class Book:
```

Each object represents one book.

Its constructor is:

```python
def __init__(self, title, author, genre, status="Available", added_by=""):
```

The attributes are:

- `title`
- `author`
- `genre`
- `status`
- `added_by`

For example:

```python
book = Book(
    "Things Fall Apart",
    "Chinua Achebe",
    "Fiction"
)
```

The default status is `Available`.

## `to_dict()`

Like a User, a Book must be converted to a dictionary before JSON can save it.

```python
def to_dict(self):
```

returns a normal Python dictionary containing the book information.

## `from_dict()`

```python
@classmethod
def from_dict(cls, data):
```

This does the opposite.

It receives a dictionary loaded from JSON and creates a `Book` object from it.

The process is:

```text
JSON dictionary
      |
      v
Book.from_dict()
      |
      v
Book object
```

`@classmethod` receives `cls`, which represents the class itself.

## BookCollection

```python
class BookCollection:
```

A `Book` represents one book.

A `BookCollection` manages many books.

This separation makes the responsibilities clearer:

```text
Book           -> information about one book
BookCollection -> operations involving many books
```

## Constructor

```python
def __init__(self, books_file="data/books.json"):
```

The collection remembers where the book JSON file is stored.

## `_load_books()`

```python
def _load_books(self):
```

The single underscore means the method is intended for internal use.

It:

1. Reads the JSON file.
2. Receives dictionaries.
3. Converts every dictionary into a `Book` object.

The list comprehension:

```python
[Book.from_dict(item) for item in load_json(self.books_file)]
```

is a shorter version of:

```python
books = []

for item in load_json(self.books_file):
    book = Book.from_dict(item)
    books.append(book)
```

## `_save_books()`

Before saving, each Book object is converted back into a dictionary.

```text
Book objects
    |
    v
to_dict()
    |
    v
Dictionaries
    |
    v
JSON file
```

## `add_book()`

```python
def add_book(self, book):
```

The method:

1. Loads existing books.
2. Adds the new Book object to the list.
3. Saves the updated list.

This is file-based persistence.

## `view_books()`

```python
def view_books(self):
    return self._load_books()
```

It simply returns all saved books.

## `search_books()`

The search text is converted to lowercase:

```python
search_text = search_text.lower()
```

Book titles and authors are also compared in lowercase.

Therefore searches are case-insensitive.

For example:

```text
clean
Clean
CLEAN
```

can all match `Clean Code`.

## `update_status()`

The method searches for a matching title.

When it finds the book:

```python
book.status = new_status
```

It then saves the updated list and returns:

```python
True
```

If no book is found, it returns:

```python
False
```

Returning `True` or `False` lets the CLI decide which message to show.

## `delete_book()`

The method searches for the book title and removes the matching Book object.

```python
books.remove(book)
```

It then saves the changed list.

The method itself does not decide whether the caller is an Admin. Access control is handled by a decorator in the CLI.

That separation keeps `BookCollection` focused only on book management.

---

# 12. `utils/storage.py`

This file is responsible for JSON reading and writing.

Keeping JSON code in one file follows the DRY principle.

Without it, `user.py`, `book.py`, and other files might each repeat the same JSON code.

## Loading JSON

```python
def load_json(file_path):
```

The function first creates a `Path` object:

```python
path = Path(file_path)
```

Then it checks whether the file exists:

```python
if not path.exists():
    return []
```

A missing file therefore behaves like an empty collection rather than crashing the application.

The file is opened using:

```python
with path.open("r", encoding="utf-8") as file:
```

`"r"` means read mode.

`json.load(file)` converts JSON into Python lists and dictionaries.

## Error handling

```python
except (json.JSONDecodeError, OSError):
    return []
```

This handles simple file problems.

- `JSONDecodeError` can happen when JSON is invalid.
- `OSError` can happen when there is a file-system problem.

For this beginner project the function returns an empty list instead of exposing a long technical error to the CLI user.

## Saving JSON

```python
def save_json(file_path, data):
```

This line makes sure the parent folder exists:

```python
path.parent.mkdir(parents=True, exist_ok=True)
```

Then the file is opened in write mode:

```python
with path.open("w", encoding="utf-8") as file:
```

`json.dump()` writes Python data into JSON.

```python
json.dump(data, file, indent=4)
```

`indent=4` makes the JSON easier for humans to read.

---

# 13. `utils/validators.py`

This file contains very small validation functions.

## Checking empty values

```python
def not_empty(value):
    return bool(value.strip())
```

`.strip()` removes spaces at the beginning and end.

Therefore:

```text
"     "
```

is treated as empty.

## Checking an email

```python
def valid_email(email):
```

The validation deliberately stays simple.

It checks that:

- `@` exists
- the part after `@` contains `.`

This is enough for the coursework demonstration, although production email validation can be more detailed.

---

# 14. `utils/auth.py`

This file contains `AuthManager`.

Its responsibility is authentication.

The class does not manage books and does not display menus.

That keeps each class focused on one main job.

## Constructor

```python
def __init__(self, users_file="data/users.json"):
```

The default user file is:

```text
data/users.json
```

The path can also be replaced during testing.

## Registration

```python
def register(self, name, email, password, role="user"):
```

The method first cleans input:

```python
name = name.strip()
email = email.strip().lower()
role = role.strip().lower()
```

Converting emails to lowercase helps prevent duplicate accounts such as:

```text
JANE@example.com
jane@example.com
```

being treated as different users.

The method then validates:

- name
- email
- password length
- role

Invalid input raises a `ValueError`.

For example:

```python
raise ValueError("Please enter a valid email.")
```

The CLI catches that error and shows a readable message.

## Preventing duplicate emails

The program loads saved users and checks every email.

If a duplicate is found, registration stops.

## Creating the correct object

If the role is `admin`:

```python
user = Admin(...)
```

Otherwise:

```python
user = User(...)
```

This is where inheritance becomes useful in the real program.

## Saving the user

The User object is converted to a dictionary:

```python
users.append(user.to_dict())
```

Then saved:

```python
save_json(self.users_file, users)
```

## Login

```python
def login(self, email, password):
```

The method:

1. Loads all saved users.
2. Searches for the email.
3. Recreates either a `User` or `Admin` object.
4. Calls `check_password()`.
5. Returns the user object if successful.
6. Returns `None` when login fails.

This is important because `main.py` can simply test:

```python
if user:
```

instead of repeating authentication logic.

---

# 15. `utils/decorators.py`

A decorator wraps another function and adds behavior around it.

The project uses two decorators:

```python
@login_required
```

and:

```python
@admin_required
```

## `login_required`

A protected method can be written as:

```python
@login_required
def add_book(self):
```

Before `add_book()` runs, the wrapper checks:

```python
if self.current_user is None:
```

If no user is logged in, the function stops.

This avoids writing the same login check inside every protected method.

That is a good example of DRY code.

## `admin_required`

The Admin decorator checks both:

1. A user is logged in.
2. The logged-in user's role is `admin`.

```python
if self.current_user.role != "admin":
```

If the check fails, deletion is blocked.

## `@wraps`

```python
from functools import wraps
```

and:

```python
@wraps(function)
```

help preserve information such as the original function's name after it has been decorated.

---

# 16. `main.py`

`main.py` is the entry point of the application.

It contains `BookCLI`, which coordinates the program.

## Imports

```python
from models.book import Book, BookCollection
from utils.auth import AuthManager
from utils.decorators import admin_required, login_required
from utils.validators import not_empty
```

Notice that `main.py` does not contain the internal code for hashing or JSON persistence.

It imports those responsibilities from their proper modules.

This demonstrates modular programming.

## Constructor

```python
def __init__(self, users_file="data/users.json", books_file="data/books.json"):
```

Three important attributes are created:

```python
self.auth = AuthManager(users_file)
self.collection = BookCollection(books_file)
self.current_user = None
```

This demonstrates **object interaction**.

`BookCLI` contains and uses an `AuthManager` and a `BookCollection`.

At program start:

```python
self.current_user = None
```

because nobody is logged in.

## `run()`

`run()` contains the main application loop.

```python
while True:
```

The application keeps running until the user chooses Exit.

It checks:

```python
if self.current_user is None:
```

Guests see the guest menu.

Logged-in users see the user menu.

## Guest menu

The guest menu supports:

- Register
- Login
- Exit

Menu choices are stored as strings.

For example:

```python
if choice == "1":
```

Using strings keeps the menu simple and avoids converting input to integers.

Invalid choices are handled with:

```python
else:
    print("Invalid option. Please choose 1, 2 or 3.")
```

## User menu

The menu changes according to the role.

Normal users receive five choices.

Admins receive an extra Delete option.

This is one visible part of role-based access control.

The decorator on `delete_book()` provides another layer of access control.

## Registration in the CLI

The CLI asks for:

```text
Name
Email
Password
Role
```

It then calls:

```python
self.auth.register(...)
```

Notice that `main.py` does not hash the password itself.

That job belongs to `AuthManager` and `User`.

The registration call is inside:

```python
try:
```

and:

```python
except ValueError as error:
```

This is error handling.

If validation fails, the program continues instead of crashing.

## Login in the CLI

The CLI asks for email and password and passes them to:

```python
self.auth.login(email, password)
```

When login succeeds:

```python
self.current_user = user
```

The application now knows who is using it.

## Logout

Logout is very simple:

```python
self.current_user = None
```

The user is no longer authenticated, so the next loop shows the guest menu.

## Viewing books

```python
@login_required
def view_books(self):
```

Only a logged-in user can access it.

The CLI asks the collection for books:

```python
books = self.collection.view_books()
```

and passes them to the display method.

## Adding books

The application asks for:

- title
- author
- genre

Then it checks:

```python
if not all([not_empty(title), not_empty(author), not_empty(genre)]):
```

If any required value is empty, the method stops.

Otherwise a Book object is created:

```python
book = Book(...)
```

The logged-in user's email is saved in:

```python
added_by=self.current_user.email
```

Finally:

```python
self.collection.add_book(book)
```

saves the book.

## Searching books

The search method accepts part of a title or author name.

For example:

```text
Search: achebe
```

can find:

```text
Things Fall Apart | Chinua Achebe
```

## Updating status

A user gives the title and a new status.

Suggested statuses are:

- `Available`
- `Reading`
- `Read`

The `BookCollection` returns `True` or `False`, allowing the CLI to print either success or `Book not found.`

## Deleting books

```python
@admin_required
def delete_book(self):
```

This method demonstrates role-based access using a decorator.

Even if a normal user somehow tries to call the method directly, the decorator blocks access.

## Displaying books

```python
@staticmethod
def display_books(books):
```

This helper avoids repeating book-printing code in both View and Search.

That is another DRY decision.

`enumerate()` is used to number the results:

```python
for number, book in enumerate(books, start=1):
```

Example output:

```text
1. Things Fall Apart | Chinua Achebe | Fiction | Available
2. 1984 | George Orwell | Fiction | Read
```

## Starting the application

At the bottom:

```python
if __name__ == "__main__":
```

means the CLI starts only when `main.py` is run directly.

```python
BookCLI().run()
```

creates a BookCLI object and starts the menu loop.

The application also handles `Ctrl+C`:

```python
except KeyboardInterrupt:
```

so the program closes with a friendly message instead of a long traceback.

---

# 17. How the Classes Work Together

A registration request follows this route:

```text
BookCLI.register()
       |
       v
AuthManager.register()
       |
       +---- validators
       |
       +---- User.hash_password()
       |
       +---- User or Admin object
       |
       v
storage.save_json()
       |
       v
users.json
```

Adding a book follows this route:

```text
BookCLI.add_book()
       |
       v
Book object
       |
       v
BookCollection.add_book()
       |
       v
storage.save_json()
       |
       v
books.json
```

This is an example of **multiple interacting classes**.

---

# 18. OOP Concepts in the Project

## 18.1 Classes

Classes used include:

```text
User
Admin
Book
BookCollection
AuthManager
BookCLI
```

A class describes what data and behavior an object should have.

## 18.2 Objects

Examples of objects are:

```python
user = User(...)
book = Book(...)
collection = BookCollection(...)
```

Each object is an instance of a class.

## 18.3 Inheritance

```python
class Admin(User):
```

Admin inherits User behavior.

This prevents duplication.

## 18.4 Encapsulation

```python
self.__password_hash
```

The password hash is kept inside the User class and accessed through class methods and a property.

## 18.5 Composition / object interaction

`BookCLI` creates:

```python
self.auth = AuthManager(...)
self.collection = BookCollection(...)
```

Instead of doing everything itself, it uses other objects.

---

# 19. JSON Persistence Explained

Persistence means information remains available after the program closes.

Without persistence:

```text
Run program
Add book
Close program
Book disappears
```

With JSON persistence:

```text
Run program
Add book
Save to books.json
Close program
Run again
Load books.json
Book still exists
```

That is why `users.json` and `books.json` are important.

---

# 20. Decorators Explained Simply

Without a decorator, several methods might repeat:

```python
if self.current_user is None:
    print("Please login first.")
    return
```

Instead we write that rule once:

```python
@login_required
```

and reuse it.

Conceptually:

```text
Call add_book()
      |
      v
login_required checks login
      |
   +--+--+
   |     |
Logged  Guest
   |     |
   v     v
Run    Stop
```

---

# 21. Input Validation and Error Handling

The project validates several inputs.

## Name

Cannot be blank.

## Email

Must look like an email address.

## Password

Must contain at least four characters.

This is intentionally short for the coursework example. A real system should require stronger passwords.

## Role

Must be:

```text
user
```

or:

```text
admin
```

## Book fields

Title, author, and genre cannot be empty.

## Menu choices

Unknown choices print an error message instead of crashing.

## File errors

Basic JSON and file errors are caught in `load_json()`.

## Keyboard interruption

`Ctrl+C` is caught when running the application directly.

---

# 22. Why the Project Is Modular

A non-modular program might put everything in one large `main.py`.

That can become difficult to read.

This project separates responsibilities:

```text
models/     -> objects and business data
utils/      -> reusable helpers
main.py     -> menus and coordination
data/       -> stored information
tests/      -> checks application behavior
```

A useful rule is:

> One file should have one clear main responsibility.

---

# 23. Why the Code Is DRY

DRY means:

**Don't Repeat Yourself.**

Examples in this project include:

- JSON reading is written once in `load_json()`.
- JSON saving is written once in `save_json()`.
- Login checking is written once in `@login_required`.
- Admin checking is written once in `@admin_required`.
- Book display logic is written once in `display_books()`.
- Admin reuses User behavior through inheritance.

The project stays DRY without introducing complicated abstractions.

---

# 24. Running the Tests

Tests are included so the behavior can be checked without manually trying every feature.

Run:

```bash
python -m unittest discover -s tests -v
```

The tests cover:

- password hashing
- user registration
- Admin registration
- duplicate users
- invalid emails
- successful login
- failed login
- adding books
- searching books
- updating status
- deleting books
- login-required decorator
- admin-required decorator
- basic CLI registration and login behavior

Tests are useful because changing the program later can accidentally break something that previously worked.

---

# 25. Example User Session

```text
BOOK COLLECTION MANAGER

1. Register
2. Login
3. Exit
Choose an option: 1

REGISTER
Name: Jane
Email: jane@example.com
Password: secret123
Role (user/admin): user
Registration successful. You are now logged in.

Welcome, Jane (user)
1. View books
2. Add book
3. Search books
4. Update book status
5. Logout
Choose an option: 2

ADD BOOK
Title: Things Fall Apart
Author: Chinua Achebe
Genre: Fiction
Book added successfully.
```

If the application is closed and opened again, the user and book remain in their JSON files.

---

# 26. Requirement Checklist

| Requirement | Where it is implemented |
|---|---|
| Classes | `User`, `Admin`, `Book`, `BookCollection`, `AuthManager`, `BookCLI` |
| Inheritance | `Admin(User)` |
| Encapsulation | `User.__password_hash` |
| Multiple interacting classes | `BookCLI`, `AuthManager`, `BookCollection`, `User`, `Book` |
| Modular structure | `models/`, `utils/`, `data/`, `tests/` |
| JSON persistence | `storage.py`, `users.json`, `books.json` |
| Decorators | `login_required`, `admin_required` |
| Interactive CLI | `main.py` |
| Validation | `validators.py`, `AuthManager`, `BookCLI` |
| Error handling | `try/except`, validation errors, JSON handling |
| Registration | `AuthManager.register()` |
| Login | `AuthManager.login()` |
| Password hashing | `User.hash_password()` |
| Role-based access | User/Admin menus and `@admin_required` |
| Requirements file | `requirements.txt` |

---

# 27. Common Questions a Student May Be Asked

## Why did you use classes?

Classes help group related data and behavior. For example, a Book object keeps a book's title, author, genre, and status together.

## Where is inheritance used?

`Admin` inherits from `User`.

```python
class Admin(User):
```

## Where is encapsulation used?

The password hash is stored as:

```python
self.__password_hash
```

inside the `User` class.

## Why use JSON?

JSON provides simple file-based persistence and does not require installing or configuring a database.

## Why have `BookCollection` instead of putting everything in Book?

A Book represents one book. A BookCollection manages operations involving many books.

## Why use decorators?

Decorators let authentication rules be written once and reused on several CLI methods.

## Why does `login()` return a User object?

The CLI needs to know which user is currently logged in. The returned object provides the user's name, email, and role.

## How does role-based access work?

The logged-in User has a `role` attribute. Admin-only functions use `@admin_required` to check that the role is `admin`.

## What happens when the program closes?

Python objects disappear from memory, but saved JSON data remains on disk and is loaded again later.

---

# 28. Limitations and Possible Future Improvements

The project intentionally avoids advanced features.

Possible future improvements include:

- Use bcrypt or Argon2 for production-grade password hashing.
- Prevent public users from choosing the Admin role.
- Give every book a unique ID.
- Allow users to edit book details.
- Track which books belong to individual users.
- Add borrowing and return dates.
- Replace JSON with PostgreSQL.
- Add a web or graphical interface.

These improvements are **not required** for the current project. The current version is deliberately small so that the main Python and OOP concepts remain easy to understand.

---

# 29. Final Summary

The Book Collection Manager demonstrates how a relatively small Python project can combine several important programming ideas.

The main flow is:

```text
User starts CLI
      |
      v
Register / Login
      |
      v
User or Admin object
      |
      v
Book menu
      |
      v
BookCollection
      |
      v
JSON storage
```

The key OOP ideas are:

```text
Classes       -> User, Book, BookCollection, AuthManager, BookCLI
Inheritance   -> Admin inherits from User
Encapsulation -> private password hash
Interaction   -> BookCLI uses AuthManager and BookCollection
```

The result is intentionally straightforward: enough structure to demonstrate good Python design, but not so much structure that the project becomes difficult for a beginner to explain.
