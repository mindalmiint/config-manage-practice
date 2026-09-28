import tkinter as tk
from tkinter import scrolledtext
import getpass
import socket
from parser import parse_command
from commands import execute_command


class ShellEmulatorGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.prompt_start_position = "1.0"
        self._setup_window()
        self._create_text_area()
        self._bind_events()
        self._show_prompt()

    def _setup_window(self):
        username = getpass.getuser()
        hostname = socket.gethostname()

        title = f"Эмулятор - [{username}@{hostname}]"
        self.root.title(title)
        self.root.geometry("800x600")
        self.root.configure(bg="#1E1E1E")
        self.root.minsize(600, 400)

    def _create_text_area(self):
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
        self.text_area.bind('<Return>', self._on_enter_pressed)
        self.text_area.bind('<Key>', self._on_key_pressed)

    def _get_prompt(self):
        username = getpass.getuser()
        hostname = socket.gethostname()
        return f"{username}@{hostname} % "

    def _show_prompt(self):
        prompt = self._get_prompt()
        self.text_area.insert(tk.END, prompt)
        self.text_area.mark_set("prompt_end", tk.INSERT)
        self.prompt_start_position = self.text_area.index(
            "prompt_end"
        )
        self.text_area.see(tk.END)

    def _write_output(self, text):
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)

    def _get_current_command(self):
        command = self.text_area.get(
            self.prompt_start_position,
            tk.END
        )
        return command.strip()

    def _clear_current_line(self):
        self.text_area.delete(self.prompt_start_position, tk.END)

    def _on_key_pressed(self, event):
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
        self.root.mainloop()