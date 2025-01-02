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
    def test_no_subcommand(self):
        """Checks if the script accepts to run with no subcommands or parameters at all"""
        Testbed.create_testbed(self.test_dir) # Get a clean testbed
        result = Testbed.run_cli(self.cli_path, cwd=self.test_dir)
        self.assertIn(
            "0.0.0", result.stdout)

    @pytest.mark.dev
    def test_bump_major(self):
        result = self.run_cli('bump', '--major', '--verbose')
        self.assertIn("Running in bump subcommand mode.", result.stdout)
        self.assertIn("Bumping major version.", result.stdout)

    @pytest.mark.dev
    def test_bump_minor(self):
        result = self.run_cli('bump', '--minor', '--verbose')
        self.assertIn("Running in bump subcommand mode.", result.stdout)
        self.assertIn("Bumping minor version.", result.stdout)

    @pytest.mark.dev
    def test_bump_patch(self):
        result = self.run_cli('bump', '--patch', '--verbose')
        self.assertIn("Running in bump subcommand mode.", result.stdout)
        self.assertIn("Bumping patch version.", result.stdout)

    @pytest.mark.dev
    def test_init_with_prefix(self):
        result = self.run_cli('init', '--prefix', 'v1')
        self.assertIn("Running in init subcommand mode.", result.stdout)
        self.assertIn("Using prefix: v1", result.stdout)

    @pytest.mark.dev
    def test_init_with_offset(self):
        result = self.run_cli('init', '--offset', '1.0.0')
        self.assertIn("Running in init subcommand mode.", result.stdout)
        self.assertIn("Using offset: 1.0.0", result.stdout)

    @pytest.mark.dev
    def test_init_with_prefix_and_offset(self):
        result = self.run_cli('init', '--prefix', 'v1', '--offset', '10')
        self.assertIn("Running in init subcommand mode.", result.stdout)
        self.assertIn("Using prefix: v1", result.stdout)
        self.assertIn("Using offset: 10", result.stdout)
