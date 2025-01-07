import unittest
import pytest
import os
import sys
from unittest.mock import patch, Mock
from io import StringIO

# Import the main function from gh-semver.py
# This is the function that will be tested
# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the main function from gh-semver.py
from gh_semver import *
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
    def test_bump(self):
        args = ['bump', '--major', '--no-run']
        valid = parse(args)
        self.assertEqual(valid.command, 'bump')
        self.assertTrue(valid.major)
        self.assertFalse(valid.run)
        
    @pytest.mark.dev
    def test_bump_invalid_argument(self):
        args = ['bump', '--major', '--no-run', "--invalid"]
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            with self.assertRaises(SystemExit) as cm:
                parse(args)
            self.assertEqual(cm.exception.code, 2)
            self.assertIn("unrecognized arguments: --invalid", mock_stderr.getvalue())

    @pytest.mark.dev
    def test_bump_full_monty(self):
        args = ['bump', '--minor', '--message', 'Additional message', '--suffix', 'pending']
        valid = parse(args)
        self.assertEqual(valid.command, 'bump')
        self.assertTrue(valid.minor)
        self.assertTrue(valid.run)    

    @pytest.mark.dev
    def test_bump_invalid_suffix(self):
        args = ['bump', '--minor', '--suffix', 'Pending']
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            with self.assertRaises(SystemExit) as cm:
                parse(args)
            self.assertEqual(cm.exception.code, 2)
            self.assertIn("Suffix: Allowed characters are lowercase letters, numbers, dashes and underscores", mock_stderr.getvalue())

    @pytest.mark.dev
    def test_config(self):
        args = ['config', '--prefix', 'ver', '--suffix', 'dev', '--initial', '1.0.0']
        valid = parse(args)
        self.assertEqual(valid.command, 'config')
        self.assertEqual(valid.prefix, 'ver')
        self.assertEqual(valid.suffix, 'dev')
        self.assertEqual(valid.initial, '1.0.0')


    @pytest.mark.dev
    def test_config_invalid_initial(self):
        args = ['config', '--prefix', 'ver', '--suffix', 'dev', '--initial', '1.NO.0']
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            with self.assertRaises(SystemExit) as cm:
                parse(args)
            self.assertEqual(cm.exception.code, 2)
            stderr = mock_stderr.getvalue()
            self.assertIn("Initial offset: Must be a three-level integer separated by dots (e.g. 1.0.0)", stderr)

    @pytest.mark.dev
    def test_config_invalid_prefix(self):
        args = ['config', '--prefix', 'Numb3r', '--suffix', 'dev', '--initial', '1.0.0']
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            with self.assertRaises(SystemExit) as cm:
                parse(args)
            self.assertEqual(cm.exception.code, 2)
            stderr = mock_stderr.getvalue()
            self.assertIn("Prefix: Allowed characters are lowercase and uppercase letters", stderr)
