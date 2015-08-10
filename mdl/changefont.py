import os
import re


if __name__ == '__main__':
    currentDir = os.listdir(".")
    pattern = re.compile("material.*")
    for afile in currentDir:
        if pattern.match(afile):
            with open(afile, "r+") as f:
                data = f.read()
                data = data.replace("font-size:14px", "font-size:16px")
                f.seek(0, 0)
                f.write(data)
