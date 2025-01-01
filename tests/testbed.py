import os
import subprocess


class Testbed:
    @staticmethod
    def cleanup_testbed(test_dir):
        if os.path.exists(test_dir):
            print("Cleaning up the testbed")
            try:
                subprocess.check_call('rm -rf {}'.format(test_dir), shell=True)
            except subprocess.CalledProcessError as e:
                print(f"Failed to remove test directory: {e}")
                
        
    @staticmethod
    def create_testbed(test_dir):
        subprocess.check_call('mkdir -p {}'.format(test_dir), shell=True)
        subprocess.check_call('git init', cwd=test_dir, shell=True)
        subprocess.check_call('git checkout -b testbed', cwd=test_dir, shell=True)

    @staticmethod
    def run_cli(cli_path, *args, cwd):
        result = subprocess.run(
            ['python3', cli_path] + list(args), cwd=cwd, capture_output=True, text=True)
        return result
