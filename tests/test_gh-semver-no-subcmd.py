import subprocess
import unittest
import pytest
import os


class TestGhSemverNoSubcommand(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        # Class-level setup code
        print("Setting up TestGhSemverNoSubcommand testbed")
        cls.cli_path = os.path.abspath('gh-semver.py')
        cls.test_dir = os.path.abspath('./testbed/TestGhSemverNoSubcommand')
        # Check if teardown ran succesfully and rerun it if it didn't
        cls.__cleanup_testbed()
        cls.__create_testbed()


    @classmethod
    def teardown_class(cls):
        # Class-level teardown code
        print("Tearing down TestGhSemverCLI class")
        cls.__cleanup_testbed()

    @classmethod
    def __cleanup_testbed(cls):
        if os.path.exists(cls.test_dir):
            print("Cleaning up the testbed")
            try:
                subprocess.check_call('rm -rf {}'.format(cls.test_dir), shell=True)
            except subprocess.CalledProcessError as e:
                print(f"Failed to remove test directory: {e}")
                
        
    @classmethod
    def __create_testbed(cls):
        subprocess.check_call('mkdir -p {}'.format(cls.test_dir), shell=True)
        subprocess.check_call('git init', cwd=cls.test_dir, shell=True)


    def run_cli(self, *args):
        result = subprocess.run(
            ['python3', self.cli_path] + list(args), cwd=self.test_dir, capture_output=True, text=True)
        return result

    @pytest.mark.dev
    @pytest.mark.smoke
    def test_no_subcommand_initial(self):
        """This test checks if the script returns the default initial version when no config files are setup - it requires a clean testbed"""
        self.__cleanup_testbed()
        self.__create_testbed()
        result = self.run_cli()
        self.assertIn(
            "v0.0.0", result.stdout)
        
    @pytest.mark.dev
    @pytest.mark.smoke
    def test_no_subcommand_from_config(self):
        """This test checks if the config files are read correctly, if they exist - it requires a clean testbed"""
        self.__cleanup_testbed()
        self.__create_testbed() 
        # Create a .semver.config file with a variant differnt from the default prefix and initial offset       
        subprocess.check_call('echo "[semver]\\n  prefix = ver\\n  initial = 1.0.0">.semver.config', cwd=self.test_dir, shell=True)
        result = self.run_cli()    
        self.assertIn(
            "ver1.0.0", result.stdout)
        # Set the initial and prefix values in the git config, they should override the values in the .semver.config file
        subprocess.check_call('git config set --local semver.initial 2.0.0', cwd=self.test_dir, shell=True)
        subprocess.check_call('git config set --local semver.prefix version', cwd=self.test_dir, shell=True)
        result = self.run_cli()    
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
        result = self.run_cli()
        self.assertIn("v0.0.1", result.stdout)

        subprocess.check_call('git tag -a -m onetwoone ver1.2.1', cwd=self.test_dir, shell=True)
        result = self.run_cli()
        self.assertIn("ver1.2.1", result.stdout)

        subprocess.check_call('git tag -a -m oneoneone version1.1.1', cwd=self.test_dir, shell=True)
        result = self.run_cli()
        self.assertIn("ver1.2.1", result.stdout)

        subprocess.check_call('git tag -a -m twooneone version2.1.1-freetext', cwd=self.test_dir, shell=True)
        result = self.run_cli()
        self.assertIn("version2.1.1-freetext", result.stdout)

        subprocess.check_call('git tag -a -m nonvalid version3.11-freetext', cwd=self.test_dir, shell=True)
        result = self.run_cli()
        self.assertIn("version2.1.1-freetext", result.stdout)