"""ЛР3. Проект «Треугольник». Запуск: python main.py | Тесты: python -m unittest discover -v"""

import sqlite3
from abc import ABC, abstractmethod


class Calculator:
    """a. Вычисления: тип треугольника (метод из ЛР1, без координат)."""

    def solve(self, s1, s2, s3):
        try:
            a, b, c = float(s1), float(s2), float(s3)
        except ValueError:
            return "некорректный ввод"
        if not (a > 0 and b > 0 and c > 0 and a + b > c and a + c > b and b + c > a):
            return "не треугольник"
        if a == b == c:
            return "равносторонний"
        if a == b or b == c or a == c:
            return "равнобедренный"
        return "разносторонний"


class Database:
    """b. БД SQLite: add / get / delete (ключ записи — три длины сторон)."""

    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS triangles ("
            "s1 TEXT, s2 TEXT, s3 TEXT, kind TEXT, error TEXT, "
            "PRIMARY KEY (s1, s2, s3))"
        )

    def add(self, s1, s2, s3, kind, error):
        self.conn.execute(
            "INSERT OR REPLACE INTO triangles VALUES (?, ?, ?, ?, ?)",
            (s1, s2, s3, kind, error),
        )
        self.conn.commit()

    def get(self, s1, s2, s3):
        return self.conn.execute(
            "SELECT kind, error FROM triangles WHERE s1=? AND s2=? AND s3=?",
            (s1, s2, s3),
        ).fetchone()

    def delete(self, s1, s2, s3):
        cursor = self.conn.execute(
            "DELETE FROM triangles WHERE s1=? AND s2=? AND s3=?",
            (s1, s2, s3),
        )
        self.conn.commit()
        return cursor.rowcount


class UserInterface(ABC):
    """c. Интерфейс взаимодействия с пользователем."""

    @abstractmethod
    def get_sides(self):
        pass


class ConsoleUI(UserInterface):
    def get_sides(self):
        return (
            input("Первая сторона: "),
            input("Вторая сторона: "),
            input("Третья сторона: "),
        )


class Notifier(ABC):
    """d. Интерфейс сторонней зависимости (отправка результата)."""

    @abstractmethod
    def send(self, message):
        pass


class ServerNotifier(Notifier):
    """Имитация отправки на внешний сервер."""

    def send(self, message):
        print("Отправлено на сервер:", message)


class Controller:
    """e. Сквозная логика: ввод → БД или расчёт → отправка → результат."""

    def __init__(self, calc, db, ui, notifier):
        self.calc = calc
        self.db = db
        self.ui = ui
        self.notifier = notifier

    def run(self):
        s1, s2, s3 = self.ui.get_sides()
        row = self.db.get(s1, s2, s3)
        if row is None:
            result = self.calc.solve(s1, s2, s3)
            self.db.add(s1, s2, s3, result, "")
        else:
            result = row[0]
        self.notifier.send(result)
        return result


def main():
    print(Controller(Calculator(), Database(), ConsoleUI(), ServerNotifier()).run())


if __name__ == "__main__":
    main()