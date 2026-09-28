import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.commands import execute_command, cmd_ls, cmd_cd, cmd_exit


def test_cmd_ls_no_args():
    assert cmd_ls([]) == "ls []"


def test_cmd_ls_with_args():
    assert cmd_ls(['-la']) == "ls ['-la']"


def test_cmd_cd_no_args():
    assert cmd_cd([]) == "cd []"


def test_cmd_cd_with_path():
    assert cmd_cd(['/home']) == "cd ['/home']"


def test_cmd_exit():
    assert cmd_exit([]) == "exit []"


def test_execute_ls():
    result, should_exit = execute_command('ls', ['-la'])
    assert result == "ls ['-la']"
    assert should_exit is False


def test_execute_exit():
    result, should_exit = execute_command('exit', [])
    assert result == "exit []"
    assert should_exit is True


def test_unknown_command():
    result, should_exit = execute_command('unknown', [])
    assert "not found" in result
    assert should_exit is False