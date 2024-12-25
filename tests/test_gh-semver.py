import subprocess
import unittest
import pytest


class TestGhSemverCLI(unittest.TestCase):

    @pytest.mark.dev
    @pytest.mark.smoke
    def run_cli(self, *args):
        result = subprocess.run(
            ['python3', 'gh-semver.py'] + list(args), capture_output=True, text=True)
        return result

    @pytest.mark.dev
    @pytest.mark.smoke
    def test_no_subcommand(self):
        result = self.run_cli()
        self.assertIn(
            "No subcommand provided. Running default behavior.", result.stdout)

    @pytest.mark.dev
    @pytest.mark.smoke
    def test_bump_major(self):
        result = self.run_cli('bump', '--major')
        self.assertIn("Running in bump subcommand mode.", result.stdout)
        self.assertIn("Bumping major version.", result.stdout)

    @pytest.mark.dev
    @pytest.mark.smoke
    def test_bump_minor(self):
        result = self.run_cli('bump', '--minor')
        self.assertIn("Running in bump subcommand mode.", result.stdout)
        self.assertIn("Bumping minor version.", result.stdout)

    @pytest.mark.dev
    @pytest.mark.smoke
    def test_bump_patch(self):
        result = self.run_cli('bump', '--patch')
        self.assertIn("Running in bump subcommand mode.", result.stdout)
        self.assertIn("Bumping patch version.", result.stdout)

    @pytest.mark.dev
    @pytest.mark.smoke
    def test_init_with_prefix(self):
        result = self.run_cli('init', '--prefix', 'v1')
        self.assertIn("Running in init subcommand mode.", result.stdout)
        self.assertIn("Using prefix: v1", result.stdout)

    @pytest.mark.dev
    @pytest.mark.smoke
    def test_init_with_offset(self):
        result = self.run_cli('init', '--offset', '1.0.0')
        self.assertIn("Running in init subcommand mode.", result.stdout)
        self.assertIn("Using offset: 1.0.0", result.stdout)

    @pytest.mark.dev
    @pytest.mark.smoke
    def test_init_with_prefix_and_offset(self):
        result = self.run_cli('init', '--prefix', 'v1', '--offset', '10')
        self.assertIn("Running in init subcommand mode.", result.stdout)
        self.assertIn("Using prefix: v1", result.stdout)
        self.assertIn("Using offset: 10", result.stdout)
