import sqlite3
from sqlite3 import Error


class DB_Connector:
    def __init__(self, db_file):
        """Инициализация подключения к базе данных."""
        self.connection = self.create_connection(db_file)
        self.create_table()

    def create_connection(self, db_file):
        """Создает соединение с указанной базой данных SQLite."""
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
        except Error as e:
            print(f"Ошибка '{e}' произошла при подключении к БД.")
        return self.conn

    def create_table(self):
        """Создает таблицу Scheduler, если она не существует."""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS Scheduler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            description TEXT,
            priority TEXT,
            status TEXT,
            deadline TEXT,
            comment TEXT,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(create_table_sql)

        except Error as ex:
            print(f"Ошибка '{ex}' произошла при создании таблицы.")

    def add_record(self,
                   task_name,
                   description, priority, status, deadline, comment):
        """Добавляет запись в таблицу Scheduler."""
        sql = """INSERT INTO Scheduler (
            task_name, description, priority, status, deadline, comment
            )
                 VALUES (?, ?, ?, ?, ?, ?)"""
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql, (
                task_name, description, priority, status, deadline, comment
                ))
            self.connection.commit()
            print("Запись успешно добавлена.")
        except Error as ex:
            print(f"Ошибка '{ex}' произошла при добавлении записи.")

    def delete_record(self, record_id):
        """Удаляет запись из таблицы Scheduler по id."""
        sql = """DELETE FROM Scheduler WHERE id = ?"""
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql, (record_id,))
            self.connection.commit()
            print("Запись успешно удалена.")
        except Error as ex:
            print(f"Ошибка '{ex}' произошла при удалении записи.")

    def update_record(self, record_id,
                      task_name, description, priority, status,
                      deadline, comment):
        """Обновляет запись в таблице Scheduler."""
        sql = """UPDATE Scheduler
                 SET task_name = ?, description = ?, priority = ?, status = ?,
                 deadline = ?, comment = ?
                 WHERE id = ?"""
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql, (
                task_name, description,
                priority, status, deadline, comment, record_id
                ))
            self.connection.commit()
            print("Запись успешно обновлена.")
        except Error as ex:
            print(f"Ошибка '{ex}' произошла при обновлении записи.")

    def get_all_records(self):
        """Возвращает все записи из таблицы Scheduler."""
        sql = """SELECT * FROM Scheduler ORDER BY deadline"""
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
            records = self.cursor.fetchall()
            return records
        except Error as ex:
            print(f"Ошибка '{ex}' произошла при получении всех записей.")
            return []

    def get_records_by_params(self, **params):
        """Возвращает записи из таблицы Scheduler по указанным параметрам."""
        query = "SELECT * FROM Scheduler WHERE "
        conditions = []
        values = []

        for key, value in params.items():
            conditions.append(f"{key} = ?")
            values.append(value)

        query += " AND ".join(conditions)

        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(query, values)
            records = self.cursor.fetchall()
            return records
        except Error as e:
            print(f"Ошибка '{e}' произошла при получении записей.")
            return []

    def close_connection(self):
        """Закрывает соединение с базой данных."""
        if self.connection:
            self.connection.close()
            print("Соединение с базой данных закрыто.")


if __name__ == '__main__':
    connector = DB_Connector('TaskManager.db')
    connector.create_connection('TaskManager.db')
