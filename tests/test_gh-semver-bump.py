import subprocess
import unittest
import pytest
import os
import re
from .testbed import Testbed

class TestGhSemverBump(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        # Class-level setup code
        print("Setting up TestGhSemverBump testbed")
        cls.cli_path = os.path.abspath('gh-semver.py')
        cls.test_dir = os.path.abspath('./testbed/TestGhSemverBump')
        Testbed.cleanup_testbed(cls.test_dir)
        Testbed.create_testbed(cls.test_dir)

        # Create a tag that qualifies as a semantic version, make it different from any default or config values
        subprocess.check_call('echo "testfile">testfile.txt', cwd=cls.test_dir, shell=True)
        subprocess.check_call('git add testfile.txt', cwd=cls.test_dir, shell=True)
        subprocess.check_call('git commit -m "added testfile"', cwd=cls.test_dir, shell=True)
        subprocess.check_call('git tag -a -m zerozeroone v0.0.1', cwd=cls.test_dir, shell=True)
        subprocess.check_call('git tag -a -m onetwoone ver1.2.1', cwd=cls.test_dir, shell=True)
        subprocess.check_call('git tag -a -m oneoneone version1.1.1', cwd=cls.test_dir, shell=True)
        subprocess.check_call('git tag -a -m twooneone version2.1.1-freetext', cwd=cls.test_dir, shell=True)
        subprocess.check_call('git tag -a -m nonvalid version3.11-freetext', cwd=cls.test_dir, shell=True)

    @classmethod
    def teardown_class(cls):
        # Class-level teardown code
        print("Tearing down TestGhSemverBump class")
        #cls.__cleanup_testbed()

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
    def test_bump_patch_cmd(self):
        """This test checks the bump subcommand used without any of the required switches"""
        result = Testbed.run_cli(self.cli_path, 'bump', '--patch', '--no-run', cwd=self.test_dir)
        assert re.search(r"git tag -a -m \"Bumped patch from version  '.*'\" .*", result.stdout)

        
