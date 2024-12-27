#!/usr/bin/env python3

import os
import sys
import argparse

# Add the subdirectory containing the classes to the general class_path
class_path = os.path.dirname(os.path.abspath(__file__))+"/classes"
sys.path.append(class_path)

from semver import Semver


if __name__ == "__main__":

    # Define command-line arguments
    parser = argparse.ArgumentParser()

    # Add a global --verbose switch
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')

    # create two sub commands  - bump and init. Bump should take one of three required withchs - --major, --minor and --patch
    # init should take two optional switches -  --prefix and --offset
    subparsers = parser.add_subparsers(dest='command')

    bump_parser = subparsers.add_parser('bump', help='Bump the version')
    bump_group = bump_parser.add_mutually_exclusive_group(required=True)
    bump_group.add_argument('--major', action='store_true', help='Bump the major version')
    bump_group.add_argument('--minor', action='store_true', help='Bump the minor version')
    bump_group.add_argument('--patch', action='store_true', help='Bump the patch version')

    init_parser = subparsers.add_parser('init', help='Initialize the repository')
    init_parser.add_argument('--prefix', help='Prefix for the version')
    init_parser.add_argument('--offset', help='Offset for the version')

    args = parser.parse_args()

    # Handle the case where no subcommand is provided
    if args.command is None:
        if args.verbose:
          print("Running default behavior. Returning current SemVer.")

        # Add default behavior here
        print(Semver.get_current_semver())

        sys.exit(0)

    if args.command == 'bump':
        print("Running in " + args.command + " subcommand mode.")
        if args.major:
            print("Bumping major version.")
        elif args.minor:
            print("Bumping minor version.")
        elif args.patch:
            print("Bumping patch version.")
        sys.exit(0)
    
    if args.command == 'init':
        print("Running in " + args.command + " subcommand mode.")
        if args.prefix:
            print("Using prefix: " + args.prefix)
        if args.offset:
            print("Using offset: " + str(args.offset))
        sys.exit(0)


