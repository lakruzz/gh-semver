import os
import subprocess
import sys
import re

# Add directory of this class to the general class_path
# to allow import of sibling classes
class_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(class_path)


class Semver:
    """Class used to represent the semver state of git repository"""

    # Class constants
    config_file = ".semver.config"    

    # Class variables

    prefix = None
    initial = None
    suffix = None
    workdir = os.getcwd() # Required, therefore also  set at class level to allow a null constructor
    git_root = None
    config = {}
    semver_tags = {}
    current_semver = None
    current_tag = None
    next ={}

    def __run_git(self, cmd=str):
        result = subprocess.run(
        cmd, capture_output=True, text=True, shell=True, cwd=self.workdir)
        return result    
          
    # Instance methods
    def __init__(self, workdir=None):
        if workdir:
            # check if the directory exists
            if not os.path.exists(workdir):
                raise FileNotFoundError(f"Directory {workdir} does not exist")
            self.workdir = os.path.abspath(workdir)

        result = self.__run_git('git rev-parse --show-toplevel')
        if not result.returncode == 0: 
            raise FileNotFoundError(f"{result.stderr}")
            sys.exit(1)
        self.git_root = result.stdout.strip()
        self.config_file = self.git_root + '/' + self.config_file

        self.__read_semver_tags()
        self.__read_semver_config()

    def __read_semver_tags(self):
        """Desinged to be called from __init__ to read the tags in the repo and again 
        after a from bump, when a new tag is created.

        Reads the tags in the repo, extract the semantic version tags
        and store them in a dictionary (semver_tags) with the tuple of the
        three integers as the key and the tag as the value and keep the most recent
        version (current_semver and current_tag).

        Also sets the next major, minor and patch versions in the next dictionary.
        """

        tags = self.__run_git('git tag').stdout.strip().split('\n')
        semver_pattern = re.compile(r'(\d+)\.(\d+)\.(\d+)')

        self.semver_tags = {}

        for tag in tags:
            match = semver_pattern.search(tag)
            if match:
                self.semver_tags[tuple(map(int, match.groups()))] = tag

        if self.semver_tags:
            sorted_semver_tags = sorted(self.semver_tags.keys())
            self.current_semver = sorted_semver_tags[-1]
            self.current_tag = self.semver_tags[sorted_semver_tags[-1]]

        if not self.current_semver:
            self.__set_current_semver_from_initial()

        self.__set_next_versions()

    def __set_current_semver_from_initial(self):

        if self.initial == None:
            self.initial = '0.0.0'
        try:
            self.current_semver = tuple(map(int, self.initial.split('.')))
        except Exception as e:
            raise ValueError(f"Failed to parse initial version, doesn't look like a three-level integer: {e}")
        
        suffix = ''
        if self.suffix and self.suffix != '':
            suffix = f"-{self.suffix}"
            
        self.current_tag = f"{self.prefix}{self.initial}{suffix}"
    

    def __set_next_versions(self):    
        # Bump major, reset minor and patch
        self.next['major'] = f"{self.current_semver[0] + 1}.0.0"
        # Leave major, bump minor, reset patch
        self.next['minor'] = f"{self.current_semver[0]}.{self.current_semver[1] + 1}.0"
        # Leave major and minor, bump patch
        self.next['patch'] = f"{self.current_semver[0]}.{self.current_semver[1]}.{self.current_semver[2] + 1}"
     
    def __read_semver_config(self):
        """Read the .semver.config file and store the configuration as a dictionary"""
        
        self.config = {}

        # The config_file may not exist - we don't care. Just continue and return an empty dict
        config = self.__run_git(f'git config list --file {self.config_file}').stdout
        try:
            for line in config.split('\n'):
                key, value = line.split('=')
                if key == 'semver.prefix':
                    self.config['prefix'] = value
                elif key == 'semver.initial':
                    self.config['initial'] = value
                elif key == 'semver.suffix':
                    self.config['suffix'] = value
        except Exception:
            pass

        self.prefix = self.config.get('prefix', '')
        self.initial = self.config.get('initial', '0.0.0')
        self.suffix = self.config.get('suffix', '')
        if self.semver_tags.keys().__len__() == 0:
            self.__set_current_semver_from_initial()
            self.__set_next_versions()
    
    def set_config(self, prefix=None, initial=None, suffix=None):
        """Set the configuration in the .semver.config file"""

        updated = False
        args = {'prefix': prefix, 'initial': initial, 'suffix': suffix}
        for setting in args.keys():
            if args[setting]:
                result = self.__run_git(f'git config --file {self.config_file} semver.{setting} {args[setting]}')
                updated = True     
        self.__read_semver_config()
        
  
    def bump(self, level=str, message=None, suffix=None):
        cmd = self.get_git_tag_cmd(level, message, suffix)
        result = self.__run_git(cmd)
        self.__read_semver_tags()
        return self.current_tag

    def get_git_tag_cmd(self, level=str, message=None, suffix=None):
        if message:
            message = f"\n{message}"
        else:
            message = ""

        if suffix:
            suffix = f"-{suffix}"
        else:
            if self.suffix: 
                suffix = f"-{self.suffix}"
            else:
                suffix = ""
        
        next_tag = f"{self.prefix}{self.next[level]}{suffix}"

        return f"git tag -a -m \"{next_tag}\nBumped {level} from version '{self.current_tag}' to '{next_tag}'{message}\" {next_tag}"