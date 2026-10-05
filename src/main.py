"""Точка входа эмулятора оболочки."""

from gui import ShellEmulatorGUI


def main():
    """Создаёт и запускает графический эмулятор оболочки."""
    app = ShellEmulatorGUI()
    app.run()


if __name__ == "__main__":
    main()
