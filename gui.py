import tkinter as tk
from tkinter import ttk, messagebox

from queries.query_date import execute_query_date
from queries.query_show_plays import show_plays
from queries.query_tickets import execute_query_tickets
from queries.query_price_ticket import execute_query_price_ticket
from queries.query_show_tickets import execute_query_show_tickets


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Театральная касса")
        self.geometry("800x400")

        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self, text="Какую информацию желаете получить?")
        self.label.pack(pady=15)

        self.button1 = ttk.Button(
            self,
            text="Какие спектакли идут в определенный день?",
            command=self.open_form1,
        )
        self.button2 = ttk.Button(
            self,
            text="Есть ли билеты на конкретный спектакль?",
            command=self.open_form2,
        )
        self.button3 = ttk.Button(
            self, text="Сколько стоит конкретный билет?", command=self.open_form3
        )

        self.button1.pack(pady=20)
        self.button2.pack(pady=20)
        self.button3.pack(pady=20)

    def open_form1(self):
        # Создаем форму
        form_window = tk.Toplevel(self)
        form_window.title("Какие спектакли идут в определенный день?")
        form_window.geometry("800x400")

        tk.Label(form_window, text="Введите нужную дату в формате ГГГГ-ММ-ДД:").pack(
            pady=5
        )
        date_entry = ttk.Entry(form_window, width=40)
        date_entry.pack(pady=10)

        # Кнопка для отправки формы
        submit_button = ttk.Button(
            form_window,
            text="Отправить",
            command=lambda: self.submit_form(param=1, date_entry=date_entry),
        )
        submit_button.pack(pady=10)

    def open_form2(self):
        # Создаем форму
        form_window = tk.Toplevel(self)
        form_window.title("Есть ли билеты на конкретный спектакль?")
        form_window.geometry("800x400")

        tk.Label(
            form_window,
            text="Введите номер нужного спектакля и нужную дату в формате ГГГГ-ММ-ДД",
        ).pack(pady=5)

        entry_frame = ttk.Frame(form_window)
        entry_frame.pack(pady=10)

        play_id_entry = ttk.Entry(entry_frame, width=5)
        play_id_entry.grid(row=0, column=0, padx=(0, 10))

        date_entry = ttk.Entry(entry_frame, width=20)
        date_entry.grid(row=0, column=1, padx=(0, 10))

        button_play1 = ttk.Button(
            entry_frame,
            text="Подтвердить",
            command=lambda: self.submit_form(
                param=2, play_id_entry=play_id_entry, date_entry=date_entry
            ),
        )
        button_play1.grid(row=0, column=2)

        # Вывод таблицы спектаклей

        results = show_plays()

        if results:
            self.tree = ttk.Treeview(
                form_window, columns=("play_id", "title", "author"), show="headings"
            )
            self.tree.heading("play_id", text="Номер")
            self.tree.heading("title", text="Название")
            self.tree.heading("author", text="Автор")
            self.tree.pack(expand=True, fill="both")
            # Заполняем таблицу новыми данными
            for row in results:
                self.tree.insert("", "end", values=row)
        else:
            # Если результатов нет, добавляем строку с сообщением
            self.tree.insert("", "end", values=("Cпектаклей нет", "", ""))

    def open_form3(self):
        # Создаем форму
        form_window = tk.Toplevel(self)
        form_window.title("Сколько стоит конкретный билет?")
        form_window.geometry("2000x400")

        tk.Label(form_window, text="Введите номер нужного билета").pack(pady=5)

        entry_frame = ttk.Frame(form_window)
        entry_frame.pack(pady=10)

        ticket_id_entry = ttk.Entry(entry_frame, width=5)
        ticket_id_entry.grid(row=0, column=0, padx=(0, 10))

        button_play1 = ttk.Button(
            entry_frame,
            text="Подтвердить",
            command=lambda: self.submit_form(param=3, ticket_id_entry=ticket_id_entry),
        )
        button_play1.grid(row=0, column=1)

        # Вывод таблицы билетов

        results = execute_query_show_tickets()

        if results:
            self.tree = ttk.Treeview(
                form_window,
                columns=(
                    "ticket_id",
                    "row_number",
                    "title",
                    "author",
                    "showing_date",
                    "name_theater",
                ),
                show="headings",
            )
            self.tree.heading("ticket_id", text="Номер")
            self.tree.heading("row_number", text="Номер ряда")
            self.tree.heading("title", text="Название")
            self.tree.heading("author", text="Автор")
            self.tree.heading("showing_date", text="Дата")
            self.tree.heading("name_theater", text="Театр")

            self.tree.pack(expand=True, fill="both")

            # Заполняем таблицу новыми данными
            for row in results:
                self.tree.insert("", "end", values=row)
        else:
            # Если результатов нет, добавляем строку с сообщением
            self.tree.insert("", "end", values=("Билетов нет", "", ""))

    def submit_form(
        self, param, date_entry=None, play_id_entry=None, ticket_id_entry=None
    ):
        match param:
            case 1:
                date = date_entry.get()
                results = execute_query_date(date)

                results_window = tk.Toplevel(self)
                results_window.title("Спектакли в выбранный день")
                results_window.geometry("600x400")

                if results:
                    tree = ttk.Treeview(
                        results_window,
                        columns=("title", "author", "theater"),
                        show="headings",
                    )
                    tree.heading("title", text="Название")
                    tree.heading("author", text="Автор")
                    tree.heading("theater", text="Театр")

                    # Добавляем данные в таблицу
                    for row in results:
                        tree.insert("", "end", values=row)

                    tree.pack(expand=True, fill="both")
                else:
                    tk.Label(results_window, text="В этот день спектаклей нет").pack(
                        pady=20
                    )

                tree.pack(expand=True, fill="both")

            case 2:
                play_id = play_id_entry.get()
                date = date_entry.get()
                results = execute_query_tickets(play_id, date)

                results_window = tk.Toplevel(self)
                results_window.title("Билеты")
                results_window.geometry("600x400")

                if results:
                    tree = ttk.Treeview(
                        results_window,
                        columns=("count_tickets", "theater"),
                        show="headings",
                    )
                    tree.heading("count_tickets", text="Количество билетов")
                    tree.heading("theater", text="Театр")

                    # Добавляем данные в таблицу
                    for row in results:
                        tree.insert("", "end", values=row)

                    tree.pack(expand=True, fill="both")
                else:
                    tk.Label(
                        results_window, text="В этот день спектаклей нигде нет"
                    ).pack(pady=20)

                tree.pack(expand=True, fill="both")

            case 3:
                ticket_id = ticket_id_entry.get()
                results = execute_query_price_ticket(ticket_id)

                results_window = tk.Toplevel(self)
                results_window.title("Стоимость выбранного билета")
                results_window.geometry("600x400")

                if results:
                    results_num = results[0][
                        0
                    ]  # Доступ к первому элементу списка и кортежа
                    # Преобразуем Decimal в строку (если нужно)
                    results_num = str(results_num)
                    tk.Label(results_window, text=f"{results_num} $").pack(pady=20)
                else:
                    tk.Label(results_window, text="Ошибка").pack(pady=10)
