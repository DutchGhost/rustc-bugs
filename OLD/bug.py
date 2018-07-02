import toml
import argparse

import os
import sys
import shutil
import fileinput
import datetime
from dateutil import parser as dparser
from subprocess import run, Popen, PIPE, check_output, DEVNULL, CalledProcessError

def time_now():
    now = str(datetime.datetime.now().isoformat()).split('.')

    now = now[0]

    return ''.join([now, "Z"])

def generate_info(name):
    now = time_now()

    toml_string = """
    [info]
    name = "{}" # Name of the bug
    discription = "" # Little discription of the bug
    discovery_date = {} # When was it discovered
    type = "" # What kind of bug, e.g ICE, invalid code generation etc
    effected_versions = [""] # the versions it effects

    [resolved]
    stable = false
    beta = false
    nightly = false

    [issue]
    link = "" # link to the issue

    [optional]
    last_checked = {} # When was this bug last tested

    [additional]
    """.format(name, now, now)

    parsed_toml = toml.loads(toml_string)

    with open("info.toml", 'w') as f:
        # @NOTE: This *might* fail
        toml.dump(parsed_toml, f)

def update_info(effected_versions, name):
    info = toml.load('info.toml')
    info_section = info["info"]

    info_section["effected_versions"] = [v for (v, e) in effected_versions if not e]
    
    optional = info["optional"]
    optional["last_checked"] = dparser.parse(time_now())

    resolved = info["resolved"]

    for (stable_beta_nightly, (v, e)) in zip(["stable", "beta", "nightly"], effected_versions):
        should_not_error = resolved[stable_beta_nightly]

        if should_not_error and not e:
            print("\n\n")
            print("WARNING")
            print("{} crashed on {}, while it should not have", name, stable_beta_nightly)
        resolved[stable_beta_nightly] = e

    with open('info.toml', 'w') as f:
        toml.dump(info, f)

#@NOTE: This also returns True if the process did not exit succesfully, not sure if this is a good thing.
def is_ice(cmd, version):
    try:
        check_output(cmd, stderr=PIPE, shell=False)
        
    except CalledProcessError as e:
        err = e.stderr.decode('utf-8')
        if 'internal compiler error' in err:

            with open('backtraces\{}.backtrace'.format(version), 'w') as f:
                lines = err.split('\n')

                backtrace = '\n'.join(lines[1:])

                f.write(backtrace)
        return True
    return False

def build():
    version_resolved = []
    os.environ["RUST_BACKTRACE"] = "1"
    for version in ["stable", "beta", "nightly"]:
        
        # @NOTE: both of these *might* fail, but is unlikely
        check_output(["rustup", "override", "set", version], stdin=PIPE, stderr=PIPE)
        version = check_output(["rustc", "--version",], stdin=PIPE, shell=False).decode('utf-8').rstrip()

        if is_ice(["cargo", "run"], version):
            version_resolved.append((version, False))
        else:
            version_resolved.append((version, True))

    os.environ["RUST_BACKTRACE"] = "0"
    return version_resolved

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
        e_versions = build()
        update_info(e_versions, name)
        
    if args.new:
        run(["cargo", "new", name])
        os.chdir(name)
        os.mkdir("backtraces")
        generate_info(name)

    run(["git", "add", "backtraces/*"])
    run(["git", "add", "src/*"])

    run(["cargo", "clean"])