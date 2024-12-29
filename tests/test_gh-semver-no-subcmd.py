import subprocess
import unittest
import pytest
import os
from .testbed import Testbed

class TestGhSemverNoSubcommand(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        # Class-level setup code
        print("Setting up TestGhSemverNoSubcommand testbed")
        cls.cli_path = os.path.abspath('gh-semver.py')
        cls.test_dir = os.path.abspath('./testbed/TestGhSemverNoSubcommand')
        Testbed.cleanup_testbed(cls.test_dir)
        Testbed.create_testbed(cls.test_dir)


    @classmethod
    def teardown_class(cls):
        # Class-level teardown code
        print("Tearing down TestGhSemverCLI class")
        #cls.__cleanup_testbed()


    def run_cli(self, *args, cwd=None):
        if cwd is None:
            cwd = self.test_dir
        result = subprocess.run(
            ['python3', self.cli_path] + list(args), cwd=cwd, capture_output=True, text=True)
        return result

    @pytest.mark.dev
    @pytest.mark.smoke
    def test_no_subcommand_initial(self):
        """This test checks if the script returns the default initial version when no config files are setup - it requires a clean testbed"""
        Testbed.cleanup_testbed(self.test_dir)
        Testbed.create_testbed(self.test_dir)
        result = Testbed.run_cli(self.cli_path, cwd=self.test_dir)
        self.assertIn(
            "v0.0.0", result.stdout)
        
    @pytest.mark.dev
    @pytest.mark.smoke
    def test_no_subcommand_from_config(self):
        """This test checks if the config files are read correctly, if they exist - it requires a clean testbed"""
        Testbed.cleanup_testbed(self.test_dir)
        Testbed.create_testbed(self.test_dir)
        # Create a .semver.config file with a variant differnt from the default prefix and initial offset       
        subprocess.check_call('echo "[semver]\\n  prefix = ver\\n  initial = 1.0.0">.semver.config', cwd=self.test_dir, shell=True)
        result = Testbed.run_cli(self.cli_path, cwd=self.test_dir)    
        self.assertIn(
            "ver1.0.0", result.stdout)
        
        # Even if cwd is not the root of the git repo, the script should still read the .semver.config file
        subprocess.check_call('mkdir not-root', cwd=self.test_dir, shell=True)
        subprocess.check_call('cd not-root', cwd=self.test_dir, shell=True)
        result = Testbed.run_cli(self.cli_path, cwd=self.test_dir+"/not-root")
        self.assertIn(
            "ver1.0.0", result.stdout)
       
        # Set the initial and prefix values in the git config, they should override the values in the .semver.config file
        subprocess.check_call('git config set --local semver.initial 2.0.0', cwd=self.test_dir, shell=True)
        subprocess.check_call('git config set --local semver.prefix version', cwd=self.test_dir, shell=True)
        result = Testbed.run_cli(self.cli_path, cwd=self.test_dir)     
        self.assertIn(
            "version2.0.0", result.stdout)
        
    @pytest.mark.dev
    @pytest.mark.smoke
    def test_no_subcommand_from_list(self):
        """This test checks if the script returns the latest version from a list of tags - it requires a list of tags in the repo"""
        subprocess.check_call('echo "testfile">testfile.txt', cwd=self.test_dir, shell=True)
        subprocess.check_call('git add -A', cwd=self.test_dir, shell=True)
        subprocess.check_call('git commit -m "added testfile"', cwd=self.test_dir, shell=True)
        subprocess.check_call('git tag -a -m zerozeroone v0.0.1', cwd=self.test_dir, shell=True)
        result = Testbed.run_cli(self.cli_path, cwd=self.test_dir) 
        self.assertIn("v0.0.1", result.stdout)

        subprocess.check_call('git tag -a -m onetwoone ver1.2.1', cwd=self.test_dir, shell=True)
        result = Testbed.run_cli(self.cli_path, cwd=self.test_dir) 
        self.assertIn("ver1.2.1", result.stdout)

        subprocess.check_call('git tag -a -m oneoneone version1.1.1', cwd=self.test_dir, shell=True)
        result = Testbed.run_cli(self.cli_path, cwd=self.test_dir) 
        self.assertIn("ver1.2.1", result.stdout)

        subprocess.check_call('git tag -a -m twooneone version2.1.1-freetext', cwd=self.test_dir, shell=True)
        result = Testbed.run_cli(self.cli_path, cwd=self.test_dir) 
        self.assertIn("version2.1.1-freetext", result.stdout)

        subprocess.check_call('git tag -a -m nonvalid version3.11-freetext', cwd=self.test_dir, shell=True)
        result = Testbed.run_cli(self.cli_path, cwd=self.test_dir) 
        self.assertIn("version2.1.1-freetext", result.stdout)