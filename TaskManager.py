import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QAbstractItemView,
    QMessageBox,
    QComboBox,
    QTableWidgetItem,
)
from task_scheduler import TaskScheduler  # Импортируем класс TaskScheduler
from datetime import datetime


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Таск Менеджер")
        self.setMinimumWidth(750)

        self.scheduler = TaskScheduler("scheduler.db")
        main_layout = QVBoxLayout()

        # Верхняя часть
        top_layout = QVBoxLayout()
        self.create_input_fields(top_layout)  # Создаем поля ввода
        self.create_buttons(top_layout)        # Создаем кнопки
        self.create_search_button(top_layout)  # Создаем кнопку поиска
        main_layout.addLayout(top_layout)

        # Средняя часть
        mid_layout = QHBoxLayout()
        self.create_middle_section(mid_layout)  # Создаем среднюю секцию
        main_layout.addLayout(mid_layout)

        # Нижняя часть
        bottom_layout = QVBoxLayout()
        self.create_table(bottom_layout)        # Создаем таблицу
        self.create_delete_button(bottom_layout)  # Создаем кнопку удалить
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)
        self.load_tasks()  # Загружаем задачи при запуске

    def create_search_button(self, layout: QVBoxLayout) -> None:
        """Поиск по таблице."""
        # Добавление текстового поля для поиска
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск...")
        layout.addWidget(self.search_input)

        search_button = QPushButton("Поиск")
        layout.addWidget(search_button)
        search_button.clicked.connect(self.search_tasks)

    def search_tasks(self) -> None:
        """Ищет задачи по введенному тексту в любом поле таблицы."""
        search_text = self.search_input.text().lower()  # текст для поиска
        found_rows = []  # Список для найденных строк

        for row in range(self.table.rowCount()):
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                if item and search_text in item.text().lower():
                    found_rows.append(row)
                    break  # Если нашли, выходим из внутреннего цикла

        # Скрываем все строки, а затем показываем только найденные
        for row in range(self.table.rowCount()):
            self.table.setRowHidden(row, True)

        for row in found_rows:
            self.table.setRowHidden(row, False)

    def create_delete_button(self, layout: QVBoxLayout) -> None:
        """Создает кнопку для удаления выбранной задачи."""
        delete_button = QPushButton("Удалить")
        layout.addWidget(delete_button)

        # Подключаем кнопку удаления к методу delete_task
        delete_button.clicked.connect(self.delete_task)

    def create_input_fields(self, layout: QVBoxLayout) -> None:
        """Создает поля ввода и соответствующие метки."""
        # Список надписей на метках
        labels = ["ИД", "Имя задачи",
                  "Описание", "Приоритет", "Статус", "Дедлайн", "Комментарий"]

        # Создаем текстовые поля и комбобоксы
        self.id_input = QLineEdit()  # ИД
        self.id_input.setDisabled(True)  # Поле ИД недоступно
        self.task_name_input = QLineEdit()  # Имя задачи
        self.description_input = QLineEdit()  # Описание
        self.priority_combo = QComboBox()  # Приоритет
        self.priority_combo.addItems(["низкий", "средний", "высокий"])
        self.status_combo = QComboBox()  # Статус
        self.status_combo.addItems(["новая задача", "в работе",
                                    "отменена", "решено"])

        # Устанавливаем маску для поля "Дедлайн"
        self.deadline_input = QLineEdit()  # Дедлайн
        self.deadline_input.setInputMask("9999-99-99;_")  # дата ГГГГ-ММ-ДД
        self.comment_input = QLineEdit()  # Комментарий

        # Создаем горизонтальные Layout для размещения меток и полей
        for i, label in enumerate(labels):
            input_layout = QHBoxLayout()  # Новый layout для метки и поля
            input_layout.addWidget(QLabel(label))  # Добавляем метку

            # Условие для выбора соответствующего поля ввода
            if i == 0:
                input_widget = self.id_input
            elif i == 1:
                input_widget = self.task_name_input
            elif i == 2:
                input_widget = self.description_input
            elif i == 3:
                input_widget = self.priority_combo
            elif i == 4:
                input_widget = self.status_combo
            elif i == 5:
                input_widget = self.deadline_input
            else:  # Комментарий
                input_widget = self.comment_input

            input_widget.setDisabled(True)  # все текстовые поля недоступны
            input_layout.addWidget(input_widget)  # Добавляем поле ввода
            layout.addLayout(input_layout)  # Добавляем в вертикальный

    def create_buttons(self, layout: QVBoxLayout) -> None:
        """Создает кнопки в верхней части."""
        button_layout = QHBoxLayout()

        # Создание кнопок
        self.new_task_button = QPushButton("Новая задача")
        self.edit_button = QPushButton("Редактировать")
        self.cancel_button = QPushButton("Отмена")
        self.save_button = QPushButton("Сохранить")

        # По умолчанию кнопка отмены и сохранения неактивны
        self.cancel_button.setDisabled(True)
        self.save_button.setDisabled(True)

        # Подключение сигналов к слотам
        self.new_task_button.clicked.connect(self.new_task)
        self.edit_button.clicked.connect(self.edit_task)
        self.cancel_button.clicked.connect(self.cancel_task)
        self.save_button.clicked.connect(self.save_task)  # сохраняет в БД

        # Добавляем кнопки на layout
        button_layout.addWidget(self.new_task_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)

        layout.addLayout(button_layout)

    def new_task(self) -> None:
        """Создает новую задачу."""
        for input_field in [self.task_name_input,
                            self.description_input,
                            self.deadline_input,
                            self.comment_input]:
            input_field.clear()
            input_field.setEnabled(True)  # Делаем поля доступными для записи

        self.priority_combo.setEnabled(True)  # Активируем выбор приоритета
        self.status_combo.setEnabled(True)    # Активируем выбор статуса

        self.cancel_button.setEnabled(True)    # Активируем кнопку отмены
        self.save_button.setEnabled(True)      # Активируем кнопку сохранить

    def edit_task(self) -> None:
        """Редактирует существующую задачу."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите задачу.")
            return

        task_data = [self.table.item(selected_row, i).text() for i in range(7)]

        # Заполняем поля ввода данными задачи
        self.id_input.setText(task_data[0])  # ИД, поле не редактируется
        self.task_name_input.setText(task_data[1])
        self.description_input.setText(task_data[2])
        self.priority_combo.setCurrentText(task_data[3])
        self.status_combo.setCurrentText(task_data[4])
        self.deadline_input.setText(task_data[5])
        self.comment_input.setText(task_data[6])

        # Делаем поля доступными для редактирования
        for input_field in [self.task_name_input,
                            self.description_input,
                            self.deadline_input,
                            self.comment_input]:
            input_field.setEnabled(True)

        # Активируем выбор для комбобоксов
        self.priority_combo.setEnabled(True)
        self.status_combo.setEnabled(True)

        self.cancel_button.setEnabled(True)    # Активируем кнопку отмены
        self.save_button.setEnabled(True)      # Активируем кнопку сохранить

    def cancel_task(self) -> None:
        """Отменяет изменения с подтверждением."""
        for input_field in [self.task_name_input,
                            self.description_input,
                            self.deadline_input, self.comment_input]:
            input_field.clear()
            input_field.setDisabled(True)  # Делаем поля недоступными

        # Сброс значений для комбобоксов
        self.priority_combo.setCurrentIndex(0)
        self.priority_combo.setDisabled(True)  # Деактивируем выбор приоритета
        self.status_combo.setCurrentIndex(0)
        self.status_combo.setDisabled(True)    # Деактивируем выбор статуса

        self.cancel_button.setDisabled(True)    # Деактивируем кнопку отмены
        self.save_button.setDisabled(True)      # Деактивируем кнопку сохранить

    def save_task(self) -> None:
        """Сохраняет задачу и взаимодействует с базой данных."""

        task_name = self.task_name_input.text()
        description = self.description_input.text()
        priority = self.priority_combo.currentText()
        status = self.status_combo.currentText()
        deadline = self.deadline_input.text()
        comment = self.comment_input.text()

        date_object = datetime.strptime(deadline, "%Y-%m-%d").date()
        if date_object >= datetime.now().date():

            # Если редактируем задачу
            if self.table.currentRow() >= 0:
                record_id = int(self.table.item(
                    self.table.currentRow(), 0).text())
                self.scheduler.update_task(record_id,
                                           task_name, description,
                                           priority, status, deadline, comment)
            else:  # Если создаем новую задачу
                self.scheduler.add_task(task_name, description,
                                        priority, status, deadline, comment)

            self.load_tasks()  # Обновляем таблицу задач
            self.cancel_task()  # Деактивируем изменения
        else:
            QMessageBox.warning(self, "Ошибка", "Не корректная дата дедлайна.")

    def load_tasks(self) -> None:
        """Загружает и отображает все задачи из базы данных в таблице."""
        tasks = self.scheduler.get_all_tasks()
        self.table.setRowCount(0)  # Очищаем таблицу

        for task in tasks:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for col, value in enumerate(task):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row_position, col, item)

    def delete_task(self) -> None:
        """Удаляет выбранную задачу из таблицы и базы данных."""
        selected_row = self.table.currentRow()  # Получаем выбранную строку
        if selected_row < 0:
            # Предупреждение при отсутствии выбора
            QMessageBox.warning(self, "Ошибка", "Сначала выберите задачу.")
            return

        # Получаем ИД задачи для удаления
        record_id = int(self.table.item(selected_row, 0).text())
        self.scheduler.delete_task(record_id)  # Вызываем метод удаления

    # Обновляем таблицу задач после удаления
        self.load_tasks()

    def create_middle_section(self, layout: QHBoxLayout) -> None:
        """Создает среднюю секцию с полем ввода и кнопкой."""
        pass

    def create_table(self, layout: QVBoxLayout) -> None:
        """Создает таблицу в нижней части."""
        self.table = QTableWidget(0, 7)  # Начинаем с 0 строк и 7 колонок
        self.table.setHorizontalHeaderLabels(
            ["ИД", "Имя задачи", "Описание",
             "Приоритет", "Статус", "Дедлайн", "Комментарий"]
        )

        # Установить режим выделения для целых строк
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        # Подключаем заполнение полей
        self.table.itemClicked.connect(self.populate_fields_from_selection)

        layout.addWidget(self.table)

    def populate_fields_from_selection(self, item) -> None:
        """Заполняет поля данными из выделенной строки таблицы."""
        selected_row = self.table.currentRow()
        task_data = [self.table.item(selected_row, i).text() for i in range(7)]

        self.id_input.setText(task_data[0])  # ИД
        self.task_name_input.setText(task_data[1])
        self.description_input.setText(task_data[2])
        self.priority_combo.setCurrentText(task_data[3])
        self.status_combo.setCurrentText(task_data[4])
        self.deadline_input.setText(task_data[5])
        self.comment_input.setText(task_data[6])

        # Делаем поля недоступными
        for input_field in [self.task_name_input,
                            self.description_input,
                            self.deadline_input, self.comment_input]:
            input_field.setDisabled(True)

        self.priority_combo.setEnabled(False)  # Деактивируем выбор приоритета
        self.status_combo.setEnabled(False)    # Деактивируем выбор статуса


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
