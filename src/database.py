import sqlite3

# CRUD - Create, Read, Update, Delete
class Database:
    """
    Класс для работы с БД. тут будут методы для создания таблиц,
    для добавления, обновления и удаления контактов(таблица contacts)
    """
    def __init__(self, path):
        self.path = path

    def create_tables(self):
        """
        Метод, в котором описывается, какие таблицы и с какими колонками создаются для приложения
        """
        with sqlite3.connect(self.path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    note TEXT
                )
            """)

    def count_contacts(self):
        """
        Метод, в котором вызывается запрос для получения количества контактов из БД
        """
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            result = cursor.execute("SELECT COUNT(*) FROM contacts")
            # (0)
            return result.fetchone()[0]

    def all_contacts(self):
        """
        Метод, в котором вызывается запрос для получения всех контактов из БД
        """
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            result = cursor.execute("SELECT * FROM contacts")
            return result.fetchall()

    def get_contact(self, contact_id):
        """
        Метод, в котором вызывается запрос для получения конкретного контакта из БД
        """
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            result = cursor.execute("SELECT * FROM contacts WHERE id=(?)", (contact_id,))
            # (1, 'Иван Иванов', '+7-123-456-78-90', 'Друг')
            return result.fetchone()

    def add_contact(self, name: str, phone: str, note: str = ""):
        """
        Метод, в котором вызывается запрос для добавления в БД нового контакта
        """
        print(name, phone, note, "in database add_contact")
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                INSERT INTO contacts (name, phone, note) VALUES
                (?, ?, ?)
                """,
                (name, phone, note),
            )
            # так делать неправильно:
            # conn.execute(
            #     f"INSERT INTO contacts (name, phone, note) VALUES ({name}, {phone}, {note})",
            # )
            conn.commit()

    def update_contact(self, contact_id: int, name: str, phone: str, note: str = ""):
        """
        Метод, в котором вызывается запрос для обновления контакта
        """
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                UPDATE contacts SET name = ?, phone = ?, note = ? WHERE
                id = ?
                """,
                (name, phone, note, contact_id),
            )
            conn.commit()

    def delete_contact(self, contact_id):
        """
        Метод, в котором вызывается запрос для удаления контакта
        """
        with sqlite3.connect(self.path) as conn:
            conn.execute("DELETE FROM contacts WHERE id=(?)", (contact_id,))
            conn.commit()