"""Главный модуль запуска эмулятора."""

import sys
from src.config import create_parser, resolve_configuration
from src.gui import ShellEmulatorGUI


def main() -> None:
    """Точка входа в приложение."""
    parser = create_parser()
    args = parser.parse_args()

    try:
        vfs_path, script_path, config_path = resolve_configuration(args)
    except (FileNotFoundError, ValueError) as error:
        print(f"Ошибка конфигурации: {error}", file=sys.stderr)
        sys.exit(1)

    app = ShellEmulatorGUI(
        vfs_path=vfs_path,
        script_path=script_path,
        config_path=config_path,
    )
    app.run()


if __name__ == "__main__":
    main()