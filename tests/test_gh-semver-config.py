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
    def test_config_no_switch_no_config(self):
        """Config subcommand used without any of the switches (read config)
        and without any config files"""
        Testbed.create_testbed(self.test_dir) # Get a clean testbed
        result = Testbed.run_cli(self.cli_path, 'config', cwd=self.test_dir)
        self.assertIn( # Read mode
            "Current configuration:", result.stdout)
        self.assertIn( # No configuration defined
            "No configuration defined", result.stdout)

    @pytest.mark.dev
    def test_config_no_switch_with_config(self):
        """Config subcommand used without any of the switches (read config)
        and without any config files"""
        # Creating the config file manually - not using the config subcommand - out of scope for this test
        subprocess.check_call('echo "[semver]\\n  prefix = ver\\n  initial = 1.0.0\\n  suffix = -pending">.semver.config', cwd=self.test_dir, shell=True)
        result = Testbed.run_cli(self.cli_path, 'config', cwd=self.test_dir)
        self.assertIn(  #print the new value
            "semver.prefix = ver", result.stdout)
        self.assertIn(  #print the new value
            "semver.initial = 1.0.0", result.stdout)
        self.assertIn(  #print the new value
            "semver.suffix = -pending", result.stdout)
            
    @pytest.mark.dev
    def test_config_prefix_switch(self):
        """Config subcommand used to write the prefix to the config files"""
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
    
    @pytest.mark.dev
    def test_config_suffix_switch(self):
        """Config subcommand used to write the suffix to the config files"""
        # Will not require a clean testbed, this is a write operation
        result = Testbed.run_cli(self.cli_path, 'config', '--suffix',  'pending', cwd=self.test_dir)
        self.assertIn( #print the new value
            "semver.suffix = pending", result.stdout)
        result = Testbed.run_cli(self.cli_path, 'config', '--suffix',  'numb3r', cwd=self.test_dir)
        self.assertIn(  #print the new value
            "semver.suffix = numb3r", result.stdout)
        result = Testbed.run_cli(self.cli_path, 'config', '--suffix',  'dot.no', cwd=self.test_dir)
        assert(result.returncode > 0)
        self.assertIn(  #try to set it to a non-valid value
            "error: argument --suffix:", result.stderr)    
        
    @pytest.mark.dev
    def test_config_offset_switch(self):
        """Config subcommand used to write the offset to the config files"""
        # Will not require a clean testbed, this is a write operation
        result = Testbed.run_cli(self.cli_path, 'config', '--offset',  '0.0.0', cwd=self.test_dir)
        self.assertIn( #print the new value
            "semver.offset = 0.0.0", result.stdout)
        result = Testbed.run_cli(self.cli_path, 'config', '--offset',  '12.4.345', cwd=self.test_dir)
        self.assertIn(  #print the new value
            "semver.offset = 12.4.345", result.stdout)
        result = Testbed.run_cli(self.cli_path, 'config', '--offset',  'v0.0.0', cwd=self.test_dir)
        assert(result.returncode > 0)
        self.assertIn(  #try to set it to a non-valid value
            "error: argument --offset:", result.stderr)        