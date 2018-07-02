import os
import shutil

from subprocess import CalledProcessError, check_output, PIPE, run
if __name__ == '__main__':
    os.environ["RUST_BACKTRACE"] = "1"
    
    # Get the ICE's.
    with open("Cargo.toml", 'r') as f:
        runs = [line.split(' =')[0] for line in f.readlines()[11:]]
    

    results = []
    for v in ["stable", "beta", "nightly"]:
        
        # Change the version
        run(["rustup", "default", v])
        
        # For each ICE, build the lib.
        for ice_name in runs:
            print('running {} in version {}'.format(ice_name, v))
            
            try:
                out = check_output(["cargo", "build", "--features", ','.join([v, ice_name])], stderr = PIPE, shell = False)
            except CalledProcessError as e:
                err = e.stderr.decode('utf-8')

                if 'internal compiler error' in err and "thread 'main' panicked at" in err:

                    lines = err.split('\n')

                    backtrace = '\n'.join(lines[1:])
                    print(v)
                    results.append([v, ice_name, backtrace])
    
    
    join_paths = lambda ice_name, version: r"\\".join(["backtraces", ice_name, version])
    
    for version, ice_name, backtrace in results:
        print(version, ice_name)
        
        path = join_paths(ice_name, version)
        print(path)
        try:
            os.remove(path)
        except Exception as e:
            print('could not rm path')

        with open(path, 'w') as f:
            f.write(backtrace)
    
    run(["cargo", "clean"])
