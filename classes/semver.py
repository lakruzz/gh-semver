import os
import subprocess
import sys
import re


# Add directory of this class to the general class_path
# to allow import of sibling classes
class_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(class_path)


class Semver:
    # Class variables
    config_file = ".semver.config"    
    prefix = ''      # Default prefix
    initial = "0.0.0"  # Default offset
    suffix = ''      # Default suffix
    message = ''     # Default message
    workdir = os.getcwd()
    git_root = None
    config = None
    semver_tags = {}
    current_semver = None
    current_tag = None
    next ={}

    def __run_git(self, cmd=str):
        result = subprocess.run(
        cmd, capture_output=True, text=True, shell=True, cwd=self.workdir)
        return result

    # Static methods
    @staticmethod
    def get_current_semver():
        """Return the current semver tag"""
        semver=Semver()
        return semver.current_tag
    

    @staticmethod
    def __get_initial_offset():
        # If `git config --get semver.initial` returns a value, return it as the offset else
        # try `gitconfig --get --file .semver.config semver.initial` and if it returns a value then use that
        # else return the default value Semver.initial
 
        prefix = Semver.__get_prefix()
        try:
            initial_offset = os.popen(
                'git config get semver.initial').read().strip()
            if initial_offset:
                return initial_offset
        except Exception:
            pass

        try:
            initial_offset = os.popen(
                'git config get --file $(git rev-parse --show-toplevel)/.semver.config semver.initial').read().strip()
            if initial_offset:
                return initial_offset
        except Exception:
            pass

        return Semver.initial
    
    @staticmethod
    def __get_prefix():
       # If `git config --get semver.prefix` returns a value, return it as the prefix else
       # try `gitconfig --get --file .semver.config semver.prefix` and if it returns a value then use that
       # else return the default value Semver.prefix
        try:
            initial_offset = os.popen(
                'git config get semver.prefix').read().strip()
            if initial_offset:
                return initial_offset
        except Exception:
            pass

        try:
            initial_offset = os.popen(
                'git config get --file $(git rev-parse --show-toplevel)/.semver.config semver.prefix'
                ).read().strip()
            if initial_offset:
                return initial_offset
        except Exception:
            pass

        return Semver.prefix

    @staticmethod
    def __get_current_semver_tuple():    
        tags = os.popen('git tag').read().strip().split('\n')
        semver_pattern = re.compile(r'(\d+)\.(\d+)\.(\d+)')
        semver_tags = {}

        for tag in tags:
            match = semver_pattern.search(tag)
            if match:
                semver_tags[tuple(map(int, match.groups()))] = tag

        if semver_tags:
            sorted_semver_tags = sorted(semver_tags.keys())
            return sorted_semver_tags[-1], semver_tags[sorted_semver_tags[-1]]
        else:
            return None, None
        
    # Instance methods
    def __init__(self, workdir=None):
        if workdir:
            # check if the directory exists
            if not os.path.exists(workdir):
                raise FileNotFoundError(f"Directory {workdir} does not exist")
            self.workdir = workdir

        result = self.__run_git('git rev-parse --show-toplevel')
        if not result.returncode == 0:
            raise FileNotFoundError(f"Not running in a git repository: {result.stderr}")
            sys.exit(1)
        self.git_root = result.stdout.strip()
        self.config_file = self.git_root + '/' + self.config_file
        self.config = self.__get_config()
        self.prefix = self.config.get('prefix', self.prefix)
        self.initial = self.config.get('initial', self.initial)
        self.suffix = self.config.get('suffix', self.suffix)

        #tags = os.popen('git tag').read().strip().split('\n')
        tags = self.__run_git('git tag').stdout.strip().split('\n')
        semver_pattern = re.compile(r'(\d+)\.(\d+)\.(\d+)')

        for tag in tags:
            match = semver_pattern.search(tag)
            if match:
                self.semver_tags[tuple(map(int, match.groups()))] = tag

        if self.semver_tags:
            sorted_semver_tags = sorted(self.semver_tags.keys())
            self.current_semver = sorted_semver_tags[-1]
            self.current_tag = self.semver_tags[sorted_semver_tags[-1]]

        if not self.current_semver:
            try:
                self.current_semver = tuple(map(int, self.initial.split('.')))
            except Exception as e:
                print(f"Failed to parse initial version, doesn't look like a three-level integer: {e}")
            self.current_tag = self.prefix + self.initial + self.suffix

        # Bump major, reset minor and patch
        self.next['major'] = f"{self.current_semver[0] + 1}.0.0"
        # Leave major, bump minor, reset patch
        self.next['minor'] = f"{self.current_semver[0]}.{self.current_semver[1] + 1}.0"
        # Leave major and minor, bump patch
        self.next['patch'] = f"{self.current_semver[0]}.{self.current_semver[1]}.{self.current_semver[2] + 1}"

    def __get_config(self):
        """Read the .semver.config file and return the configuration"""
        config_map = {}
        
        # The config_file may not exist - we don't care. Just continue and return an empty dict
        config = self.__run_git(f'git config list --file {self.config_file}').stdout
        try:
            for line in config.split('\n'):
                key, value = line.split('=')
                if key == 'semver.prefix':
                    config_map['prefix'] = value
                elif key == 'semver.initial':
                    config_map['initial'] = value
                elif key == 'semver.suffix':
                    config_map['suffix'] = value
        except Exception:
            pass
        return config_map
    
    def set_config(self, prefix=None, offset=None, suffix=None):
        """Set the configuration in the .semver.config file"""

        updated = False

        if prefix:
            try:
                subprocess.check_call(f'git config --file $(git rev-parse --show-toplevel)/{self.config_file} semver.prefix {prefix}', shell=True)
            except subprocess.CalledProcessError as e:
                print(f"Failed to set prefix: {e}")
                sys.exit(1)
            updated = True
            self.prefix = prefix
            print (f"semver.prefix = {prefix}")
        if offset:
            try:
                subprocess.check_call(f'git config --file $(git rev-parse --show-toplevel)/{self.config_file} semver.initial {offset}', shell=True)
            except subprocess.CalledProcessError as e:
                print(f"Failed to set offset: {e}")
            updated = True
            self.initial = offset
            print (f"semver.offset = {offset}")
        if suffix:
            try:
                subprocess.check_call(f'git config --file $(git rev-parse --show-toplevel)/{self.config_file} semver.suffix {suffix}', shell=True)
            except subprocess.CalledProcessError as e:  
                print(f"Failed to set suffix: {e}")
            updated = True
            self.suffix = suffix
            print (f"semver.suffix = {suffix}")
        
        if not updated:
            current_config = self.get_config()
            print("Current configuration:")
            if current_config:
                for key, value in current_config.items():
                    print(f"  semver.{key} = {value}") 
            else:
                print("  No configuration defined")       

  
    def bump(self, level=str, message=None, suffix=None):
        cmd = self.get_git_tag_cmd(level, message, suffix)
        result = self.__run_git(cmd)
        self.current_semver, self.current_tag = Semver.__get_current_semver_tuple()
        return self.current_tag

    def get_git_tag_cmd(self, level=str, message=None, suffix=None):
        if message:
            message = f"\n{message}"
        else:
            message = ""

        if suffix:
            suffix = f"-{suffix}"
        else:    
            suffix = ""
        
        next_tag = f"{self.prefix}{self.next[level]}{suffix}"

        return f"git tag -a -m \"Bumped {level} from version '{self.current_tag}' to '{next_tag}'{message}\" {next_tag}"