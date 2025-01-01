import subprocess
import unittest
import pytest
import os
from .testbed import Testbed

class TestGhSemverNoSubcommand(unittest.TestCase):

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
    def test_no_subcommand_initial(self):
        """Checks if the script returns the default initial version when no config files are setup"""
        Testbed.create_testbed(self.test_dir) # Get a clean testbed
        result = Testbed.run_cli(self.cli_path, cwd=self.test_dir)
        self.assertIn(
            "0.0.0", result.stdout)
        
    @pytest.mark.dev
    def test_no_subcommand_from_config(self):
        """Check if the config files are read correctly"""
        Testbed.create_testbed(self.test_dir)
        # Create a .semver.config file with a variant differnt from the default prefix and initial offset       
        subprocess.check_call('echo "[semver]\\n  prefix = ver\\n  initial = 1.0.0\\n  suffix = -pending">.semver.config', cwd=self.test_dir, shell=True)
        result = Testbed.run_cli(self.cli_path, cwd=self.test_dir)    
        self.assertIn(
            "ver1.0.0-pending", result.stdout)
        
        # Even if cwd is not the root of the git repo, the script should still read the .semver.config file
        subprocess.check_call('mkdir not-root', cwd=self.test_dir, shell=True)
        subprocess.check_call('cd not-root', cwd=self.test_dir, shell=True)
        result = Testbed.run_cli(self.cli_path, cwd=self.test_dir+"/not-root")
        self.assertIn(
            "ver1.0.0-pending", result.stdout)
        

       

    @pytest.mark.dev
    def test_no_subcommand_from_list(self):
        """Checks if the script returns the latest version from a list of tags"""

        # Create a tag that qualifies as a semantic version, make it different from any default or config values
        # Not using the bump subcommand as it would be out of scope for this test
        subprocess.check_call('echo "testfile">testfile.txt', cwd=self.test_dir, shell=True)
        subprocess.check_call('git add testfile.txt', cwd=self.test_dir, shell=True)
        subprocess.check_call('git commit -m "added testfile"', cwd=self.test_dir, shell=True)
        subprocess.check_call('git tag -a -m zerozeroone v0.0.1', cwd=self.test_dir, shell=True)

        # Check if it returns the correct version
        result = Testbed.run_cli(self.cli_path, cwd=self.test_dir) 
        self.assertIn("v0.0.1", result.stdout)

        # Create a tag, still different from any default or config values and with a higher version number
        subprocess.check_call('git tag -a -m onetwoone ver1.2.1', cwd=self.test_dir, shell=True)
        result = Testbed.run_cli(self.cli_path, cwd=self.test_dir) 
        self.assertIn("ver1.2.1", result.stdout)

        # Create a tag, still different from any default or config values and with a lower version number than the previous one
        # This should still pick the highest version number
        subprocess.check_call('git tag -a -m oneoneone version1.1.1', cwd=self.test_dir, shell=True)
        result = Testbed.run_cli(self.cli_path, cwd=self.test_dir) 
        self.assertIn("ver1.2.1", result.stdout)

        # Create a tag with a freetext suffix, with a higher version number than the previous one
        # The freetest should be allowed
        subprocess.check_call('git tag -a -m twooneone version2.1.1-freetext', cwd=self.test_dir, shell=True)
        result = Testbed.run_cli(self.cli_path, cwd=self.test_dir) 
        self.assertIn("version2.1.1-freetext", result.stdout)

        # Create a tag with a higher, but invalid version number - should be ignored
        subprocess.check_call('git tag -a -m nonvalid version3.11-freetext', cwd=self.test_dir, shell=True)
        result = Testbed.run_cli(self.cli_path, cwd=self.test_dir) 
        self.assertIn("version2.1.1-freetext", result.stdout)