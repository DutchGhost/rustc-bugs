import argparse

import os
import shutil
import fileinput
from subprocess import run

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

        # Copy the template to the cargo project
        shutil.copyfile('info-template.toml', '{}\info.toml.partial'.format(name))

        os.chdir(name)
        with open('info.toml.partial', 'r') as pf:
            with open('info.toml', 'w') as f:

                # strip newlines
                for line in map(lambda s: s.rstrip(), pf.readlines()):
                    
                    # Split the ' # ...' off
                    info, *rest = line.split(' # ')

                    # We can write the name directly
                    if "name" in info:
                        f.write(info.replace(r'name = ""', r'name = "{}"'.format(name)))
                    else:
                        f.write(info)
                    
                    f.write('\n')
        os.remove('info.toml.partial')