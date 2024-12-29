#!/usr/bin/env python3

import os
import sys
import argparse

# Add the subdirectory containing the classes to the general class_path
class_path = os.path.dirname(os.path.abspath(__file__))+"/classes"
sys.path.append(class_path)

from semver import Semver


if __name__ == "__main__":

    # Define the parent parser with the --verbose argument
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')

    # Define command-line arguments
    parser = argparse.ArgumentParser(parents=[parent_parser])   

    # create two sub commands  - bump and init. Bump should take one of three required withchs - --major, --minor and --patch
    # init should take two optional switches -  --prefix and --offset
    subparsers = parser.add_subparsers(dest='command')

    bump_parser = subparsers.add_parser('bump', parents=[parent_parser], help='Bump the version')
    bump_group = bump_parser.add_mutually_exclusive_group(required=True)
    bump_group.add_argument('--major', action='store_true', help='Bump the major version')
    bump_group.add_argument('--minor', action='store_true', help='Bump the minor version')
    bump_group.add_argument('--patch', action='store_true', help='Bump the patch version')

    # Add the --message option to take a string parameter
    bump_parser.add_argument('-m', '--message', type=str, help='Additional message to add to the tag')

    # Add the --run and --no-run options as mutually exclusive
    run_group = bump_parser.add_mutually_exclusive_group(required=False)
    run_group.add_argument('--run', dest='run', action='store_true', help='Run the bump (default)')
    run_group.add_argument('--no-run', dest='run', action='store_false', help='Do not run the bump')
    bump_parser.set_defaults(run=True)

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
        if args.verbose:
            print("Running in " + args.command + " subcommand mode.")
        semver = Semver()
    
        
        if args.major:
            if args.verbose:
                print("Bumping major version.")

        elif args.minor:
            if args.verbose:
                print("Bumping minor version.")

        elif args.patch:
            if args.verbose:
                print("Bumping patch version.")
            

            print(semver.commands['patch'])
        sys.exit(0)
    
    if args.command == 'init':
        print("Running in " + args.command + " subcommand mode.")
        if args.prefix:
            print("Using prefix: " + args.prefix)
        if args.offset:
            print("Using offset: " + str(args.offset))
        sys.exit(0)


