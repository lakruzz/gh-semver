import subprocess
import unittest
import pytest
import os
import sys
from .testbed import Testbed

# Add the subdirectory containing the classes to the general class_path
class_path = os.path.dirname(os.path.abspath(__file__))+"/classes"
sys.path.append(class_path)

from classes.semver import Semver


class TestGhSemverBump(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        # Class-level setup code
        print("Setting up TestGhSemverBump testbed")
        cls.cli_path = os.path.abspath('gh-semver.py')
        cls.test_dir = os.path.abspath('./testbed/TestGhSemverBump')
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
        semver = Semver(workdir=self.test_dir) 
        cmd = semver.get_git_tag_cmd(level='major', message='Additional message', suffix='pending')
        self.assertRegex(cmd, r"^git tag -a -m")
        self.assertRegex(cmd, r"3.0.0-pending$")

        new_tag = semver.bump(level='major', message='Additional message', suffix='pending')
        self.assertRegex(cmd, r"3.0.0-pending$")


