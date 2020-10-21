

def read_file_as_string(name):
    with open("inputs/" + name) as f:
        return f.read()


def read_file_as_lines(name):
    with open("inputs/" + name) as f:
        for line in f:
            yield line.rstrip("\n")
