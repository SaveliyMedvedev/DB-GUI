import tkinter as tk
from tkinter import ttk, messagebox

import queries


class DateForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Какие спектакли идут в определенный день?")
        self.geometry("800x400")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Введите нужную дату в формате ГГГГ-ММ-ДД:").pack(pady=5)
        self.date_entry = ttk.Entry(self, width=40)
        self.date_entry.pack(pady=10)
        submit_button = ttk.Button(self, text="Отправить", command=self.submit_form)
        submit_button.pack(pady=10)

    def submit_form(self):
        date = self.date_entry.get()
        results = queries.execute_query_date(date)
        self.display_results(results)

    def display_results(self, results):
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
            tk.Label(results_window, text="В этот день спектаклей нет").pack(pady=20)

        tree.pack(expand=True, fill="both")


class TicketsForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Есть ли билеты на конкретный спектакль?")
        self.geometry("800x400")
        self.create_widgets()

    def create_widgets(self):

        form_window = tk.Toplevel(self)
        form_window.title("Есть ли билеты на конкретный спектакль?")
        form_window.geometry("800x400")

        tk.Label(
            self,
            text="Введите номер нужного спектакля и нужную дату в формате ГГГГ-ММ-ДД",
        ).pack(pady=5)

        self.entry_frame = ttk.Frame(self)
        self.entry_frame.pack(pady=10)

        self.play_id_entry = ttk.Entry(self.entry_frame, width=5)
        self.play_id_entry.grid(row=0, column=0, padx=(0, 10))

        self.date_entry = ttk.Entry(self.entry_frame, width=20)
        self.date_entry.grid(row=0, column=1, padx=(0, 10))

        button_play = ttk.Button(
            self.entry_frame,
            text="Подтвердить",
            command=self.submit_form,
        )
        button_play.grid(row=0, column=2)

        # Вывод таблицы спектаклей

        results = queries.show_plays()

        if results:
            self.tree = ttk.Treeview(
                self, columns=("play_id", "title", "author"), show="headings"
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

    def submit_form(self):
        play_id = self.play_id_entry.get()
        date = self.date_entry.get()
        results = queries.execute_query_tickets(play_id, date)

        self.display_results(results)

    def display_results(self, results):
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
            tk.Label(results_window, text="В этот день спектаклей нигде нет").pack(
                pady=20
            )

        tree.pack(expand=True, fill="both")


class PriceTicketForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Сколько стоит конкретный билет?")
        self.geometry("2000x400")
        self.create_widgets()

    def create_widgets(self):

        form_window = tk.Toplevel(self)
        form_window.title("Сколько стоит конкретный билет?")
        form_window.geometry("2000x400")

        tk.Label(self, text="Введите номер нужного билета").pack(pady=5)

        self.entry_frame = ttk.Frame(self)
        self.entry_frame.pack(pady=10)

        self.ticket_id_entry = ttk.Entry(self.entry_frame, width=5)
        self.ticket_id_entry.grid(row=0, column=0, padx=(0, 10))

        button_play = ttk.Button(
            self.entry_frame,
            text="Подтвердить",
            command=self.submit_form,
        )
        button_play.grid(row=0, column=1)

        # Вывод таблицы билетов

        results = queries.execute_query_show_tickets()

        if results:
            self.tree = ttk.Treeview(
                self,
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

    def submit_form(self):
        ticket_id = self.ticket_id_entry.get()
        results = queries.execute_query_price_ticket(ticket_id)

        self.display_results(results)

    def display_results(self, results):
        results_window = tk.Toplevel(self)
        results_window.title("Стоимость выбранного билета")
        results_window.geometry("600x400")

        if results:
            results_num = results[0][0]
            # Доступ к первому элементу списка и кортежа
            # Преобразуем Decimal в строку (если нужно)
            results_num = str(results_num)
            tk.Label(results_window, text=f"{results_num} $").pack(pady=20)
        else:
            tk.Label(results_window, text="Ошибка").pack(pady=10)


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
            command=self.open_date_form,
        ).pack(pady=20)

        self.button2 = ttk.Button(
            self,
            text="Есть ли билеты на конкретный спектакль?",
            command=self.open_tickets_form,
        ).pack(pady=20)

        self.button3 = ttk.Button(
            self,
            text="Сколько стоит конкретный билет?",
            command=self.open_price_ticket_form,
        ).pack(pady=20)

    def open_date_form(self):
        DateForm(self)

    def open_tickets_form(self):
        TicketsForm(self)

    def open_price_ticket_form(self):
        PriceTicketForm(self)
