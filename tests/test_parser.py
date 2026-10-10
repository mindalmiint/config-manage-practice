import sys
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parent.parent)
)

import pytest
from src.parser import parse_command


def test_simple_command():
    assert parse_command('ls') == ('ls', [])


def test_command_with_arguments():
    result = parse_command('ls -la /home')
    assert result == ('ls', ['-la', '/home'])


def test_quoted_argument():
    result = parse_command('cd "My Documents"')
    assert result == ('cd', ['My Documents'])


def test_single_quoted_argument():
    result = parse_command("cd 'My Documents'")
    assert result == ('cd', ['My Documents'])


def test_empty_input():
    assert parse_command('') == (None, [])
    assert parse_command('   ') == (None, [])


def test_extra_spaces():
    result = parse_command('ls   -la    /home')
    assert result == ('ls', ['-la', '/home'])


def test_invalid_syntax():
    with pytest.raises(ValueError):
        parse_command('cd "незакрытая')