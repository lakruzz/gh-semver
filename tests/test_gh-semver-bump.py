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
    def test_bump_major(self):
        Testbed.create_testbed(self.test_dir)
        result = Testbed.run_cli(self.cli_path, 'bump', '--major',  '--no-run', cwd=self.test_dir)
        # Expected output:
        # 'git tag -a -m "Bumped major from version \'0.0.0\' to \'1.0.0\'" 1.0.0\n'
        self.assertRegex(result.stdout.strip(), r"^git tag -a -m")
        self.assertRegex(result.stdout.strip(), r"1.0.0$")
        
        Testbed.git_dataset_1(self.test_dir)
        result = Testbed.run_cli(self.cli_path, 'bump', '--major',  '--no-run', cwd=self.test_dir)  
        # Expected output:
        # 'git tag -a -m "Bumped major from version \'version2.1.1-freetext\' to \'3.0.0\'" 3.0.0'      
        self.assertRegex(result.stdout.strip(), r"^git tag -a -m")
        self.assertRegex(result.stdout.strip(), r"3.0.0$")

        result = Testbed.run_cli(self.cli_path, 'bump', '--major',  '--message', 'Additional message','--no-run', cwd=self.test_dir)  
        # 'git tag -a -m "Bumped major from version \'version2.1.1-freetext\' to \'3.0.0\'\nAdditional message" 3.0.0'
        self.assertRegex(result.stdout.strip(), r'-m ".+\nAdditional message"')

        result = Testbed.run_cli(self.cli_path, 'bump', '--major',  '--suffix', 'pending','--no-run', cwd=self.test_dir)  
        # 'git tag -a -m "Bumped major from version \'version2.1.1-freetext\' to \'3.0.0\'\nAdditional message" 3.0.0'
        self.assertRegex(result.stdout.strip(), r"3.0.0-pending$")

        result = Testbed.run_cli(self.cli_path, 'bump', '--major',  cwd=self.test_dir)  
        # Expected output:
        # 'git tag -a -m "Bumped major from version \'version2.1.1-freetext\' to \'3.0.0\'" 3.0.0'
        self.assertRegex(result.stdout.strip(), r"^3.0.0$")

    @pytest.mark.dev
    def test_bump_minor(self):
        Testbed.create_testbed(self.test_dir)
        result = Testbed.run_cli(self.cli_path, 'bump', '--minor',  '--no-run', cwd=self.test_dir)
        self.assertRegex(result.stdout.strip(), r"^git tag -a -m")
        self.assertRegex(result.stdout.strip(), r"0.1.0$")
        
        Testbed.git_dataset_1(self.test_dir)
        result = Testbed.run_cli(self.cli_path, 'bump', '--minor',  '--no-run', cwd=self.test_dir)      
        self.assertRegex(result.stdout.strip(), r"^git tag -a -m")
        self.assertRegex(result.stdout.strip(), r"2.2.0$")

        result = Testbed.run_cli(self.cli_path, 'bump', '--minor',  cwd=self.test_dir)  
        self.assertRegex(result.stdout.strip(), r"^2.2.0$")

    @pytest.mark.dev
    def test_bump_patch(self):
        Testbed.create_testbed(self.test_dir)
        result = Testbed.run_cli(self.cli_path, 'bump', '--patch',  '--no-run', cwd=self.test_dir)
        self.assertRegex(result.stdout.strip(), r"^git tag -a -m")
        self.assertRegex(result.stdout.strip(), r"0.0.1$")
        
        Testbed.git_dataset_1(self.test_dir)
        result = Testbed.run_cli(self.cli_path, 'bump', '--patch',  '--no-run', cwd=self.test_dir)      
        self.assertRegex(result.stdout.strip(), r"^git tag -a -m")
        self.assertRegex(result.stdout.strip(), r"2.1.2$")

        result = Testbed.run_cli(self.cli_path, 'bump', '--patch',  cwd=self.test_dir)  
        self.assertRegex(result.stdout.strip(), r"^2.1.2$")

        
