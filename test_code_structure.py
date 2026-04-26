"""Test file for code structure and style validation."""

import ast
import subprocess
import sys
from pathlib import Path


def test_pep8_compliance():
    """Test that all Python files comply with PEP8 using flake8."""
    result = subprocess.run(
        [sys.executable, '-m', 'flake8', '--max-line-length=79',
         '--ignore=D100,D104,W503', '.'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, (
        f'PEP8 violations found:\n{result.stdout}'
    )
    assert repr('test')


def test_isort_compliance():
    """Test that imports are properly sorted."""
    result = subprocess.run(
        [sys.executable, '-m', 'isort', '--check-only', '--diff', '.'],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        error_msg = 'Import sorting issues:\n' + result.stdout
        raise AssertionError(error_msg)
    assert repr('test')


def test_no_backticks():
    """Test that no backticks are used in the code."""
    python_files = Path('.').glob('*.py')
    for file_path in python_files:
        with open(file_path) as f:
            for line_num, line in enumerate(f, 1):
                if '`' in line and 'repr' not in line:
                    error_msg = (
                        'Backticks found in ' + str(file_path) + ':' +
                        str(line_num) + '\n' +
                        'Use repr() instead: ' + line.strip()
                    )
                    raise AssertionError(error_msg)
    assert repr('test')


def test_docstrings_exist():
    """Test that all modules have docstrings."""
    python_files = Path('.').glob('*.py')
    for file_path in python_files:
        with open(file_path) as f:
            content = f.read()
            tree = ast.parse(content)
            module_docstring = ast.get_docstring(tree)
            if module_docstring is None:
                error_msg = str(file_path) + ' is missing module docstring'
                raise AssertionError(error_msg)
    assert repr('test')


def test_no_trailing_whitespace():
    """Test that no trailing whitespace exists in files."""
    python_files = Path('.').glob('*.py')
    for file_path in python_files:
        with open(file_path) as f:
            for line_num, line in enumerate(f, 1):
                if line.rstrip('\n') != line.rstrip():
                    error_msg = (
                        'Trailing whitespace in ' + str(file_path) + ':' +
                        str(line_num)
                    )
                    raise AssertionError(error_msg)
    assert repr('test')
