import os
import shutil

from subprocess import CalledProcessError, check_output, PIPE, run

TOML_START = 12

class Icecream():
    def __init__(self):
        pass

    def __enter__(self):
        os.environ["RUST_BACKTRACE"] = "1"

        with open("Cargo.toml", 'r') as f:
            self.icenames = [line.split(' =')[0] for line in f.readlines()[12:]]
        return self

    def __exit__(self, *args):
        
        os.environ["RUST_BACKTRACE"] = "0"
        run(["cargo", "clean"])
    
    def __iter__(self):

        rare_features = {"broken_mir" : "generator_ice"}

        for version in ["stable", "beta", "nightly"]:
            run(["rustup", "override", "set", version])

            for ice_name in self.icenames:
                print("[*] Running ICE {} on {}".format(ice_name, version))
                
                # @TODO: Find a better way to detect we need custom, rare features.
                features = ','.join([version, ice_name, rare_features.get(ice_name, '')])


                try:
                    out = check_output(["cargo", "build", "--features", features], stderr = PIPE, shell = False)
                except CalledProcessError as e:
                    err = e.stderr.decode('utf-8')

                    if 'internal compiler error' in err or "thread 'main' panicked at" in err:
                        lines = err.split('\n')

                        backtrace = '\n'.join(lines[1:])

                        yield version, ice_name, backtrace
        yield "nightly", "test", "comp error"

def join_paths(ice_name, version):

    directory = "\\".join(["backtraces", ice_name])
    
    if not os.path.exists(directory):
        os.mkdir(directory)
    
    return "\\".join([directory, version])
    
if __name__ == '__main__':
    with Icecream() as icer:
        for version, ice_name, backtrace in icer:
            with open(join_paths(ice_name, version), 'w') as f:
                f.write(backtrace)
