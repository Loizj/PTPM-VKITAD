import unittest
from unittest.mock import Mock, patch

from main import (
    Calculator,
    ConsoleUI,
    Controller,
    Database,
    Notifier,
    ServerNotifier,
    UserInterface,
)


def new_controller():
    """Собирает контроллер с реальными Calculator и Database и заглушками."""
    db = Database()
    ui, sender = Mock(), Mock()
    return Controller(Calculator(), db, ui, sender), db, sender


class TestController(unittest.TestCase):
    def test_new_input_is_computed_stored_and_sent(self):
        c, db, sender = new_controller()
        c.ui.get_sides.return_value = ("7", "8", "9")

        self.assertEqual(c.run(), "разносторонний")
        self.assertEqual(db.get("7", "8", "9"), ("разносторонний", ""))
        sender.send.assert_called_once_with("разносторонний")

    def test_existing_record_is_taken_from_database(self):
        c, db, _ = new_controller()
        db.add("5", "5", "5", "равносторонний", "")
        c.ui.get_sides.return_value = ("5", "5", "5")
        c.calc = Mock()

        self.assertEqual(c.run(), "равносторонний")
        c.calc.solve.assert_not_called()

    def test_error_is_stored_and_sent(self):
        c, db, sender = new_controller()
        c.ui.get_sides.return_value = ("1", "1", "3")

        self.assertEqual(c.run(), "не треугольник")
        self.assertEqual(db.get("1", "1", "3"), ("не треугольник", ""))
        sender.send.assert_called_once_with("не треугольник")


class TestUnit(unittest.TestCase):
    def test_calculator(self):
        s = Calculator().solve
        self.assertEqual(s("5", "5", "5"), "равносторонний")
        self.assertEqual(s("6", "6", "10"), "равнобедренный")
        self.assertEqual(s("7", "8", "9"), "разносторонний")
        self.assertEqual(s("1", "1", "3"), "не треугольник")
        self.assertEqual(s("x", "1", "3"), "некорректный ввод")

    def test_database_and_interfaces(self):
        db = Database()
        db.add("3", "4", "5", "разносторонний", "")
        self.assertEqual(db.get("3", "4", "5"), ("разносторонний", ""))
        self.assertIsNone(db.get("1", "2", "3"))
        self.assertEqual(db.delete("3", "4", "5"), 1)
        self.assertIsNone(db.get("3", "4", "5"))

        for cls in (UserInterface, Notifier):
            with self.assertRaises(TypeError):
                cls()
        with patch("builtins.input", side_effect=["3", "4", "5"]):
            self.assertEqual(ConsoleUI().get_sides(), ("3", "4", "5"))
        ServerNotifier().send("привет")


if __name__ == "__main__":
    unittest.main()