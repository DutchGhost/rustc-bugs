from subprocess import PIPE, run

if __name__ == '__main__':
    with open("Cargo.toml", 'r') as f:
        features = [line.split(' =')[0] for line in f.readlines()[8:]]
        print(features)
        run(["cargo", "doc", "--features", ','.join(features)], stderr = PIPE, shell = False)
