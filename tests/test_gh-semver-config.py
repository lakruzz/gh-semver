import subprocess
import unittest
import pytest
import os
import re
from .testbed import Testbed

class TestGhSemverConfig(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        # Class-level setup code
        print("Setting up TestGhSemverConfig testbed")
        cls.cli_path = os.path.abspath('gh-semver.py')
        cls.test_dir = os.path.abspath('./testbed/TestGhSemverConfig')
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
    def test_init_no_switch_no_config(self):
        """This test checks the config subcommand used without any of the switches (read config)
        and without any config files"""
        Testbed.cleanup_testbed(self.test_dir)
        Testbed.create_testbed(self.test_dir)
        result = Testbed.run_cli(self.cli_path, 'init', cwd=self.test_dir)
        self.assertIn(
            "usage: gh-semver.py bump", result.stdout)

    @pytest.mark.dev
    def test_config_prefix_switch(self):
        """This test checks the bump subcommand used without any of the required switches"""
        result = Testbed.run_cli(self.cli_path, 'config', '--prefix',  '1.0.0', cwd=self.test_dir)
        self.assertIn(
            "semver.prefix = 1.0.0", result.stdout)