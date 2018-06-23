import toml
import argparse

import os
import shutil
import fileinput
import datetime
from subprocess import run

def generate_info(name):
    toml_string = """
    [info]
    name = "{}" # Name of the bug
    discription = "" # Little discription of the bug
    discovery_date = {} # When was it discovered
    type = "" # What kind of bug, e.g ICE, invalid code generation etc
    labels = "" # What labels has it been given?
    effects = [""] # the versions it effects
    resolved = false # Has it been fixed or not?

    [issue]
    link = "" # link to the issue

    [additional]

    [optional]
    last_checked = {} # When was this bug last tested
    """.format(name, datetime.datetime.now().isoformat(), datetime.datetime.now().isoformat())

    parsed_toml = toml.loads(toml_string)

    with open("info.toml", 'w') as f:
        try:
            toml.dump(parsed_toml, f)
        except TypeError as e:
            print("typerror: {}".format(e))

if __name__ == '__main__':

    # Create a new argparser
    parser = argparse.ArgumentParser(description = "Generates project for a found rustc-bug")

    # We need a name
    parser.add_argument('--name', help = "the name of the found bug", nargs=1, required = True)
    
    # We might call --new, or --run, but never both
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--run', help = "runs the given name", required = False, action='store_true')
    group.add_argument('--new', help = "creates a new cargo project with the given name", required = False, action='store_true')
    
    args = parser.parse_args()

    name = args.name[0]
    if args.run:
        os.chdir(name)
        run(["cargo", "run"])
    
    if args.new:
        run(["cargo", "new", name])
        os.chdir(name)
        generate_info(name)