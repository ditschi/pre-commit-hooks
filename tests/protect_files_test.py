from __future__ import annotations

import pytest
import subprocess

from pre_commit_hook_collection.protect_files import protected_files_changed
from pre_commit_hook_collection.protect_files import unstage_files
from pre_commit_hook_collection.protect_files import main

class TestProtectedFiles:
    def test_protected_files_changed_no_input(self):
        changed_files: list[str] = []
        protected_patterns: list[str]= []
        expected_result = False
        assert bool(
            protected_files_changed(
                changed_files,
                protected_patterns,
            ),
        ) is expected_result

    def test_protected_files_changed_no_pattern(self):
        changed_files = [
            'my/file/path/file.txt',
            'my/file/path/file.py', 'another/file.txt', 'README.md',
        ]
        protected_patterns: list[str] = []
        expected_result = False
        assert bool(
            protected_files_changed(
                changed_files,
                protected_patterns,
            ),
        ) is expected_result

    def test_protected_files_changed_match_pattern_all(self):
        changed_files = [
            'my/file/path/file.txt',
            'my/file/path/file.py', 'another/file.txt', 'README.md',
        ]
        protected_patterns = ['*']
        expected_result = True
        assert bool(
            protected_files_changed(
                changed_files,
                protected_patterns,
            ),
        ) is expected_result
        assert len(protected_files_changed(changed_files, protected_patterns)) == 4

    def test_protected_files_changed_match_pattern(self):
        changed_files = [
            'my/file/path/file.txt',
            'my/file/path/file.py', 'another/file.txt', 'README.md',
        ]
        protected_patterns = ['*.txt', 'README.md']
        expected_result = True
        assert bool(
            protected_files_changed(
                changed_files,
                protected_patterns,
            ),
        ) is expected_result
        assert len(protected_files_changed(changed_files, protected_patterns)) == 3

    def test_protected_files_changed_match_pattern_path(self):
        changed_files = [
            'my/file/path/file.txt',
            'my/file/path/file.py', 'another/file.txt', 'README.md',
        ]
        protected_patterns = ['my/file/*']
        expected_result = True
        assert bool(
            protected_files_changed(
                changed_files,
                protected_patterns,
            ),
        ) is expected_result
        assert len(protected_files_changed(changed_files, protected_patterns)) == 2

    def test_protected_files_changed_no_match_pattern(self):
        changed_files = [
            'my/file/path/file.txt',
            'my/file/path/file.py', 'another/file.txt', 'README.md',
        ]
        protected_patterns = ['not/changed/*']
        expected_result = False
        assert bool(
            protected_files_changed(
                changed_files,
                protected_patterns,
            ),
        ) is expected_result


class TestUnstage:
    def test_unstage_call(self, mocker):
        filepaths = ["file_a", "this/dir/"]
        expected_command = ["git", "reset", "--", "file_a", "this/dir/"]

        subprocess_run_mock = mocker.patch("subprocess.run")
        unstage_files(filepaths)

        subprocess_run_mock.assert_called_once_with(expected_command, check=False)


class TestMain:
    def test_main_success_when_no_protected_changed(self):
        result = main(["--filenames", "changed/file.md",
                  "--protected-files-glob", "*.txt"])
        assert result == 0

    def test_main_failure_when_protected_changed(self):
        result = main(["--filenames", "changed/file.txt",
                  "--protected-files-glob", "*.txt"])
        assert result == 1

    def test_main_failure_when_no_unstage(self):
        result = main(["--filenames", "changed/file.txt",
                  "--protected-files-glob", "*.txt",
                  "--no-unstage"])
        assert result == 1

    def test_main_nothing_staged(self):
        result = main(["--filenames",
                       "--protected-files-glob", "*"])
        assert result == 0

    def test_main_no_unstage_when_no_protected(self, mocker):
        call_mock = mocker.patch("pre_commit_hook_collection.protect_files.unstage_files")

        main(["--filenames", "changed/file.txt"])
        call_mock.assert_not_called()

    def test_main_unstage_when_protected(self, mocker):
        call_mock = mocker.patch("pre_commit_hook_collection.protect_files.unstage_files")

        main(["--filenames", "changed/file.txt",
              "--protected-files-glob", "*.txt"])
        call_mock.assert_called()

    def test_main_no_unstage_when_disabled(self, mocker):
        call_mock = mocker.patch("pre_commit_hook_collection.protect_files.unstage_files")

        main(["--filenames", "changed/file.txt",
              "--protected-files-glob", "*.txt",
              "--no-unstage"])
        call_mock.assert_not_called()
