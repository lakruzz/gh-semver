import subprocess
import unittest
import pytest
import os


class TestGhSemverCLI(unittest.TestCase):


    @classmethod
    def setup_class(cls):
        # Class-level setup code
        print("Setting up TestGhSemverCLI class")
        cls.cli_path = os.path.abspath('gh-semver.py')
        cls.test_dir = os.path.abspath('./testbed/TestGhSemverCLI')
        # Check if teardown ran succesfully and rerun it if it didn't
        if os.path.exists(cls.test_dir):
            if not cls.cleanup_testbed():
                raise Exception("Failed to remove existing test directory")
        subprocess.check_call('mkdir -p {}'.format(cls.test_dir), shell=True)
        subprocess.check_call('git init', cwd=cls.test_dir, shell=True)

    @classmethod
    def teardown_class(cls):
        # Class-level teardown code
        print("Tearing down TestGhSemverCLI class")
        cls.cleanup_testbed()

    
    @classmethod
    def cleanup_testbed(cls):
        print("Cleaning up the testbed")
        try:
            subprocess.check_call('rm -rf {}'.format(cls.test_dir), shell=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to remove test directory: {e}")
            return False        

    def run_cli(self, *args):
        result = subprocess.run(
            ['python3', self.cli_path] + list(args), cwd=self.test_dir, capture_output=True, text=True)
        return result

    @pytest.mark.dev
    def test_no_subcommand(self):
        result = self.run_cli('--verbose')
        self.assertIn(
            "Running default behavior. Returning current SemVer.", result.stdout)

    @pytest.mark.dev
    def test_bump_major(self):
        result = self.run_cli('bump', '--major')
        self.assertIn("Running in bump subcommand mode.", result.stdout)
        self.assertIn("Bumping major version.", result.stdout)

    @pytest.mark.dev
    def test_bump_minor(self):
        result = self.run_cli('bump', '--minor')
        self.assertIn("Running in bump subcommand mode.", result.stdout)
        self.assertIn("Bumping minor version.", result.stdout)

    @pytest.mark.dev
    def test_bump_patch(self):
        result = self.run_cli('bump', '--patch')
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
