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
                return prefix+initial_offset
        except Exception:
            pass

        try:
            initial_offset = os.popen(
                'git config get --file $(git rev-parse --show-toplevel)/.semver.config semver.initial').read().strip()
            if initial_offset:
                return prefix+initial_offset
        except Exception:
            pass

        return prefix+Semver.initial
    

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
    

    
    def __init__(self):
        self.prefix = Semver.__get_prefix()
        self.initial = Semver.__get_initial_offset()
        self.current_semver = Semver.get_current_semver()

    @staticmethod
    def get_current_semver():
        # Run `git tag` and and grep the ones that match a semver three level-integer (\d+\.\d+\.\d+).
        # Create a map of tuples where the key is the match from the regexp and the value is the tag.
        # Sort the map by the tuple keys and return the value of last tuple of the sorted map.
        tags = os.popen('git tag').read().strip().split('\n')
        semver_pattern = re.compile(r'(\d+)\.(\d+)\.(\d+)')
        semver_tags = {}

        for tag in tags:
            match = semver_pattern.search(tag)
            if match:
                semver_tags[tuple(map(int, match.groups()))] = tag

        if semver_tags:
            sorted_semver_tags = sorted(semver_tags.keys())
            return semver_tags[sorted_semver_tags[-1]]

        return Semver.__get_initial_offset()
