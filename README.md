# ЛР3 — «Треугольник» (интеграционное тестирование и заглушки)

Весь код — в `main.py`, все тесты — в `tests/test_main.py`.

Классы: `Calculator` (метод из ЛР1), `Database` (SQLite: add/get/delete),
`UserInterface` + `ConsoleUI` (ввод, ABC), `Notifier` + `ServerNotifier`
(отправка, ABC), `Controller` (ввод → БД или расчёт → сохранение → отправка → результат).

```text
main.py              # весь код
tests/test_main.py   # 5 тестов (3 интеграционных)
tests/__init__.py
README.md
```

```bash
python main.py
python -m unittest discover -v
```

Заглушки: `mock.patch("builtins.input")` (ввод), `Mock` (сервер),
проверка «без пересчёта» через подмену калькулятора.