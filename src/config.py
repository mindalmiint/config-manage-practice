"""Модуль для обработки конфигурации и аргументов командной строки."""

import argparse
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
import yaml


def create_parser() -> argparse.ArgumentParser:
    """Создает парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Эмулятор командной строки UNIX."
    )
    parser.add_argument(
        "--vfs-path",
        type=str,
        default=None,
        help="Путь к физическому расположению VFS",
    )
    parser.add_argument(
        "--script-path",
        type=str,
        default=None,
        help="Путь к стартовому скрипту",
    )
    parser.add_argument(
        "--config-path",
        type=str,
        default=None,
        help="Путь к конфигурационному файлу YAML",
    )
    return parser


def load_yaml_config(config_path: str) -> Dict[str, Any]:
    """Загружает настройки из YAML-файла."""
    path = Path(config_path)
    if not path.is_file():
        raise FileNotFoundError(
            f"Конфигурационный файл не найден: {config_path}"
        )

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            return data if isinstance(data, dict) else {}
    except Exception as error:
        raise ValueError(
            f"Ошибка чтения конфигурационного файла: {error}"
        ) from error


def resolve_configuration(
    cli_args: argparse.Namespace,
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Объединяет параметры CLI и YAML с учетом приоритета YAML."""
    config_path = cli_args.config_path
    yaml_data: Dict[str, Any] = {}

    if config_path:
        yaml_data = load_yaml_config(config_path)

    vfs_path = yaml_data.get("vfs_path") or cli_args.vfs_path
    script_path = yaml_data.get("script_path") or cli_args.script_path

    return vfs_path, script_path, config_path