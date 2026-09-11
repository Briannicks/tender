import unittest

from models.user import Admin, User
from utils.decorators import admin_required, login_required


class FakeApp:
    def __init__(self, current_user=None):
        self.current_user = current_user

    @login_required
    def user_action(self):
        return "user action"

    @admin_required
    def admin_action(self):
        return "admin action"


class DecoratorTests(unittest.TestCase):
    def test_login_required_blocks_guest(self):
        app = FakeApp()
        self.assertIsNone(app.user_action())

    def test_login_required_allows_logged_in_user(self):
        user = User("Jane", "jane@example.com", User.hash_password("pass"))
        app = FakeApp(user)
        self.assertEqual(app.user_action(), "user action")

    def test_admin_required_blocks_normal_user(self):
        user = User("Jane", "jane@example.com", User.hash_password("pass"))
        app = FakeApp(user)
        self.assertIsNone(app.admin_action())

    def test_admin_required_allows_admin(self):
        admin = Admin("Admin", "admin@example.com", User.hash_password("pass"))
        app = FakeApp(admin)
        self.assertEqual(app.admin_action(), "admin action")


if __name__ == "__main__":
    unittest.main()
