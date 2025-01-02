import subprocess
import unittest
import pytest
import os
from .testbed import Testbed



class TestGhSemverCLI(unittest.TestCase):
    """Mostly focused on tesing the CLI, that is the subcommands, arguments and options"""

    @classmethod
    def setup_class(cls):
        print(f"Setting up testbed for {cls.__name__} class")
        cls.test_dir = os.path.abspath(f"./testbed/{cls.__name__}")
        cls.cli_path = os.path.abspath('gh-semver.py')
        Testbed.create_testbed(cls.test_dir)
        Testbed.git_dataset_1(cls.test_dir)

    @classmethod
    def teardown_class(cls):
        # Class-level teardown code
        print(f"Tearing down {cls.__name__} class testbed")
        print(f"...not doing anything - testbed will be left for inspection and reset as part of the next test run")

    @pytest.mark.dev
    def test_bump_no_switch(self):
        """This test checks the bump subcommand used without any of the required switches"""
        result = Testbed.run_cli(self.cli_path, 'bump', cwd=self.test_dir)
        self.assertIn(
            "usage: gh-semver.py bump", result.stderr)

    @pytest.mark.dev
    def test_bump_wrong_switch(self):
        """This test checks the bump subcommand used without any of the required switches"""
        result = Testbed.run_cli(self.cli_path, 'bump', '--illegal', cwd=self.test_dir)
        self.assertIn(
            "usage: gh-semver.py bump", result.stderr)

    @pytest.mark.dev
    def test_config_wrong_switch(self):
        """This test checks the bump subcommand used without any of the required switches"""
        result = Testbed.run_cli(self.cli_path, 'config', '--illegal', cwd=self.test_dir)
        self.assertIn(
            "unrecognized arguments: --illegal", result.stderr)
        
    def test_bump_invalid_suffix(self):
        """This test checks the bump subcommand used without any of the required switches"""
        result = Testbed.run_cli(self.cli_path, 'bump', '--major', '--suffix', 'Numb3er', '--no-run', cwd=self.test_dir)
        self.assertGreater(result.returncode, 0)
        self.assertIn("error: argument --suffix", result.stderr)

    def test_bump_valid_suffix(self):
        """This test checks the bump subcommand used without any of the required switches"""
        result = Testbed.run_cli(self.cli_path, 'bump', '--major', '--suffix', 'numb3er', '--no-run', cwd=self.test_dir)
        self.assertEqual(result.returncode, 0)
