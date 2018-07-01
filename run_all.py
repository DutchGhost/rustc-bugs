import os
from subprocess import run

if __name__ == '__main__':
    for project in os.listdir(os.getcwd()):
        if os.path.isdir(project) and project != '.git':
            print('updating', project)
            run(["python", "bug.py", "--name", project, "--run"])