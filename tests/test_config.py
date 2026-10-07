"""Тестирование модуля конфигурации."""

from pathlib import Path
import pytest
from src.config import create_parser, load_yaml_config, resolve_configuration


def test_cli_parser_defaults():
    """Проверка значений по умолчанию для парсера CLI."""
    parser = create_parser()
    args = parser.parse_args([])
    assert args.vfs_path is None
    assert args.script_path is None
    assert args.config_path is None


def test_cli_parser_custom():
    """Проверка парсинга пользовательских аргументов CLI."""
    parser = create_parser()
    args = parser.parse_args(
        ["--vfs-path", "vfs.zip", "--script-path", "script.txt"]
    )
    assert args.vfs_path == "vfs.zip"
    assert args.script_path == "script.txt"


def test_load_yaml_config_valid(tmp_path: Path):
    """Проверка успешной загрузки YAML."""
    config_file = tmp_path / "config.yaml"
    config_file.write_text("vfs_path: /tmp/vfs.zip\nscript_path: /tmp/s.txt")

    data = load_yaml_config(str(config_file))
    assert data["vfs_path"] == "/tmp/vfs.zip"
    assert data["script_path"] == "/tmp/s.txt"


def test_load_yaml_config_not_found():
    """Проверка ошибки при отсутствии файла YAML."""
    with pytest.raises(FileNotFoundError):
        load_yaml_config("non_existent_file.yaml")


def test_priority_yaml_over_cli(tmp_path: Path):
    """Проверка приоритета YAML над аргументами CLI."""
    config_file = tmp_path / "config.yaml"
    config_file.write_text("vfs_path: yaml_vfs\nscript_path: yaml_script")

    parser = create_parser()
    args = parser.parse_args(
        [
            "--vfs-path",
            "cli_vfs",
            "--script-path",
            "cli_script",
            "--config-path",
            str(config_file),
        ]
    )

    vfs, script, config = resolve_configuration(args)
    assert vfs == "yaml_vfs"
    assert script == "yaml_script"
    assert config == str(config_file)