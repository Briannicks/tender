import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from main import BookCLI
from models.book import Book


class CLITests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        folder = Path(self.temp_dir.name)
        self.cli = BookCLI(folder / "users.json", folder / "books.json")

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch("builtins.input", side_effect=["Jane", "jane@example.com", "secret123", "user"])
    def test_register_sets_current_user(self, _):
        self.cli.register()
        self.assertIsNotNone(self.cli.current_user)
        self.assertEqual(self.cli.current_user.email, "jane@example.com")

    @patch("builtins.input", side_effect=["jane@example.com", "secret123"])
    def test_login_sets_current_user(self, _):
        self.cli.auth.register("Jane", "jane@example.com", "secret123", "user")
        self.cli.login()
        self.assertEqual(self.cli.current_user.name, "Jane")

    @patch("builtins.input", side_effect=["1984", "George Orwell", "Fiction"])
    def test_add_book_for_logged_in_user(self, _):
        self.cli.current_user = self.cli.auth.register("Jane", "jane@example.com", "secret123", "user")
        self.cli.add_book()
        self.assertEqual(len(self.cli.collection.view_books()), 1)

    @patch("builtins.input", side_effect=["1984"])
    def test_admin_can_delete_book(self, _):
        self.cli.current_user = self.cli.auth.register("Admin", "admin@example.com", "secret123", "admin")
        self.cli.collection.add_book(Book("1984", "George Orwell", "Fiction"))
        self.cli.delete_book()
        self.assertEqual(self.cli.collection.view_books(), [])


if __name__ == "__main__":
    unittest.main()
