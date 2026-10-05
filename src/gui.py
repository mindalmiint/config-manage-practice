"""Графический интерфейс эмулятора оболочки на Tkinter."""

import tkinter as tk
from tkinter import scrolledtext
import getpass
import socket
from parser import parse_command
from commands import execute_command


class ShellEmulatorGUI:
    """Эмулятор оболочки с графическим интерфейсом.

    Реализует REPL-цикл: чтение ввода пользователя, разбор
    команды, выполнение, печать результата и вывод нового
    приглашения. Работает на базе Tkinter.
    """

    def __init__(self):
        """Создаёт окно, текстовое поле и первое приглашение."""
        self.root = tk.Tk()
        self.prompt_start_position = "1.0"
        self._setup_window()
        self._create_text_area()
        self._bind_events()
        self._show_prompt()

    def _setup_window(self):
        """Настраивает заголовок, размер и цвет окна."""
        username = getpass.getuser()
        hostname = socket.gethostname()

        title = f"Эмулятор - [{username}@{hostname}]"
        self.root.title(title)
        self.root.geometry("800x600")
        self.root.configure(bg="#1E1E1E")
        self.root.minsize(600, 400)

    def _create_text_area(self):
        """Создаёт текстовое поле терминала с тёмной темой."""
        self.text_area = scrolledtext.ScrolledText(
            self.root,
            bg="#1E1E1E",
            fg="#D4D4D4",
            insertbackground="#FFFFFF",
            selectforeground="#FFFFFF",
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0,
            font=("Menlo", 13),
            padx=8,
            pady=8,
            wrap=tk.WORD
        )
        self.text_area.pack(
            fill=tk.BOTH,
            expand=True
        )
        self.text_area.focus()

    def _bind_events(self):
        """Подписывает текстовое поле на события клавиатуры."""
        self.text_area.bind('<Return>', self._on_enter_pressed)
        self.text_area.bind('<Key>', self._on_key_pressed)

    def _get_prompt(self):
        """Формирует приглашение вида 'user@host % '."""
        username = getpass.getuser()
        hostname = socket.gethostname()
        return f"{username}@{hostname} % "

    def _show_prompt(self):
        """Печатает приглашение и запоминает позицию ввода."""
        prompt = self._get_prompt()
        self.text_area.insert(tk.END, prompt)
        self.text_area.mark_set("prompt_end", tk.INSERT)
        self.prompt_start_position = self.text_area.index(
            "prompt_end"
        )
        self.text_area.see(tk.END)

    def _write_output(self, text):
        """Выводит текст в терминал и прокручивает вниз.

        Args:
            text: Строка для вывода.
        """
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)

    def _get_current_command(self):
        """Читает введённую пользователем строку без приглашения.

        Returns:
            Введённая строка без пробелов по краям.
        """
        command = self.text_area.get(
            self.prompt_start_position,
            tk.END
        )
        return command.strip()

    def _clear_current_line(self):
        """Удаляет текущую строку ввода до позиции приглашения."""
        self.text_area.delete(self.prompt_start_position, tk.END)

    def _on_key_pressed(self, event):
        """Блокирует редактирование прошлого вывода.

        Запрещает Backspace и стрелку влево на границе
        приглашения, а Home переводит курсор в начало ввода.

        Args:
            event: Событие нажатия клавиши Tkinter.

        Returns:
            'break' для отмены действия, иначе None.
        """
        current_position = self.text_area.index(tk.INSERT)

        if event.keysym in ('BackSpace', 'Left'):
            if self.text_area.compare(
                current_position,
                "<=",
                self.prompt_start_position
            ):
                return "break"

        if event.keysym == 'Home':
            self.text_area.mark_set(
                tk.INSERT,
                self.prompt_start_position
            )
            return "break"

        return None

    def _on_enter_pressed(self, event):
        """Обрабатывает Enter: парсит и выполняет команду.

        Читает ввод, разбирает его через parse_command,
        выполняет через execute_command, печатает результат
        и выводит новое приглашение.

        Args:
            event: Событие нажатия Enter.

        Returns:
            'break', чтобы предотвратить вставку '\\n'.
        """
        command_line = self._get_current_command()

        self._write_output("\n")

        if command_line:
            try:
                command_name, arguments = parse_command(
                    command_line
                )

                if command_name:
                    result, should_exit = execute_command(
                        command_name,
                        arguments
                    )
                    self._write_output(f"{result}\n")

                    if should_exit:
                        self.root.quit()
                        return "break"

            except ValueError as error:
                self._write_output(f"Ошибка: {error}\n")

        self._show_prompt()

        return "break"

    def run(self):
        """Запускает главный цикл Tkinter."""
        self.root.mainloop()
