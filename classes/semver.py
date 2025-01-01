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
    def __init__(self):
        config = self.get_config()
        self.prefix = config.get('prefix', self.prefix)
        self.initial = config.get('initial', self.initial)
        self.suffix = config.get('suffix', self.suffix)
        self.current_semver, self.current_tag = Semver.__get_current_semver_tuple()
        if not self.current_semver:
            try:
                self.current_semver = tuple(map(int, self.initial.split('.')))
            except Exception as e:
                print(f"Failed to parse initial version, doesn't look like a three-level integer: {e}")
            self.current_tag = self.prefix + self.initial + self.suffix

        # Initialize next potential versions as strings
        self.next ={}
        # Bump major, reset minor and patch
        self.next['major'] = f"{self.current_semver[0] + 1}.0.0"
        # Leave major, bump minor, reset patch
        self.next['minor'] = f"{self.current_semver[0]}.{self.current_semver[1] + 1}.0"
        # Leave major and minor, bump patch
        self.next['patch'] = f"{self.current_semver[0]}.{self.current_semver[1]}.{self.current_semver[2] + 1}"

    def get_config(self):
        """Read the .semver.config file and return the configuration"""
        config_map = {}
        try:
            config = os.popen(
                'git config list --file $(git rev-parse --show-toplevel)/.semver.config 2>/dev/null').read().strip()
        except Exception:
            pass
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
            print("Nothing to do - no configuration is changed")
        

  
    def bump(self, level=str, message=None, suffix=None):
        was_semver, was_tag = self.current_semver, self.current_tag
        try:
            cmd = self.get_git_tag_cmd(level, message, suffix)
            subprocess.check_call(cmd, shell=True)
        except Exception as e:
            print(f"Failed to run command: {e}")
            sys.exit(1)
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