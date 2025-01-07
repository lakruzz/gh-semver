import subprocess
import unittest
import pytest
import os
import sys
from unittest.mock import patch, Mock
from .testbed import Testbed

# Add the subdirectory containing the classes to the general class_path
class_path = os.path.dirname(os.path.abspath(__file__))+"/classes"
sys.path.append(class_path)

from classes.semver import Semver


class TestGhSemverUnitTest(unittest.TestCase):

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
        print("Tearing down TestGhSemverBump class")
        #cls.__cleanup_testbed()

    @pytest.mark.dev
    def test_get_tag_major(self): 
        Testbed.create_testbed(self.test_dir)
        Testbed.git_dataset_1(self.test_dir)

        semver = Semver(workdir=self.test_dir)

        cmd = semver.get_git_tag_cmd(level='major', message='Additional message', suffix='pending')
        self.assertRegex(cmd, r'^git tag -a -m')
        self.assertRegex(cmd, r'Additional message"')
        self.assertRegex(cmd, r"3.0.0-pending$")

        cmd = semver.get_git_tag_cmd(level='major')
        self.assertRegex(cmd, r"^git tag -a -m")
        self.assertRegex(cmd, r"3.0.0$")

    @pytest.mark.dev
    def test_bump_major(self):
        Testbed.create_testbed(self.test_dir)
        Testbed.git_dataset_1(self.test_dir)
        semver = Semver(workdir=self.test_dir) 
        new_tag = semver.bump(level='major', message='Additional message', suffix='pending')
        self.assertRegex(new_tag, r"3.0.0-pending$")

    @pytest.mark.dev
    def test_config(self):
        Testbed.create_testbed(self.test_dir)        
        semver = Semver(workdir=self.test_dir)
        self.assertRegex(semver.prefix, r"^$")
        self.assertRegex(semver.initial, r"^0.0.0$")
        self.assertRegex(semver.suffix, r"^$")

        semver.set_config(prefix='ver', initial='1.0.0', suffix='pending')
        self.assertRegex(semver.prefix, r"^ver$")
        self.assertRegex(semver.initial, r"^1.0.0$")
        self.assertRegex(semver.suffix, r"^pending$")

        cmd = semver.get_git_tag_cmd(level='minor')
        self.assertRegex(cmd, r"ver1.1.0-pending$")

    @pytest.mark.dev
    def test_bad_config(self):
        Testbed.create_testbed(self.test_dir) 
        subprocess.check_call('echo "[semver]\\n  prefix = ver\\n  initial = 1.hey.0\\n  suffix = -pending">.semver.config', cwd=self.test_dir, shell=True)       
        stderr = None
        try:
            semver = Semver(workdir=self.test_dir)
        except ValueError as e:
            stderr = str(e)
        self.assertRegex(stderr, r"Failed to parse initial version, doesn't look like a three-level integer") 

    @pytest.mark.dev
    def test_semver_null_constructor(self):
        semver = Semver()
        cwd = os.getcwd()
        self.assertEqual(semver.workdir, cwd)
        
    @pytest.mark.dev
    def test_semver_bad_workdir(self):
        stderr = None
        try:
            semver = Semver(workdir='bad_dir_xyz')
        except FileNotFoundError as e:
            stderr = str(e)    
        self.assertEqual(stderr, 'Directory bad_dir_xyz does not exist')

    @patch.object(Semver, '_Semver__run_git')
    def test_semver_outside_git(self, mock_run_git):
        # Simulate the git command returning an error
        mock_run_git.return_value = Mock(
            returncode=1, 
            stderr='fatal: not a git repository (or any of the parent directories): .git\n')

        with self.assertRaises(FileNotFoundError) as context:
            semver = Semver()

        self.assertIn('fatal: not a git repository (or any of the parent directories): .git\n', str(context.exception))


if __name__ == '__main__':
    unittest.main()