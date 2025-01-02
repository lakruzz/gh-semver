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
        """Config subcommand used without any of the switches (read config)
        and without any config files"""
        Testbed.create_testbed(self.test_dir) # Get a clean testbed
        result = Testbed.run_cli(self.cli_path, 'config', cwd=self.test_dir)
        self.assertIn( # Read mode
            "Current configuration:", result.stdout)
        self.assertIn( # No configuration defined
            "No configuration defined", result.stdout)

    @pytest.mark.dev
    def test_config_prefix_switch(self):
        """Config subcommand used to write to the config files"""
        # Will not require a clean testbed, this is a write operation
        result = Testbed.run_cli(self.cli_path, 'config', '--prefix',  'v', cwd=self.test_dir)
        self.assertIn( #print the new value
            "semver.prefix = v", result.stdout)
        result = Testbed.run_cli(self.cli_path, 'config', '--prefix',  'ver', cwd=self.test_dir)
        self.assertIn(  #print the new value
            "semver.prefix = ver", result.stdout)
        result = Testbed.run_cli(self.cli_path, 'config', '--prefix',  'Numb3r', cwd=self.test_dir)
        assert(result.returncode > 0)
        self.assertIn(  #try to set it to a non-valid value
            "error: argument --prefix:", result.stderr)
        
    