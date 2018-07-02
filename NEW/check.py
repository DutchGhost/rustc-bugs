import os
import shutil

from subprocess import CalledProcessError, check_output, PIPE, run

class Icecream():
    def __init__(self):
        pass

    def __enter__(self):
        os.environ["RUST_BACKTRACE"] = "1"

        with open("Cargo.toml", 'r') as f:
            self.icenames = [line.split(' =')[0] for line in f.readlines()[11:]]
        return self

    def __exit__(self, *args):
        
        os.environ["RUST_BACKTRACE"] = "0"
        run(["cargo", "clean"])
    
    def __iter__(self):
        for version in ["stable", "beta", "nightly"]:
            run(["rustup", "override", "set", version])

            for ice_name in self.icenames:
                print("[*] Running ICE {} on {}".format(ice_name, version))

                try:
                    out = check_output(["cargo", "build", "--features", ','.join([version, ice_name])], stderr = PIPE, shell = False)
                except CalledProcessError as e:
                    err = e.stderr.decode('utf-8')

                    if 'internal compiler error' in err and "thread 'main' panicked at" in err:
                        lines = err.split('\n')

                        backtrace = '\n'.join(lines[1:])

                        yield version, ice_name, backtrace

def join_paths(ice_name, version):
    return "\\".join(["backtraces", ice_name, version])

if __name__ == '__main__':
    with Icecream() as icer:
        for version, ice_name, backtrace in icer:
            with open(join_paths(ice_name, version), 'w') as f:
                f.write(backtrace)
