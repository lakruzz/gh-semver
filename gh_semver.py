#!/usr/bin/env python3

import os
import sys
import argparse
import re

# Add the subdirectory containing the classes to the general class_path
class_path = os.path.dirname(os.path.abspath(__file__)) + "/classes"
sys.path.append(class_path)

from semver import Semver

def validate_suffix(suffix):
    if not re.match("^[a-z0-9_-]*$", suffix):
        raise argparse.ArgumentTypeError("Suffix: Allowed characters are lowercase letters, numbers, dashes and underscores")
    return suffix

def validate_prefix(prefix):
    if not re.match("^[a-zA-z]*$", prefix):
        raise argparse.ArgumentTypeError("Prefix: Allowed characters are lowercase and uppercase letters")
    return prefix

def validate_initial(initial):
    if not re.match(r"^\d+\.\d+\.\d+$", initial):
        raise argparse.ArgumentTypeError("Initial offset: Must be a three-level integer separated by dots (e.g. 1.0.0)")
    return initial

def parse(args=None):
    # Define the parent parser with the --verbose argument
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')

    # Define command-line arguments
    parser = argparse.ArgumentParser(parents=[parent_parser])

    # Create two subcommands - bump and config
    subparsers = parser.add_subparsers(dest='command')

    bump_parser = subparsers.add_parser('bump', help='Bump the version')
    bump_group = bump_parser.add_mutually_exclusive_group(required=True)
    bump_group.add_argument('--major', action='store_true', help='Bump the major version')
    bump_group.add_argument('--minor', action='store_true', help='Bump the minor version')
    bump_group.add_argument('--patch', action='store_true', help='Bump the patch version')

    bump_parser.add_argument('--message', '-m', type=str, help='Additional message to add to the tag')
    bump_parser.add_argument('--suffix', type=validate_suffix, help='Suffix to add to the version. Allowed characters are lowercase letters, numbers, dashes, and underscores')

    # Add the --run and --no-run options as mutually exclusive
    run_group = bump_parser.add_mutually_exclusive_group(required=False)
    run_group.add_argument('--run', dest='run', action='store_true', help='Run the bump (default)')
    run_group.add_argument('--no-run', dest='run', action='store_false', help='Do not run the bump')
    bump_parser.set_defaults(run=True)

    config_parser = subparsers.add_parser('config', parents=[parent_parser], help='Creates or updates the .semver.config file')
    config_group = config_parser.add_argument_group('Configuration options')
    config_group.add_argument('--prefix', type=validate_prefix, help='Prefix for the tag. Allowed characters are lowercase and uppercase letters', default=None)
    config_group.add_argument('--suffix', type=validate_suffix, help='Suffix for the tag. Allowed characters are lowercase letters, numbers, dashes and underscores', default=None)
    config_group.add_argument('--initial', type=validate_initial, help='Initial offset for the first tag. Must be a three-level integer separated by dots (e.g., 1.0.0)', default=None)

    args = parser.parse_args(args)
    return args


if __name__ == "__main__":
    args = parse(sys.argv[1:])

    # Handle the case where no subcommand is provided
    if args.command is None:
        semver = Semver()
        print(semver.current_tag)
        sys.exit(0)

    if args.command == 'bump':
        semver = Semver()
        level = args.major and 'major' or args.minor and 'minor' or 'patch'    
        if args.run:
            result = semver.bump(level=level, message=args.message, suffix=args.suffix)
            print(result)
        else:
            result = semver.get_git_tag_cmd(level=level, message=args.message, suffix=args.suffix)
            print(result)