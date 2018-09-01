class Logger:
    def __init__(self, file_name="output.log"):
        self.f = open(file_name, "w")

    def print(self, *args):
        self.f.write(" ".join(str(x) for x in args) + "\n")
        self.f.flush()

    def __del__(self):
        self.f.close()
