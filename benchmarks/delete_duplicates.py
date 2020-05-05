import glob
import os

def build_dict():
    hashes = set()
    f = open('fabwave-collisions.txt', 'r')
    for line in f:
        words = line.split(' ')
        hash = words[0]
        file_name = words[-1].strip('\n')

        # if hash already exists, delete the file
        if hash in hashes:
            if os.path.exists(file_name):
                os.remove(file_name)
            else:
                print(file_name, " does not exist")
        else:
            hashes.add(hash)
    f.close()
    return

def main():
    build_dict()

main()
