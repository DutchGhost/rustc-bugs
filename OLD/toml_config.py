import toml
import os.path
from functools import wraps, partial
import types
import inspect
import os
from subprocess import check_output, CalledProcessError, PIPE
from enum import Enum
import datetime
from dateutil import parser as timeparser

RUSTC_VERSIONS = ["stable", "beta", "nightly"]

class Iced(Enum):
    TRUE = 1
    FALSE = 2

def change_rustc_version(func = None, *, version):
    if func is None:
        return partial(change_rustc_version, version = version)

    @wraps(func)
    def wrapper(*args, **kwargs):
        check_output(["rustup", "override", "set", version], stderr = PIPE, shell = False)

        return func(*args, **kwargs)

    return wrapper

def write_backtrace_on_error(func = None, *, version):
    if func is None:
        return partial(write_backtrace_on_error, version = version)
    
    os.environ["RUST_BACKTRACE"] = "1"
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = Iced.FALSE
        try:
            ret = func()

        except CalledProcessError as e:

            err = e.stderr.decode('utf-8')
            if 'internal compiler error' in err:
                
                ret = Iced.TRUE

                lines = err.split('\n')

                backtrace = '\n'.join(lines[1:])

                with open("backtraces\{}.backtrace".format(version), 'w') as f:
                    f.write(backtrace)
        return ret
    #os.environ["RUST_BACKTRACE"] = "0"
    
    return wrapper

def into_toml(toml_to_parse):

        toml_loader = toml.load if os.path.isfile(toml_to_parse) else toml.loads

        contents = toml_loader(toml_to_parse)

        return contents

class TomlReader():
    
    def __init__(self, toml, version_header = "versions"):
        
        parsed_toml = into_toml(toml)

        vs = parsed_toml.get(version_header, RUSTC_VERSIONS)

        extracted_versions = list(vs)

        print(extracted_versions)

        self.versions = extracted_versions
        self.toml = parsed_toml
        self.functions = []
        self.iced = []

        self.introspect()
    
    def introspect(self):
        """
        For every version that must be tested,
            1. create a function that switches to that version
            2. try compile with that version
            3. log backtrace if needed
        """
        cargo_run = ["cargo", "run"]

        for v in RUSTC_VERSIONS:

            if v in self.versions:
                
                @write_backtrace_on_error(version = v)
                @change_rustc_version(version = v)
                def run_version():
                    check_output(cargo_run, stderr = PIPE, shell = False)
                    return Iced.FALSE

                func = run_version
                methodname = '_'.join(["run", v])
                setattr(func, '__name__', methodname)
                self.__dict__[methodname] = types.MethodType(func, self.__class__)
                self.functions.append(func)

    def process(self):
        for f in self.functions:
            print(f.__name__)
            has_iced = f()
            
            self.iced.append((f.__name__[4:], has_iced))

    def into_toml_writer(self, toml_file = "info.toml"):
        return TomlWriter(self.toml, toml_file = toml_file, iced = self.iced)

def time_now():
    now = str(datetime.datetime.now().isoformat()).split('.')[0]

    return ''.join([now, 'Z'])

class TomlWriter():
    def __init__(self, toml, toml_file = "info.toml", iced = []):
        self.toml = toml
        self.toml_file = toml_file
        self.iced = iced

    def set_update_time(self, time_header = "optional", field = "last_checked"):
        self.toml[time_header][field] = timeparser.parse(time_now())

    def set_resolved(self, resolved_header = "resolved"):
        e_versions = self.toml[resolved_header]

        for (v, has_iced) in self.iced:
            should_not_error = e_versions.get(v, False)

            if has_iced == Iced.TRUE and should_not_error:
                print("Crashed while it should not have!")
            
            e_versions[v] = False if has_iced == Iced.TRUE else True
        
        # Drop all the versions that are still in the info file due to previous test, but that we did not test
        check_version = set([v for (v, _) in self.iced])
        diff = set(e_versions) - check_version
        for d in diff:

            e_versions.pop(d, None)

    def write(self):
        with open(self.toml_file, 'w') as f:
            toml.dump(self.toml, f)

    def process(self, time_header = "optional", field = "last_checked", resolved_header = "resolved"):
        self.set_update_time(time_header, field)
        self.set_resolved(resolved_header)
        self.write()

if __name__ == '__main__':
    reader = TomlReader("info.toml")

    reader.process()

    writer = reader.into_toml_writer()
    
    writer.process()
