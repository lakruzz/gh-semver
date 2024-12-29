import os
import sys
import re


# Add directory of this class to the general class_path
# to allow import of sibling classes
class_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(class_path)


class Semver:
    prefix = "v"     # Default prefix
    initial = "0.0.0"  # Default offset

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
                'git config get --file $(git rev-parse --show-toplevel)/.semver.config semver.prefix').read().strip()
            if initial_offset:
                return initial_offset
        except Exception:
            pass

        return Semver.prefix
    
    def __init__(self, message=None):
        self.prefix = Semver.__get_prefix()
        self.initial = Semver.__get_initial_offset()
        self.message = message
        self.current_semver, self.current_tag = Semver.__get_current_semver_tuple()
        if not self.current_semver:
            try:
                self.current_semver = tuple(map(int, self.initial.split('.')))
            except Exception as e:
                print(f"Failed to parse initial version, doesn't look like a three-level integer: {e}")
            self.current_tag = self.prefix + self.initial
        self.commands = {}
        self.commands['major'] = 'git tag -a -m "Bumped major from version  \'' + self.current_tag + '\'" ' + self.prefix + str(self.current_semver[0] + 1) + '.0.0'
        self.commands['minor'] = 'git tag -a -m "Bumped minor from version  \'' + self.current_tag + '\'" ' + self.prefix + str(self.current_semver[0]) + '.' + str(self.current_semver[1] + 1) + '.0'
        self.commands['patch'] = 'git tag -a -m "Bumped patch from version  \'' + self.current_tag + '\'" ' + self.prefix + str(self.current_semver[0]) + '.' + str(self.current_semver[1]) + '.' + str(self.current_semver[2] + 1)


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
    

    @staticmethod
    def get_current_semver():
        semver=Semver()
        return semver.current_tag
