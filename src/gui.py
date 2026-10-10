"""Модуль графического интерфейса эмулятора."""

import getpass
from pathlib import Path
import socket
import tkinter as tk
from tkinter import scrolledtext
from typing import Optional

from src.commands import execute_command
from src.parser import parse_command


class ShellEmulatorGUI:
    """Класс графического интерфейса эмулятора."""

    def __init__(
        self,
        vfs_path: Optional[str] = None,
        script_path: Optional[str] = None,
        config_path: Optional[str] = None,
    ) -> None:
        """Инициализация графического окна и параметров."""
        self.vfs_path = vfs_path
        self.script_path = script_path
        self.config_path = config_path

        self.root = tk.Tk()
        self.prompt_start_position = "1.0"
        self._setup_window()
        self._create_text_area()
        self._bind_events()

        self._print_debug_info()
        self._show_prompt()
        self._run_startup_script()

    def _setup_window(self) -> None:
        """Настройка параметров окна."""
        username = getpass.getuser()
        hostname = socket.gethostname()
        self.root.title(f"Эмулятор - [{username}@{hostname}]")
        self.root.geometry("800x600")
        self.root.configure(bg="#1E1E1E")
        self.root.minsize(600, 400)

    def _create_text_area(self) -> None:
        """Создание текстового поля."""
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
            wrap=tk.WORD,
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.focus()

    def _bind_events(self) -> None:
        """Привязка событий клавиатуры."""
        self.text_area.bind("<Return>", self._on_enter_pressed)
        self.text_area.bind("<Key>", self._on_key_pressed)

    def _get_prompt(self) -> str:
        """Формирование строки приглашения."""
        username = getpass.getuser()
        hostname = socket.gethostname()
        return f"{username}@{hostname} % "

    def _show_prompt(self) -> None:
        """Отображение приглашения к вводу."""
        prompt = self._get_prompt()
        self.text_area.insert(tk.END, prompt)
        self.text_area.mark_set("prompt_end", tk.INSERT)
        self.prompt_start_position = self.text_area.index("prompt_end")
        self.text_area.see(tk.END)

    def _write_output(self, text: str) -> None:
        """Запись текста в окно эмулятора."""
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)

    def _print_debug_info(self) -> None:
        """Вывод отладочной информации о параметрах."""
        debug_msg = (
            "=== Отладочный вывод параметров ===\n"
            f"VFS Path: {self.vfs_path}\n"
            f"Script Path: {self.script_path}\n"
            f"Config Path: {self.config_path}\n"
            "===================================\n\n"
        )
        self._write_output(debug_msg)

    def _run_startup_script(self) -> None:
        """Последовательное выполнение команд из стартового скрипта."""
        if not self.script_path:
            return

        path = Path(self.script_path)
        if not path.is_file():
            self._write_output(
                f"Ошибка: Стартовый скрипт не найден: {self.script_path}\n\n"
            )
            return

        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        for line in lines:
            command_line = line.strip()
            if not command_line:
                continue

            self._write_output(f"{command_line}\n")
            try:
                cmd_name, args = parse_command(command_line)
                if cmd_name:
                    res, should_exit = execute_command(cmd_name, args)
                    self._write_output(f"{res}\n")
                    if should_exit:
                        self.root.quit()
                        return
            except ValueError as error:
                self._write_output(f"Ошибка: {error}\n")

            self._show_prompt()

    def _get_current_command(self) -> str:
        """Получение текущей введенной команды."""
        return self.text_area.get(self.prompt_start_position, tk.END).strip()

    def _on_key_pressed(self, event: tk.Event) -> Optional[str]:
        """Обработка нажатий клавиш каретки."""
        cur_pos = self.text_area.index(tk.INSERT)
        if event.keysym in ("BackSpace", "Left"):
            if self.text_area.compare(
                cur_pos, "<=", self.prompt_start_position
            ):
                return "break"
        if event.keysym == "Home":
            self.text_area.mark_set(tk.INSERT, self.prompt_start_position)
            return "break"
        return None

    def _on_enter_pressed(self, event: tk.Event) -> str:
        """Обработка нажатия Enter."""
        command_line = self._get_current_command()
        self._write_output("\n")

        if command_line:
            try:
                cmd_name, args = parse_command(command_line)
                if cmd_name:
                    res, should_exit = execute_command(cmd_name, args)
                    self._write_output(f"{res}\n")
                    if should_exit:
                        self.root.quit()
                        return "break"
            except ValueError as error:
                self._write_output(f"Ошибка: {error}\n")

        self._show_prompt()
        return "break"

    def run(self) -> None:
        """Запуск главного цикла Tkinter."""
        self.root.mainloop()